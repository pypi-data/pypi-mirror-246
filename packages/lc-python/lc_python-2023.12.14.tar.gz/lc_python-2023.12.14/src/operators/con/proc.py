import json
import pickle
import msgpack
import os
import time
from subprocess import PIPE, Popen, call

from devapp.app import app
from operators.con.connections import con_params
from operators.const import stop  # , sources
from operators.ops.exceptions import Err, OpArgParseError

desers = [('json', json.loads), ('plain', lambda x: x.rstrip())]
deser_dict = dict(desers)

# Making the subproc die, even when the parent is killed with -9 (sigkill).
# Tested this with proc_kafka, spawned in a greenlet via Popen, worked.
# NOTE: No effect when killing the WRAPPER proc with -9 (e.g. bin/client)
try:
    # in order to implant bombs into our subprocs:
    import ctypes
    from ctypes.util import find_library

    LIBC = ctypes.CDLL(find_library('c'))
except:
    LIBC = None

PR_SET_PDEATHSIG = 1


def implant_bomb():
    return LIBC.prctl(PR_SET_PDEATHSIG, 9)


def communicate(cls, data, msg, host, port):
    breakpoint()  # FIXME BREAKPOINT
    pass


def oneshot(cfg, cls):
    pcmd = cfg['pcmd']
    app.info('Starting subproc in foreground', cmd=cfg['cmd'])
    if cfg.get('debug_fg'):
        app.warn('Starting subproc in debug mode', cmd=pcmd)
        ec = call(pcmd, shell=cfg['shell'])
        return 'None [ran in debug mode]', os.getpid()
    else:
        r = Popen(pcmd, shell=cfg['shell'], stdout=PIPE)
        return r.communicate()[0], r.pid


def producer_process(cfg, observer, cls):
    """continuously producing process"""

    def produce(popen_kw, iter_output, cfg=cfg):
        if LIBC:
            popen_kw['preexec_fn'] = implant_bomb
        with Popen(**popen_kw) as p:
            # called at unsub (build.py):
            def stopping(pid=p.pid):
                os.kill(pid, 15)

            d = {'name': 'process %s [%s]' % (cfg['cmd'], p.pid), 'func': stopping}
            stop.append(d)
            iter_output(p)

    cmd, shell, ser = cfg['pcmd'], cfg['shell'], cfg['ser']
    kw = dict(args=cmd, stdout=PIPE, shell=shell)

    # TODO: lz4 compressed data
    desers = [
        ['msgpack', msgpack.unpackb],
        ['pickle', pickle.loads],
        ['json', json.loads],
    ]

    def find_deser(raw, desers=desers, kw=kw):
        """find serialization format by trying"""
        for ser, df in desers:
            try:
                res = df(raw)
                app.info('Deserializer fixed', kw=kw, using=ser)
                return ser, res, df
            except Exception:
                continue

    # Safest option. Serialization autodetected:
    if ser.startswith('content_length'):

        def iter_output(p, observer=observer, kw=kw, ser=ser):
            L = int(ser.split(':')[-1])  # length of header
            rcv = p.stdout.read
            df = None
            while True:
                hdr = rcv(L)  # e.g. "myeader:0:421231      " for L=25
                if not hdr:
                    # systemd restart needed, we can't recover from this
                    return app.die('Producer process died', kw=kw)
                body = rcv(int(hdr.split(b':')[-1]))
                if df is None:
                    # first msg:
                    err = None
                    try:
                        l = [k for k in desers if k[0] in hdr.decode('utf-8')]
                        if len(l) == 1:
                            ser, df = l[0], l[1]
                            res = df(body)
                        elif len(l) == 0:
                            found = find_deser(body)
                            if not found:
                                err = 'Unknown message format'
                            ser, res, df = found
                        else:
                            err = 'Deserialization error'
                        if err:
                            raise Exception(err)
                    except Exception as ex:
                        app.die('First package deser error', src='proc', kw=kw, exc=ex)

                else:
                    # hot path:
                    try:
                        res = df(body)
                    except Exception as ex:
                        app.error('Deserialization error', src='proc', ex=str(ex), kw=kw)
                        continue
                observer.on_next((res, (p.pid,)))
                time.sleep(0)

    elif ser in {i[0] for i in desers} or ser == 'auto':

        def iter_output(p, observer=observer, kw=kw, desers=desers, ser=ser):
            # we try to autodetect input serialization, assuming lineseps . Have e.g. kafka pickles and msgpacks
            # CAUTION: don't do this, use content_length, unless you actually have to, lineseps are in payload as well
            if ser == 'auto':
                raw, res = b'', None
                # msgpack, pickle have '\n'. So we have to do fragments:
                for byte_line in iter(p.stdout.readline, b''):
                    raw += byte_line
                    found = find_deser(raw)
                    if not found:
                        continue
                    ser, res, df = found
                    break
                observer.on_next((res, (p.pid,)))
                time.sleep(0)
            else:
                df = [i[1] for i in desers if i[0] == ser]

            raw = b''
            for byte_line in iter(p.stdout.readline, b''):
                raw += byte_line
                try:
                    res = df(raw)
                except Exception:
                    if len(raw) > 10000000:
                        # this won't recover, we are in the middle :-(
                        # can only protect memory
                        _ = 'Unrecoverable Deserialization Problem'
                        app.error(_, kw=kw, using=ser)
                        raw = b''
                    continue
                observer.on_next((res, (p.pid,)))
                time.sleep(0)
                raw = b''

    else:
        kw.update(dict(bufsize=1, universal_newlines=True))

        def iter_output(p, observer=observer):
            for line in p.stdout:
                push_result(line, p.pid, cfg, observer)
                time.sleep(0)

    produce(kw, iter_output)


