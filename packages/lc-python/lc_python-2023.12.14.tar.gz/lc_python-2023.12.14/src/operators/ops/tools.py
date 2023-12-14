import importlib  # noqa
import time  # noqa
from copy import deepcopy  # noqa
from functools import partial as p  # noqa
from inspect import _empty, signature  # noqa
from json import loads, dumps  # noqa
import sys
import gevent
import rx as Rx
from devapp.app import app  # noqa
from operators.const import ax_pipelines
from operators.ops.exceptions import TimeoutError
from devapp.tools import write_file, os

# don't delete those imports, this is an import hub for others:
from operators.ops.funcs import (  # noqa
    Funcs,
    deserialize,
    find_func,
    funcs_from_package,
    funcs_pretty,
)
from rx import operators as rx  # noqa
from rx import subject

# noqa: https://github.com/myint/autoflake
from rx.scheduler.eventloop import GEventScheduler  # noqa

GS = GEventScheduler(gevent)


def clipboard(data, _cb=[0]):
    """data to clipboard - handy when run in foreground, locally. Otherwise consider ssh -X"""
    fn = '/tmp/lc-clip.json'
    data = dumps(data, indent=4, default=str)
    if sys.stdout.isatty():
        if not _cb[0]:
            if os.system('type pbcopy') == 0:
                _cb[0] = 'pbcopy'
            elif os.system('type xclip') == 0:
                _cb[0] = 'xclip -i -selection clipboard'
            elif os.system('wl-copy') == 0:
                _cb[0] = 'wl-copy'
        if _cb[0]:
            app.info('Using %s for clipboard' % _cb[0])
            os.system("""echo -e '%s' | %s""" % (data, _cb[0]))
            return
    _ = f'lacking xclip and pbcopy or a tty we write the clipboard to {fn}'
    app.warn(_)
    write_file(fn, data)


def raise_timeout(msg, op):
    raise TimeoutError(msg, op)  # adapted. sets .msg and .op into TimeoutError


def send_secondary(op, msg):
    """
    deliver sending function when op has a secondary nr out
    (determinded at build.py)
    """
    # FIXME: only port 0 currently => differentiate reg. port
    v = ax_pipelines['add_outs'].get(op['id'])
    if not v:
        return
    for k in v:
        if k == 'trace':
            v[k](msg)
        else:
            ax_pipelines['ext_out'](msg, op)


# def check(d):
#     while True:
#         import time

#         time.sleep(0.01)
#         if d.is_disposed:
#             breakpoint()  # FIXME BREAKPOINT


def rx_debuffer(msgs_side_effekt):
    """An rx operator which takes a function for handling msgs lists, e.g. from after
    rx.buffer_with ..., calls msgs_handler on them, then produces msg by msg again

    Currently we block while the msgs_handler is working

    """
    from operators.core import GS

    # TODO: understand an async=True sig param, then not blocking the stream
    # TODO: move to ax_core
    def debuffer(source, msgs_side_effekt=msgs_side_effekt):
        def subscribe(o, scheduler=GS):
            def _on_next(msgs=None):
                if not msgs:
                    return
                msgs_side_effekt(msgs)
                for msg in msgs:
                    o.on_next(msg)

            return source.subscribe(_on_next, o.on_error, o.on_completed, scheduler)

        return Rx.create(subscribe)

    return debuffer


from functools import partial


def rx_operator(on_next, on_completed=None, on_error=None, on_subscription=None):
    """
    Helper to conveniently define custom rx ops, by just providing any of the three funcs.
    Run on subscription to the pipeline, i.e. (long?) after setup.
    """

    def _setup(
        source,
        on_subs=on_subscription,
        on_next=on_next,
        on_completed=on_completed,
        on_error=on_error,
    ):
        def subscribe(o, scheduler=None, on_next=on_next):
            # this allows on_next to produce many messages:
            on_next_wants_observer = False
            if 'observer' in signature(on_next).parameters:
                on_next = partial(on_next, observer=o)
                on_next_wants_observer = True

            if on_subs:
                on_subs()

            def _on_next(msg=None):
                pl = msg['payload']
                r = on_next(pl, msg=msg)
                if on_next_wants_observer:
                    return
                if r is None:
                    r = pl
                msg['payload'] = r
                o.on_next(msg)

            d = source.subscribe(
                _on_next,
                on_error or o.on_error,
                on_completed or o.on_completed,
                scheduler,
            )
            return d

        return Rx.create(subscribe)

    return _setup


class NamedSubject(subject.Subject):
    def __init__(self, name):
        self.name = name
        super(NamedSubject, self).__init__()

    def __repr__(self):
        return 'Subject[%s]' % self.name


def deep_copy(msg):
    """Required whenever we share"""
    msg = dict(msg)
    msg['payload'] = deepcopy(msg['payload'])
    return msg


def share_at(op, deep_cp=False):
    """Required whenever we share"""

    def d(msg, op=op, deep_cp=deep_cp):
        if deep_cp:
            msg = deep_copy(msg)
            msg.setdefault('copied', []).append(op['id'])
        else:
            # shallow copy, ids must remain unique, also tracing infos
            msg = dict(msg)
            s = 'fwd' if deep_cp is None else 'shared'
            l = msg[s] = msg.get(s) or []
            l.append(op['id'])
        return msg

    return d


def now():
    return int(time.time() * 1000)


nr = [0]


def msg_id(last=[0]):
    n = now()
    if n == last[0]:
        nr[0] += 1
    else:
        last[0] = n
        nr[0] = 0
    return n, 'py.%s.%s' % (n, nr[0])


# from operators.caches import process_cache

# TODO: have this tuneable:
# cache = process_cache()


def as_msg(payload, f, op):
    """
    Converting src data to our message format, this is the first function after a src.
    If payload is a tuple we treat the second item as meta info

    NOTE: payload might actually be the full msg - we return that, then.
    """
    src_nfo, got_msg = None, None
    if isinstance(payload, tuple) and len(payload) == 2:
        # allowing e.g. socketholders to pass that with the msg:
        payload, src_nfo = payload
    elif isinstance(payload, dict) and payload.get('payload') is not None:
        # already in msg format (e.g. from node red)
        if payload.get('_ids'):
            # payload already a complete msg
            return payload
        got_msg = payload

    t, id = msg_id()
    ids = {'flw': op['id'], 'msg': id}
    msg = {
        # fmt:off
        'ts': t,
        '_ids': ids,
        'type': 'msg',
        'op': op['id'],
        'created': True,
        'func': [op['name']],
        'payload': payload,
        # fmt:on
    }
    if src_nfo:
        msg.setdefault('objs', {})['src'] = src_nfo
    if got_msg:
        msg.update(got_msg)
    return msg
