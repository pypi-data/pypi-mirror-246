"""
Elasticsearch

Requires an attribute "ElasticAttributes" at the root of your Functions Tree.

See e.g.  test_op_ax_elastic
"""

import sys
import time

# fmt:off
from datetime import datetime
from functools import partial

import elasticsearch
import elasticsearch_dsl as ES
import jsondiff
import ujson as json
from devapp.app import FLG, app
from devapp.tools import get_deep
from elasticsearch import helpers
from operators.con.connections import con_params
from operators.const import stop
from operators.misc_util import getter
from operators.ops.tools import Rx, rx, rx_debuffer

# fmt:on


def perc(f):
    return int((f * 100) + 0.5)


def byte(i):
    return i


# by our typ or overwrittein by our keyname:
text_kw = partial(ES.Text, analyzer='snowball', fields={'raw': ES.Keyword()})


def autoch(s):
    return True if str(s).lower() in ('1', 'true', 'on') else False


def to_date_time(ts):
    return datetime.utcfromtimestamp(ts)


def short(i):
    return int(i)


def long(i):
    return int(i)


def geo_point(md):
    return [md.get('longitude', 0), md.get('latitude', 0)]


g = getattr
# fmt: off
types = {
    int               : ES.Integer,
    byte              : ES.Byte,
    perc              : ES.Byte,
    bool              : ES.Boolean,
    short             : ES.Short,
    long              : ES.Long,
    str               : ES.Keyword,
    # 'order_date'      : partial(ES.Date,format='epoch_millis'),
    to_date_time      : ES.Date,
    # 'cid'             : text_kw,
    # 'disp_stream_id'  : text_kw,
    # 'disp_proc_id'    : text_kw,
    # 'disp_data_id'    : text_kw,
    geo_point         : ES.GeoPoint,
}
# fmt: on


is_ = isinstance
str_types = dict([(k.__name__, k) for k in types if not is_(k, str)])


rec_ch = 'recommended_channel'


def es_host(d):
    """tree_builder's links function output into ela compliant dicts"""
    d['http_auth'] = (d.pop('username', ''), d.pop('password', ''))
    p = d.pop('path', '')
    if p and not d.get('url_prefix'):
        d['url_prefix'] = p[1:]
    return d


class Flags:
    class index_prefix:
        n = '*Any* index created will be having this prefix'
        d = ''


class elastic:
    name = 'elastic'
    con = None

    hosts = None
    multi_url = True
    _instance_flags = Flags  # available per conn cls clone

    class con_defaults:
        host = '127.0.0.1'
        username = 'elastic'
        number_of_shards = 1
        password = 'passw'
        port = 9200
        ssl_show_warn = True
        url_prefix = ('', '%(path)s')
        verify_certs = False

    @classmethod
    def setup(cls):
        l = con_params(cls, defaults=cls.con_defaults)
        ip = '%s_index_prefix' % cls.name
        cls.index_prefix = g(FLG, ip)
        cls.hosts = [es_host(d) for d in l]
        # TODO: to get this dynamic on data, call this at msg time, with data and a unique schema name at hand, for autoexplore
        cls.default_index, cls.mapping, cls.getters = parse_attrs(cls)
        app.info('Have set up elastic')  # , hosts=hs)

    @classmethod
    def _connect(cls):
        if cls.con is not None:
            return
        if cls.hosts is None:
            cls.setup()
        cls.con = elasticsearch.Elasticsearch(cls.hosts)
        # https://elasticsearch-py.readthedocs.io/en/master/transports.html#transports
        while not cls.con.ping():
            try:
                cls.con.indices.refresh()
            except elasticsearch.exceptions.AuthenticationException as ex:
                app.die('Can not authenticate at elastic', exc=ex, host=cls.con)
            except Exception as ex:
                app.warn('Waiting for elastic', hosts=cls.con, ex=str(ex.args))
            time.sleep(2)

    @classmethod
    def _make_index(cls, index, alias):
        mapping = cls.mapping
        if not alias:
            a = index + '_alias'
            alias = {a: {}}
        mapping.update({'aliases': alias})
        while True:
            res = cls.con.indices.create(index=index, ignore=400, body=mapping)
            if res.get('acknowledged'):
                app.info('Index created', idx=index)
                return

            if res.get('status') == 400:
                # have = cls.con.indices.get(index=index)[index]['mappings']
                # ela has a bunch of indizes (with eq mappings, e.g. wifi-1, wifi-2, ..):
                have = None
                for v in cls.con.indices.get(index=index).values():
                    have = v['mappings']
                    break
                # compare:
                # equal rite away?
                if have == mapping['mappings']:
                    app.info('Index already existed', idx=index)
                    return

                try:
                    m, s = 'mappings', 'symmetric'
                    jd = jsondiff.diff(have, mapping[m], syntax=s, marshal=True)
                    msg = 'Index not optimized'
                    return app.warn(
                        msg,
                        idx=index,
                        diff=jd,
                        possible_prob=[
                            'values might be missing in dashboards',
                            'diskspace',
                        ],
                        hint=[
                            'reload index in elastic mgmt dashboard',
                            'adjust parameter types (e.g. from long to byte)',
                        ],
                    )
                except Exception as ex:
                    return app.error('Could not deserialize mapping diffs', err=ex)

            app.error('Tried create index. Got', **res)
            time.sleep(1)

    @classmethod
    def delete_index(cls, index):
        app.warn('Deleting index', index=index)
        cls._connect()
        r = cls.con.indices.delete(index=index, ignore=[400, 404])
        if not r.get('acknowledged') and r.get('status') not in [400, 404]:
            app.error('Could not delete index', index=index)
        return r

    @classmethod
    def snk(cls, index=None, idx_at=None, alias=None, timespan=1, count=1, is_rx=True):
        """
        Full message forwarder, using streaming_bulk.

        timespan, count: buffer_with_time_or_count params (seconds, items)
        When idx_at is set, e.g. 'foo.bar.baz' we take the idx value from
        data['foo]['bar']['baz']
        """
        cls.setup()
        sig = dict(locals())

        def buffered_send(index=index, sig=sig, cls=cls):
            snd = partial(send, index=index, cls=cls)
            ts, c = sig['timespan'], sig['count']
            return rx.buffer_with_time_or_count(ts, c), rx_debuffer(snd)

        def get_idx_val(d, index=index, idx_at=idx_at, cls=cls):
            di = index if not index is None else cls.default_index
            i = di if not idx_at else get_deep(idx_at, d['payload'], dflt=di)
            return cls.index_prefix + i

        def per_idx(s, cls=cls, alias=alias):
            cls._connect()
            cls._make_index(s.key, alias)
            return s.pipe(*buffered_send(s.key))

        f = rx.pipe(rx.group_by(get_idx_val), rx.flat_map(per_idx))

        return f


