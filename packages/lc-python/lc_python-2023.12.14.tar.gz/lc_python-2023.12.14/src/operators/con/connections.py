from devapp.app import FLG, app
from devapp.tools import define_flags, to_list, process_instance_offset
from tree_builder import links
from operator import setitem

have = {}
g = getattr


class con:
    """
    Named Connection Classes

    Populated with named con class dubs via add_connection(container class, *names)
    """


# ======================================================== app startup (pre flag define)


def dub(n, defaults, cls):
    """defaults e.g. 'con_defaults'"""

    # clone the defaults, so that we change:
    if isinstance(defaults, str):
        d = g(cls, defaults)
        if isinstance(d, type):
            d = type(defaults, (d,), {})
        else:
            d = dict(d)
    c = type(n, (cls,), {'name': n})
    setattr(c, defaults, d)
    return c


def add_connection(cls, *names, defaults='con_defaults', req_conf=False, **kw):
    """
    Called at product start, for the various connections offered

    - Creates named copies(dubs) of con classes
    - Creates flags to parametrize their URLs
    """
    if not names:
        names = (cls.__name__,)

    c = have.setdefault(cls, {})
    for n in names:
        if n in c:
            d = c[n]
            continue
        d = c[n] = dub(n, defaults, cls)
        dfl = g(d, defaults, None)
        if dfl:
            f = setattr if isinstance(dfl, type) else setitem
            [f(dfl, k, v) for k, v in kw.items()]
        setattr(con, n, d)
        d._require_configured = req_conf
        define_flags_for_dubbed_con_cls(n, cls, defaults)
    # return typically only needed by tests, in prod we get the classes from the
    # pipeline
    # typically only one, return it:
    return d if len(c) == 1 else c


# -------------------------------------------------------------------- app startup tools
def host(d):
    return d.get('host', d.get('hostname', '127.0.0.1'))


def get_or_make_url(cls, defaults):
    """what is the default for the url flag value"""
    # if given that that's it:
    u = g(cls, 'url', None)
    if u:
        return u
    d = dflts_from_type_or_dict(cls, defaults)
    cls.url = '%s://%s' % (cls.__name__, host(d))
    return cls.url


def url_flg(N, n, cls, defaults):
    v = get_or_make_url(cls, defaults)
    return type(N, (object,), {'d': v, 'n': '%s: %s url' % (cls.__name__, n)})


def define_flags_for_dubbed_con_cls(n, cls, defaults):
    # N = 'redis_url' if n == 'redis'. N = redis_foo_url if n == 'foo':
    cn = cls.__name__
    flag_prefix = n
    N = flag_prefix + '_url'
    ns = '_'.join((n[0], 'u'))  # if cn in n else (cn[0], n[0], 'u'))
    f = url_flg(N, n, cls, defaults)
    # allow to say --main_redis_url=foo --main_redis_url=bar -> and we get a list
    if g(cls, 'multi_url', 0):
        f.t = 'multi_string'

    flg_props = {'autoshort': 'cu' + ns, '%s_url' % n: f}
    for k in dir(g(cls, '_instance_flags', object)):
        if k[0] == '_':
            continue
        v = g(cls._instance_flags, k)
        if isinstance(v, type):
            n = flag_prefix + '_' + k
            f = flg_props[n] = type(n, (v,), {})
            f.n = '%s: %s' % (cn, g(f, n, k))

    b = g(cls, '_flags', object)
    define_flags(type('flags_%s' % N, (b,), flg_props))


# ========================================================================= connect time
def strip_non_default_keys(cls, d, defaults):
    if 'host' in defaults:
        d['host'] = d['hostname']
    l = {k: d[k] for k in defaults if k in d and not k in defaults_control_keys}
    d.clear()
    d.update(l)


def replace_placeholders(d):
    d['path'] = d.get('path', '')
    for k, v in d.items():
        if isinstance(v, tuple) and len(v) == 2 and perc_brkt in str(v[1]):
            v = v[1] % d
            d[k] = v


def con_params_single_url(flg_url, cls, defaults):
    b = {}
    if dflt_val('_use', defaults):
        b = dict(defaults)
        b.update(con_params_dict(cls.url, defaults))  # when only url is given
    b.update(con_params_dict(flg_url, defaults))
    return b


def con_params_multi_url(flg_url, cls, defaults):
    b = []
    if dflt_val('_use', defaults):
        ul = to_list(cls.url)
        b = [dict(defaults) for i in range(len(ul))]
        c = [con_params_dict(u, defaults) for u in ul]
        [i.update(j) for i, j in zip(b, c)]

    b = b[: len(flg_url)]
    b.extend([{} for k in range(len(flg_url) - len(b))])
    u = [con_params_dict(u, defaults) for u in flg_url]
    [i.update(k) for i, k in zip(b, u)]
    return b


def con_params_dict(url, defaults):
    if isinstance(url, str):
        url = links.parse_via(url, cast=dflt_val('_cast', defaults))
    elif not isinstance(url, dict):
        app.die('url format error, expected dict', url=url)
    url = dict(url)
    return url


defaults_control_keys = {'_strip_non_default_keys': True, '_use': True, '_cast': True}


def dflt_val(k, defaults):
    return defaults.get(k, defaults_control_keys[k])


def dflts_from_type_or_dict(cls, defaults):
    """defaults either dict (kafka) or type (redis) or string pointing to those"""
    d = defaults
    if not d:
        d = {}
    elif isinstance(d, str):
        d = g(cls, d)
    if isinstance(d, type):
        d = {k: g(d, k) for k in dir(d) if k[0] != '_' or k in defaults_control_keys}
    return d


# --------------------------------------------------------------------------- Public API


def con_params(cls, defaults='con_defaults', observer=None) -> dict:
    """
    Called at Runtime, delivering the params for a connections

    A connection class, i.e. with an .url attribute wants to know it's settings

    Returns dict with conn settings or a list of those (url like '["http://..", "..."]')

    """
    defaults = dflts_from_type_or_dict(cls, defaults)
    url = g(FLG, '%s_url' % cls.name, cls.url)
    if g(cls, '_require_configured', 0):
        if url == cls.url:
            app.warn('Unconfigured - skipping', con=cls.__name__)
            if observer:
                observer.on_completed()
            return
    f = con_params_multi_url if g(cls, 'multi_url', 0) else con_params_single_url
    r: dict = f(url, cls, defaults)
    rl = to_list(r)
    [replace_placeholders(i) for i in rl]
    if dflt_val('_strip_non_default_keys', defaults):
        for d in to_list(r):
            strip_non_default_keys(cls, d, defaults)
    if isinstance(r, dict) and r.get('port_incr_instance') and 'port' in r:
        r['port'] = process_instance_offset(int(r['port']))
    return r


perc_brkt = '%('
