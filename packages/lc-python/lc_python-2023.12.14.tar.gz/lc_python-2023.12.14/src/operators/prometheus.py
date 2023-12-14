from devapp.app import app, FLG

from prometheus_client import Counter, registry
from operators.const import tab_label
from devapp.tools import process_instance_offset
import time


def with_metrics(name, f, op):
    c_dt, c_cnt, c_err = make_counters(name, op)
    if not c_dt:
        return f

    def counted_f(*a, f=f, c_dt=c_dt, c_cnt=c_cnt, now=time.time, **kw):
        t0 = now()
        r = f(*a, **kw)
        dt = now() - t0
        # c_dt.inc(int(dt * 1000000))
        c_cnt.inc()
        return r

    return counted_f


def err_total(c=[0]):
    if c[0]:
        return c[0]
    c[0] = Counter('err_total', 'Err_Total')
    return c[0]


def make_counters(name, op, suff=None, dt_unit='micros', _have={}):
    """Run at every pipeline build, for all ops
    To avoid re-reg errors at rebuild we keep our own registry (_have)
    since the full names for those counters within prom.registry seem to be not public i.e. stable(?)
    """
    # virtual ops have tuples as id (e.g. nr_out)
    if not op.get('metrics_count', FLG.metrics_collect) or not isinstance(op['id'], str):
        return None, None, None

    suff = '_' + (op['id'].replace('.', '_') if suff is None else suff)
    have_metrics[0] += 1
    while not host[1]:
        time.sleep(0.01)
    tn = tab_label(op['z'])
    if '.' in name:
        subsystem, N = name.rsplit('.', 1)
    else:
        subsystem, N = '', name
    subsystem = subsystem.replace('.', '_')
    # we add id in case of name collisions:
    n = N + suff
    cnts = ()
    instance = f'%s.%s.%s' % (host[0], sys.argv[1], host[1])
    for k1, v1, u in [['', '', dt_unit], ['', '', 'msgs'], ['', '', 'errors']]:
        # reg = f'{n}.{k1}.{v1}.{u}'
        reg = u
        C = _have.get(reg)
        if not C:
            ckw = dict(
                name=u,
                documentation=u.capitalize(),
                labelnames=['function', 'flows', 'instance'],  # , 'pid'],
                unit=u,
            )
            C = Counter(**ckw)
            _have[reg] = C
            app.debug(f'Registered counter {C._name}')
        C = C.labels(function=name, flows=tn, instance=instance)   # , pid=os.getpid())
        cnts += (C,)

    return cnts


have_metrics = [0]

import socket, sys, os

host = [socket.gethostname(), 0]


def start_prometheus_server(c=[0]):
    if c[0]:
        return app.debug('prometheus already started', host_port=c[0])
    hp = FLG.metrics_prometheus_listener
    if not hp:
        return app.info('No prometheus listener configured')

    if not FLG.metrics_collect:
        return app.debug('No metrics configured')
    # if not have_metrics[0]:
    #     return app.debug('No metrics configured')
    from prometheus_client import start_http_server

    h, p = hp.split(':')
    p = process_instance_offset(int(p))

    for i in range(100):
        try:
            start_http_server(port=p, addr=h)
            c[0] = [h, p]
            host[1] = p
            return app.info('Started prometheus server', host_port=c[0])
        except Exception as ex:
            # should not happen, with instance
            app.warn('Prometheus port %s occupied - counting up' % p, port=p, err=ex)
            p += 1