def send(msgs, index=None, cls=None):
    docs = to_es_flat_data_dicts(msgs, cls.getters)
    l = helpers.streaming_bulk(cls.con, docs, index=index, chunk_size=len(msgs))
    for ok, result in l:
        action, result = result.popitem()
        if ok is not True:
            app.error('Failure', **result)


def to_es_flat_data_dicts(docs, getters):
    rs = []

    for r in docs:
        r = r['payload']
        m = []
        for k, g in getters:
            try:
                m.append((k, g(r)))
            except Exception as ex:
                print('breakpoint set in to_es_flat_data_dicts')
                breakpoint()
                keep_ctx = True
        m = dict([(k, v) for k, v in m if v is not None])
        rs.append(m)
    return rs


def make_mapping(Def):
    """
    This replaces the attribute definition tuples of a Def class with real
    value getters, so items get be produced later.
    Also it returns an elastic search mapping for the types.

    Keyword Behaviour:
    https://www.elastic.co/blog/strings-are-dead-long-live-strings
    """
    mapping = {}
    Def._keys = [k for k in dir(Def) if not k.startswith('_')]

    for k in Def._keys:
        v = g(Def, k)
        if isinstance(v, str):
            v += ':str'
            v = [v]
        if len(v) == 1:
            v = v[0]
            v, typ = v.split(':')[:2]
            typ = str_types.get(typ, typ)
            default = None
        elif len(v) == 2:
            v, typ, default = v[0], v[1], None
        else:
            v, typ, default = v
        setattr(Def, k, getter(v, typ, default))
        es_typ = types.get(k) or types[typ]
        if es_typ == ES.Keyword:
            mapping[k] = {
                'type': 'text',
                'fields': {'keyword': {'type': 'keyword', 'ignore_above': 256}},
            }
        else:
            mapping[k] = es_typ().to_dict()

    return {
        # TODO: 1 -> len(hosts) ?
        'settings': {'number_of_shards': 1},
        'mappings': {'properties': mapping},
    }


def parse_attrs(cls, c=[0]):
    """Read in the default attribute definition of a project"""
    if c[0]:
        # mappings is modified while parsing, can only be parsed once!
        # -> now mappings do require restart!
        return c[0]

    attrs = g(cls, 'con_attributes', None)
    if attrs is None:
        app.die('No con_attributes for elastic connection class', name=cls.name)
    di = g(attrs, '_default_index', 'lc')
    mapping = make_mapping(attrs)
    rg_getters = [(k, g(attrs, k)) for k in attrs._keys]
    c[0] = di, mapping, rg_getters
    return c[0]