def subproc_in(cls, observer, cmd):
    """
    ser = auto: if first line can be jsoned we use that from now on, else plain
    """
    d = con_params(cls)
    if isinstance(cmd, dict):
        d.update(cmd)
    elif isinstance(cmd, str):
        if not d.get('shell'):  # shell needs a string
            l = cmd.split(' ')
            d['cmd'] = l[0]
            d['args'] = l[1:]
    elif isinstance(cmd, list):
        d['cmd'] = cmd[0]
        d['args'] = cmd[1:]
    else:
        msg = 'cmd format error'
        raise OpArgParseError(msg, cmd=cmd)
    if d.get('debug_fg'):
        d['oneshot'] = True
    d['pcmd'] = [d['cmd']]
    d['pcmd'].extend(d['args'])
    if d['shell']:
        d['pcmd'] = ' '.join(d['pcmd'])
    t0 = time.time()
    if d['oneshot']:
        r, pid = oneshot(d, cls)
        push_result(r, pid, d, observer)
    else:
        producer_process(d, observer, cls)

    app.info('Process completed', cmd=d['cmd'], dt=round(time.time() - t0, 2))
    observer.on_completed()


def push_result(res, pid, cfg, observer):
    ds = cfg.get('deserializer')
    have_deser = False
    if not ds:
        ser = cfg['ser']
        if ser == 'auto':
            for k, f in desers:
                try:
                    res = f(res)
                    cfg['deserializer'] = f
                    have_deser = True
                except Exception:
                    pass
        else:
            try:
                ds = deser_dict[ser]
            except Exception:
                msg = Err.func_parametrize_error
                raise OpArgParseError(msg, ser=ser)

    if not have_deser:
        try:
            res = ds(res)
        except Exception as ex:
            app.error('proc.src line error', line=res[:100], cmd=cfg['cmd'], exc=ex)
            return
    observer.on_next((res, (pid,)))


def subproc_out(cls, data, msg):
    breakpoint()  # FIXME BREAKPOINT


class proc:
    name = 'proc'

    class con_defaults:
        cmd = '/bin/cat'
        args = ['/etc/hosts']
        shell = False
        oneshot = True
        ser = 'auto'
        debug_fg = False

    url = 'proc://localhost'

    src = classmethod(subproc_in)
    com = classmethod(communicate)
    snk = classmethod(subproc_out)
