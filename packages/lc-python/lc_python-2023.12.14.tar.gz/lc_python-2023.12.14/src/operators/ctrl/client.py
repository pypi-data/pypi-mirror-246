import os
import time
import traceback

import psutil
from devapp.app import FLG, app
from devapp.tools import api
from devapp.tools.lazy import LazyLoad
from rx import operators as rx

from operators.con import con
from operators.con.redis import redis

Lazy = LazyLoad()
Lazy.tracing = 'operators.tracing'

if os.environ.get('xxx'):
    # trick to get lazy loading AND gd in the editor
    from operators import tracing

    class Lazy(LazyLoad):
        tracing = tracing


class S:
    subscription = None
    channel: redis = None
    client_name = None


def type_not_supported(msg, **_):
    raise NotImplementedError('Call /help to get documentation')


def send_result(msg):
    """One shot - in pipeline"""
    S.channel.snk(msg['payload'], msg, name='ctrl')


class API:
    _doc_skip_params = ['msg', 'sid']

    def ops(msg, **_):
        return Lazy.tracing.operators()

    class trace:
        """Message Tracing"""

        def get(msg, **_):
            return Lazy.tracing.status()

        def status(msg, **_):
            return Lazy.tracing.status()

        def clear(msg, **_):
            """Clear ALL tracing"""
            return Lazy.tracing.clear_tracing()

        def stop(msg, sid, **_):
            """automatically called when a tracing client disconnects"""
            return Lazy.tracing.deactivate_tracing(sid=sid)

        def start(
            msg,
            sid,
            ops=[['type', 'eq', 'ax-src']],
            msgs=[[True]],
            clear=False,
            streaming=1,
            **_,
        ):
            """
            Switch on msg tracing

            🟥 This has perf impact, especially with expensive msg tracing.

            ## Params:

            - clear: Clears all existing tracing before applying this one

            - ops, msgs: filters

            ops: Filters ops to apply tracing for.
            msgs: Filters passing messages

            Allowed: pycond structures, plain text.
            Convention: ~foo is a substring search for foo in the stringified object (expensive)

            ## Example:

                http --stream post :2222/api/v1/trace/start clear=1 ops=~


            """
            t = Lazy.tracing
            if not t.S.channel_snk:
                t.S.channel_snk = S.channel.snk
            if clear:
                t.clear_tracing()
            t.S.header = msg['ctrl']
            return t.activate_tracing(ops, msgs, sid=sid)

    def status(msg, sid, **_):
        return {
            'status': 'alive',
            'rsc': {
                'sys': {
                    'mem': psutil.virtual_memory().percent,
                    'cpu': psutil.cpu_percent(),
                }
            },
            'meta': {
                'hubsck': msg['_ws'].hub_sck_name,
                'name': S.client_name,
                'pid': os.getpid(),
            },
        }


def validate(msg):
    p = msg['payload']
    try:
        return bool(p['sid'] and p['path'])
    except Exception:
        pass


def add_sid_to_msg(msg):
    p = msg['payload']
    sid = p['sid']
    # some jobs will result in data produced, matching the criteria of more than one job
    # we want to send those only once, marking here which jobs it matches
    # leaving to the client to pick his results, per job
    msg['ctrl'] = c = {'sid': {sid: p['path']}}
    c['hub_sck_name'] = msg['_ws'].hub_sck_name
    c['worker'] = S.client_name
    return msg


def run_job(s):
    while s.key.endswith('/'):
        s.key = s.key[:-1]
    p = s.key.split('/')
    spec = api.inspect_api(API)[s.key]['params']
    r = API
    while p:
        part = p.pop(0)
        r = getattr(r, part, 0)
        # if hasattr(r, 'lazyx'): lazy(r.lazy)
        if not r:
            r = type_not_supported
            break

    if isinstance(r, type):
        r = getattr(r, 'get', type_not_supported)

    def run(msg, f=r, spec=spec):
        p = msg['payload']
        q = p['query']
        q['sid'] = p['sid']
        try:
            if not spec.get('streaming'):
                msg['ctrl']['done'] = True
            res = f(msg, **q)
            if res:
                msg['payload'] = res
            return msg
        except Exception as ex:
            msg['ctrl']['done'] = True
            msg['ctrl']['err'] = e = {'msg': str(ex), 'exc': ex.__class__.__name__}
            if q.get('dbg'):
                e['tb'] = traceback.format_exc().splitlines()
            msg['payload'] = msg.get('payload', {})
            return msg

    return run


def pipeline():  # msgs are jobs here
    return (
        rx.filter(validate),
        rx.map(add_sid_to_msg),
        rx.group_by(lambda msg: msg['payload']['path']),
        rx.flat_map(lambda s: s.pipe(rx.map(run_job(s)))),
        rx.map(send_result),
    )


def subscribe_to_ctrl_broadcasts():
    if S.subscription:
        return
    S.channel = chan = getattr(con, 'redis', 0)
    if not chan:
        return app.warn(
            'No channel to send ctrl messages',
            hint='currently only con.redis supported - please define a redis connection named "redis"',
        )
    from node_red import nrclient

    S.client_name = f'{FLG.lc_client_name}@{nrclient.host}'
    S.subscription = nrclient.subj_cst.pipe(*pipeline()).subscribe(lambda _: 0)
