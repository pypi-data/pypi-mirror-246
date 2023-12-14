import msgpack
import pickle
import tempfile
from functools import partial

import confluent_kafka
import ujson as json
from devapp.app import app
from devapp.tools import to_list, wait_for_port, write_file, exists, os, has_tty
from operators.con.connections import con_params
from operators.ops.tools import rx_operator
from operators.con import proc


def cb_delivery(self, msg, topic=''):
    err = msg.error()
    if err:
        print(topic, str(err))
    else:
        print('kafka cb_delivery:', topic, len(str(msg.value())))


def cb_error(err, *a, **kw):
    print('error kafka', str(err))


def kafka_config(d):
    m = {k[2:]: v for k, v in d.items() if k[:2] == 'c.'}
    return m


reader_exe = 'lib:proc_kafka_consume.py'

# fmt:off
con_defaults = {
    'c.log.connection.close' : False,
    'c.sasl.mechanisms'      : 'PLAIN',
    'c.sasl.password'        : '$password',
    'c.sasl.username'        : 'axtract',
    'c.security.protocol'    : 'sasl_plaintext',
    # if you want more, configure kafka://?c.bootstrap.servers=1.1.1.1:9092,...
    # kafka lib can swallow comma seped hostports
    'c.bootstrap.servers'    : ('127.0.0.1:9092', '%(hostname)s:%(port)s'),
}

con_dflts_src = sr = dict(con_defaults)
con_dflts_snk = sn = dict(con_defaults)

sr['c.group.id']                    = 'axtract'
sr['topics']                        = ['readings']
sr['c.session.timeout.ms']          = 6000
sr['ext.stream_reader.cmd']         = reader_exe
sr['ext.stream_reader.ser']         = 'content_length:0:20'
sr['ext.stream_reader.oneshot']     = False
sr['ext.stream_reader.cfg.del_cfg'] = True

sn['topic']                    = 'results'
sn['enc']                      = 'pickle-2'
sn['c.queue.buffering.max.ms'] = 100

# fmt:on


class kafka:
    name = 'kafka'
    url = 'http://127.0.0.1:9092'
    con_defaults = con_defaults
    con_dflts_src = con_dflts_src
    con_dflts_snk = con_dflts_snk

    @classmethod
    def src(cls, observer, group_id=None, topics=None, password=None):
        """
        name is group.id
        We go subproc, since rrdkafka does block gevent

        password is here to allow supplying sasl.password within config from --env_var
        """
        d = con_params(cls, defaults=cls.con_dflts_src)
        # easy way to debug:
        kafka_debug = os.environ.get('lc_kafka_mock', '')
        if kafka_debug:
            try:
                fn, count, dt = kafka_debug.split(':')[:3]
                count, dt = int(count), float(dt)
                assert exists(fn) or print(f'Not exists: {fn}') or 1 / 0
            except Exception:
                app.die('Could not deserialize $lc_kafka_mock which is set')
            d['ext.stream_reader.cfg.test_msg_fn'] = fn
            d['ext.stream_reader.cfg.del_cfg'] = False
            d['ext.stream_reader.cfg.test_msg_count'] = count
            d['ext.stream_reader.cfg.test_msg_dt'] = dt
        if topics:
            d['topics'] = to_list(topics)
        if group_id:
            d['c.group.id'] = group_id
        # we write the config to a tmpfile and only hand the filename over. security risk though
        temp = tempfile.NamedTemporaryFile(delete=False)  # proc consume will delete
        write_file(temp.name, json.dumps(d))
        temp.close()
        pref = 'ext.stream_reader.'
        p = {k[len(pref) :]: v for k, v in d.items() if k.startswith(pref)}

        sp = p.get('cmd') or reader_exe
        if sp.startswith('lib:'):
            p['cmd'] = __file__.rsplit('/', 1)[0] + '/' + sp[4:]
        p['args'] = [temp.name]
        r = proc.proc.src(observer, cmd=p)
        return r

    @classmethod
    def snk(cls, key='{d[id]}', topic=None, cfg=None, enc=None, is_rx=True):
        """
        Simple full message forwarder.

        Can be used as operator as well.

        enc SHOULD be defined in the connector, not in NR
        """
        d = con_params(cls, defaults=cls.con_dflts_snk)
        if cfg:
            d.update(cfg)
        if topic:
            d['topic'] = topic
        if d['enc'] == 'auto':
            d['enc'] = 'pickle-2'
        if enc is not None:  # from Node RED
            d['enc'] = enc
        enc = d['enc']
        topic = d['topic']
        con = [0]
        cb = partial(cb_delivery, topic=topic)

        def setup(config=kafka_config(d)):
            if has_tty:
                # avoid output error msg spamming when de[v/bugg]ing w/o kafka
                hp = to_list(config['bootstrap.servers'])[0].split(':', 1)
                _ = 'Kafka Sink'
                if not wait_for_port(int(hp[1]), hp[0], timeout=0.5, log_err=_):
                    return app.error('talking kafka offline'.upper())

            con[0] = confluent_kafka.Producer(config)

        def s(data, msg, key=key, enc=enc, topic=topic, cb=cb, con=con):
            return send(data, msg, key, enc, topic, cb, con)

        def disconnect(con=con):
            # never happens
            return

        def _snd(data, msg, cfg=cfg):
            return send(data, msg, **cfg)

        return rx_operator(on_subscription=setup, on_next=s, on_completed=disconnect)


def send(data, msg, key, enc, topic, cb, con):
    try:
        keyv = key.format(d=data, m=msg)
    except Exception as ex:
        app.error('bogus data in kafka send', exc=ex)
        return

    # TODO: unsure what kakfa does, for now this
    if enc == 'pickle-2':
        v = pickle.dumps(data, 2)
    elif enc == 'msgpack':
        v = msgpack.packb(data, use_bin_type=True, default=str)
    else:
        raise Exception('We support only pickle-2 in kafka')
    con[0].produce(topic=topic, value=v, key=keyv, on_delivery=cb)
    # TODO: Is this efficient?
    con[0].poll(timeout=0.0)
