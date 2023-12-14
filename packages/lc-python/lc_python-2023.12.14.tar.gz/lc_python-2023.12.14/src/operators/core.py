import time
import sys
from devapp import gevent_patched as gevent_patched
from operators.prometheus import make_counters
import gevent
from ax.utils.ax_tree.ax_tree import AXTree
from devapp.app import app
from node_red.tools import jp, js
from operators.const import ax_pipelines
from operators.dec_enc import decode_msg, encode_msg, encode_payload
from operators.kv_tools import kv, schemadict
from operators.ops.tools import NamedSubject, Rx, rx, clipboard
from operators.con.file import file
from operators.src import hello_server, interval

# from operators.http import http
# from operators.sock import sock
# from operators.proc import proc
# from operators.redis import redis
from pycond import parse_cond
from rx.scheduler.eventloop import GEventScheduler
from structlogging.sl import AppLogLevel

GS = GEventScheduler(gevent)

# class LazyImported(object):
#     """
#     Those just dont get their inner namespace explored when building funcs_from_package
#     TODO: advantage?
#     """

#     mod, cls = None, None

#     def __init__(self, mod, cls):
#         self.nmod = mod
#         self.ncls = cls

#     def __call__(self):
#         if not self.mod:
#             self.mod = import_module(self.nmod)
#             self.cls = getattr(self.mod, self.ncls)
#         return self.cls

#     def __getattr__(self, k, dflt=None):
#         breakpoint()  # FIXME BREAKPOINT
#         c = self()
#         return getattr(c, k)

#     def is_gevent_monkey_patched():
#         # TODO: why is this here?
#         try:
#             from gevent import monkey
#         except ImportError:
#             return False
#         else:
#             return monkey.is_module_patched('__builtin__')

from threading import current_thread


class ax_core_ops:
    """
    Namespace ax.

    Present always (no need to explicitly expose in funcs)
    """

    get = kv.get
    set = kv.set
    update = kv.update
    file_read = file.read

    def rate(data, msg, op, dt=1, on_stdout=False, _c=[0]):  # noqa: B006
        now = time.time()
        r = _c[0]
        if not r:
            r = _c[0] = [op.get('label', op['id']), now, 0]
        r[2] += 1
        if now - r[1] > dt:
            R = r[2] / (now - r[1])
            msg[f'rate_{r[0]}'] = R
            if on_stdout:
                print(f'Rate@{r[0]}: {r[2]} / sec. Msg {len(str(data))} b')
            r[1] = now
            r[2] = 0
        return data

    def count(data, msg, op, _c=[0], now=time.time):  # noqa: B006
        r = _c[0]
        if not r:
            n = op.get('label') or op.get('name')
            r = _c[0] = make_counters(n, op, dt_unit='millis')
        try:
            dt = int(now() * 1000) - msg['ts']
        except Exception:
            return app.error('No message timestamp', **msg)
        r[0].inc(dt)
        r[1].inc()

    def add_conf(data, deep=False, **kw):
        """a default to add configuration infos, e.g. wifi dispatcher's reg domain"""
        return ax_core_ops.update(
            data,
            msg={},
            pth=[
                'conf',
            ],
            deep=deep,
            create=True,
            **kw,
        )

    def brk(data, msg, op):
        """breakpoint for interactive inspection"""
        if sys.stdin.isatty() and sys.stdout.isatty():
            try:
                app.warn('Hit breakpoint', payload=data)
            except Exception as _:
                app.warn('Could not print payload', len=len(data))
            # guys need to see WHICH bp is hit right now
            l = f'ax.brk at: tab {op["z"]} op: {op.get("label", op)}'
            app.warn('Inspect than continue with c', at_=l)
            breakpoint()  # FIXME BREAKPOINT
        else:
            app.info('ignoring inspect_interactive - no tty')
        return data

    def dump(data, msg, op, level=20, truncate=None, full_msg=False, schema=False):
        r = msg if full_msg else data
        label = op.get('label', 'ax.dump')
        with AppLogLevel(level):
            if schema:
                r = schemadict(r)
            if truncate:
                d = str(r)
                app.info(f'Data dump [{label}]', data=d[:truncate] + '...', chars=len(d))
            else:
                app.info(f'Data dump [{label}]', payload=r)
        return data

    def set_log(data, msg, key='{d[id]}', **kw):
        """Setting the logger  name to a dynamic key, per msg

        In the logger we'll dig up for the name.

        Py3's contextvars are no solution, won't see a gevent.spawn
        """

        try:
            keyv = key.format(d=data, m=msg)
        except Exception as ex:
            return

        # The attr is seen by logger. fast. 0.0002 for 1000
        # id: So that at async ops (spawned by hub via rx and not this greenlet, ops.py) we have it still (no parent check possible then)
        msg['_ids']['log'] = gevent.getcurrent().logger_name = keyv

    def sleep(data, msg, sec=0):
        """Sleep for given number of secs. May be dynamic (e.g.: {d[block_sec]}).

        Note: This will block the stream => Configure as async in NR, giving up order!
        """
        try:
            sec = float(sec.format(d=data, m=msg))
        except Exception as ex:
            pass
        if sec > 0:
            sec = float(sec)
            app.info('Sleeping', sec=sec)
            time.sleep(sec)

    def hello(
        data, msg, name='world', tag=None, count_start=0, hello_traversed_total=[0]
    ):
        """test operator"""
        if not isinstance(data, dict):
            data = {'got': data}
        data['ax.hello operator says'] = 'Hello, %s!' % name
        tc = 'hello_traversed_count'
        data[tc] = data.get(tc, count_start) + 1
        hello_traversed_total[0] += 1
        data['hello_traversed_total'] = hello_traversed_total[0]
        if tag:
            data.setdefault('tags', []).append(tag)
        app.debug('ax.hello - logging msg', payload=msg)
        return data

    def push_to(data, msg, subj, c=[0], _subjs=[], **kw):
        s = c[0]
        if not s:
            d = ax_core_ops.src.named_subjects
            subj = [subj] if not isinstance(subj, list) else subj
            s = c[0] = [d[i].on_next for i in subj]
            _subjs.extend(subj)
        app.info('push_to', subjs=_subjs)
        [i(msg) for i in s]

    def noop(data, msg):
        """no operation. e.g. wire hub"""

    class rx:
        """Custom RxPy operators

        In addition to the standard [RxPy](https://rxpy.readthedocs.io/en/latest/operators.html)
        namespace, addressable in top level rx namespace.
        """

        def parse_conditions(conditions):
            """
            Conditions are useful in many scenarios.

            This is a generic parser of conditions dicts before data flows
            Will put the result into ax_pipelines, which is available everywhere.

            Usage:  ax_op(ax.rx.parse_conditions, conditions=conditions),

            """
            # TODO: unittest in lc
            cond = dict([(k, (v, parse_cond(v))) for k, v in conditions.items()])
            from operators.const import ax_pipelines as axp

            axp['conditions'].update(cond)
            return rx.map(lambda x: x)

        def interval_immediate(dt):
            """helper to get events, from time 0"""
            return Rx.concat(Rx.just(-1, GS), Rx.interval(dt / 1000.0))

        def debatch():
            def _debatch(msgs):
                app.debug('Debatching', len=len(msgs['payload']))
                # without sched we had blocking with redis streams originated msgs
                return Rx.from_(msgs['payload'], scheduler=GS)

                # return Rx.interval(0.01).pipe(
                #     rx.map(lambda i: as_msg(i, '', {'id': 'adf', 'name': 'asdf'}))
                # )

            return rx.flat_map(_debatch)

    def compress(payload, msg):
        """
        Compresses the payload of a message, marking compression algo in the header.

        Best format to send large messages, e.g. after buffer ops to the hub,
        compressed: msgpack:lz4

        """
        enc = msg['enc'] = 'msgpack:lz4'
        return encode_payload(payload, enc=enc)


