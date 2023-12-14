"""
Message Tracing

🟣 $HOME/repos/ax/devapps/lc-python/docs/dev/devnotes/tracing.md
"""
import time
import pycond as pc
from devapp.app import FLG, app
from devapp.tools import clean_env_key, define_flags, exists, os, project

from operators.const import ax_pipelines
from operators.dec_enc import encode_payload
from operators.con.redis import redis

now = time.time


class S:
    filters_by_opid = {}
    send_result = None
    channel_snk: redis.snk = None
    header: dict = None


def make_tracer(op):
    key = '-'.join(
        [
            k[0] + ':' + str(op.get(k))
            for k in ['z', 'type', 'label', 'name', 'id']
            if op.get(k)
        ]
    )
    key = clean_env_key(key, '_-. :')

    def trace_msg(msg, filters=S.filters_by_opid.get(op['id'], {}).items(), key=key):  # noqa
        sids = {}
        for sid, v in filters:
            try:
                v['hits'][0] += 1
                # TODO: ident check and set, we have that info in v
                if v['filterfunc'](state=msg['payload']):
                    sids[sid] = True
                    v['hits'][1] += 1
            except Exception:
                pass
        if sids:
            p = {str(now()) + '::' + key: msg['payload']}
            msg = {'_ids': msg['_ids'], 'ctrl': S.header, 'ctrl.subs': sids, 'payload': p}
            S.channel_snk(p, msg, name='ctrl')

    return trace_msg


def make_filter(f):
    if isinstance(f, str):
        if not f:
            f = 'true'  # all
        if f[0] == '~':
            app.warn('Got performance intensive trace rule', rule=f)
            return f, lambda state, f=f[1:]: f in str(state)
        f = pc.to_struct(pc.tokenize(f, brkts='()'))
    return f, pc.parse_cond(f)[0]


def deact(opid):
    # add outs has NR sending and trace. we remove the latter
    r = ax_pipelines['add_outs'].get(opid)
    if r:
        r.pop('trace', 0)
        if not r:
            ax_pipelines['add_outs'].pop(opid)


def operators():
    return ax_pipelines['ops']


def status():
    jobs = set()
    r = {}
    f = dict(S.filters_by_opid)
    for id, rules in f.items():
        r[id] = m = {}
        for sid, v in rules.items():
            v = dict(v)
            v.pop('filterfunc')
            m[sid] = v
            jobs.add(sid)
    r['jobs'] = list(jobs)
    return r

    return {'hi': 23}
    breakpoint()  # FIXME BREAKPOINT


def clear_tracing():
    ops = list(ax_pipelines['add_outs'].keys())
    [deact(id) for id in ops]
    S.filters_by_opid.clear()
    app.info('cleared tracing')
    return {'cleared_tracing': status()}


def deactivate_tracing(sid):
    f = S.filters_by_opid
    [tr.pop(sid, 0) for _, tr in f.items()]
    l = [deact(k) for k, v in f.items() if not v]
    [f.pop(i) for i in l]
    app.debug('left trace rules', json=f)
    app.info('deactivated tracing', sid=sid)
    return {f'cleared_tracing for {sid}': status()}


def activate_tracing(opsfilter, msgsfilter, sid):
    """This can be called while runing, e.g. resulting from an API hit or a websock subs
    Default is to check the flag
    """
    AP = ax_pipelines
    opsfilter, opfilterfunc = make_filter(opsfilter)
    msgfilter, msgfilterfunc = make_filter(msgsfilter)

    ops = filter(lambda o: o.get('_is_py'), AP['ops'].values())
    ops = list([o for o in ops if opfilterfunc(state=o)])

    ao = AP['add_outs']
    m = {'filterfunc': msgfilterfunc, 'msgfilter': msgfilter, 'hits': [0, 0]}
    for op in ops:
        id = op['id']
        have = S.filters_by_opid.setdefault(id, {})
        for k, v in have.items():
            if v['msgfilter'] == msgfilter:
                v.setdefault('ident', set()).add(sid)
            m.setdefault('ident', set()).add(k)
        have[sid] = m
        ao.setdefault(id, {})['trace'] = make_tracer(op)
    app.debug('new trace rules', json=S.filters_by_opid)
    return {f'Activated_tracing for {sid}': status()}


# begin_archive
#
#
#
#
# class flags:
#     autoshort = 'tr'
#
#     class tracing:
#         class dest:
#             n = 'Where to send traces to. Must be connection name with a write_trace method. E.g. "redis"'
#             t = ['', 'files', 'f', 'redis', 'r']
#             d = ''
#
# define_flags(flags)

#
# S = [0, False, None]  # current number, activation state, tracer class
#
#
# def reset_counter():
#     S[0] = 0
#
#
# def activate(v: bool):
#     S[1] = v
#
#
# class files:
#     active = False
#     fn = 'tracefile'
#
#     def dir():
#         return project.root() + '/data/tracing'
#
#     def reset():
#         activate(False)
#         time.sleep(0)
#         reset_counter()
#         d = files.dir()
#         if exists(d):
#             for fn in os.listdir(d):
#                 os.unlink(d + '/' + fn)
#         # if exists(d): rmtree(d)
#         os.makedirs(d, exist_ok=True)
#
#     def make_tracer(op):
#         fn = '-'.join(
#             [
#                 k[0] + ':' + str(op.get(k))
#                 for k in ['z', 'type', 'label', 'name', 'id']
#                 if op.get(k)
#             ]
#         )
#         fn = clean_env_key(fn, '_-. :')
#
#         def trace_msg(msg, fn=fn, _bytes=[0], _fd=[0], _ls=b'\n'):
#             fd = _fd[0]
#             if not fd:
#                 fd = _fd[0] = open(files.dir() + '/' + fn, 'wb')
#             nr, act = S[:2]
#             if not act:
#                 return
#             S[0] = n = nr + 1
#             k = {'nr': n, 'ts': now(), 'msg': msg}
#             # 1.18s vs 3.2s with str(k) writes. and 10times smaller fs:
#             ks = encode_payload(k, enc='msgpack:lz4') + _ls
#             _bytes[0] += fd.write(ks)
#
#         return trace_msg
#
#
# tracing = {'f': files, 'files': files}
#