class AX:
    """Only AX Core Ops."""

    # this is empty because the ax_core_ops are anyway always available...


class conv:
    def axtree(payload):
        if isinstance(payload, dict):
            r = AXTree(payload)
            _ = 'Converted payload to AXTree'
            app.debug(_, leafs=r.number_of_leaves()) if app.log_level < 20 else 0
            return r
        else:
            app.warn(
                'Can only convert dicts to AXTree - ignoring',
                got=type(payload),
            )


class src:
    hello = hello_server
    interval = interval
    named_subjects = {}
    file_watch = file.watch

    def on_demand(name=None, is_rx=True, op=None):
        if name is None:
            name = op['label']
        ns = ax_core_ops.src.named_subjects
        return ns.get(name) or ns.setdefault(name, NamedSubject(name))

    def nr_in(frm, nr_src, is_rx=True):
        """virtual operator handling data from node red via a subject"""
        return ax_pipelines['nr_sources'][nr_src]


class snk:
    _mem_snk = []
    _mem_snk_last_event = []  # for test clients to block for
    # that one we make accessible in ax.snk.file_out like mem, could be dest '-'
    file_write = file.snk  # sideeffect, but this one we want always, w/o add_connection
    clipboard = clipboard

    def nr_out(data, msg, to=None):
        """virtual operator handling data to node red via a subject"""
        ax_pipelines['ext_out'](msg, to)

    def mem(data, msg, wait_count=None, name='memsnk'):
        """A simple data snk in python - will be turned into a subscription
        name not evaluated just a namer to differentiate different ones
        """
        s = ax_core_ops.snk
        s._mem_snk.append(msg)
        if wait_count and len(s._mem_snk) == wait_count:
            s._mem_snk_last_event[0].set()

        if 'is_last_event' in str(msg):
            s._mem_snk_last_event[0].set()

        app.debug('mem snk got data: %s...' % str(msg)[:1000])

    forget = ax_core_ops.noop
    log = ax_core_ops.dump


ax_core_ops.src = src
ax_core_ops.snk = snk
# ax_core_ops.http = http
ax_core_ops.conv = conv
# ax_core_ops.proc = proc
# ax_core_ops.sock = sock
# ax_core_ops.redis = redis
# ax_core_ops.kafka = LazyImported(mod='operators.kafka', cls='kafka')
# ax_core_ops.mysql = LazyImported(mod='operators.mysql', cls='mysql')
# breakpoint()  # FIXME BREAKPOINT
# ax_core_ops.elastic = LazyImported(mod='operators.elastic', cls='elasticsearch')


# ax_core_ops.subflow = subflow.subflow

from operators.ctrl import server

ax_core_ops.ctrl = server

# ax_core_ops.src.subflow_in = subflow.subflow_in
# ax_core_ops.snk.subflow_out = subflow.subflow_out
# --------------------------------------------------------------- I/O encoding/decoding
