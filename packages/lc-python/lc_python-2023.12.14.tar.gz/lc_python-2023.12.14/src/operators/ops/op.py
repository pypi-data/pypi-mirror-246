from gevent import spawn
from gevent.event import Event
import sys
from importlib import import_module
from string import ascii_letters as letters
from string import digits
from devapp.tools import write_file
from devapp.app import app
from operators.const import d_ax_func_mods, rpl_ax_func, tmpl_ax_func
from operators.ops.exceptions import Err, OpArgParseError
from operators.ops.tools import GS, Rx, as_msg
from operators.ops.tools import p as partial
from operators.ops.tools import raise_timeout, rx, send_secondary
from operators.err_handling import set_data_exc, is_exc, had_no_exception
from operators.prometheus import make_counters, err_total

# from prometheus_client import start_http_server, Summary, Counter

import time

now = time.time


def as_aggr_msg(msgs, f, op):
    """Output of buffer or window into an aggregate message"""
    res = as_msg(msgs, f, op)
    if not msgs:
        app.warn("No aggregate - don't know where to send empty []", **op)
    else:
        ws = msgs[0].get('_ws')
        if ws:
            res['_ws'] = ws
    res['is_aggr'] = len(msgs)
    send_secondary(op, res)
    return res


class ax_func_tools:
    """Dynamic Functions Support"""

    def clean_func_name(s):
        s0 = s[0] if s[0] in letters else 'func_'
        return s0 + ''.join([c for c in s[1:] if c in letters or c in digits or c == '_'])

    def ind(s, count):
        if not s.strip():
            return s
        s = '\n' + s.strip()
        spc = '\n' + (count * '    ')
        return spc.join([l for l in s.splitlines()])

    # when this is in the init body, we call it everytime on subs:
    def has_subs(s):
        return '\nif subscribed:' in ('\n' + s)

    def create_ax_func(op):
        """A func given in the op itself: ax-func

        We generate an rx function with setup, subscription an on_next funcs,
        as a file, so that we can have breakpoints.
        """
        cls = ax_func_tools
        M = dict(rpl_ax_func)
        name = M['name'] = op.get('name') or cls.clean_func_name(op['id'])
        s_init = op.get('initialize', '')
        p = partial(cls.ind, s_init)
        i = M['initialize'] = p(2)
        M['setup'] = p(1)
        if not i or not cls.has_subs(s_init):
            M['call_init_subs'] = ''

        M['func'] = cls.ind(op.get('func', ''), 2)

        s = tmpl_ax_func
        for k in M:
            s = s.replace('__AX_FUNC_%s__' % k, M[k])

        func = cls.create_func(name, s, op)

        app.debug('Converted to', body=s)
        l = [['is_rx_op', True], ['incl_msg', True], ['name', name], ['func', func]]
        return {k: v for k, v in l}

    def create_func(name, body, op):
        """Allows to have breakpoints with real source code output"""
        fn = '%s/%s.py' % (d_ax_func_mods(), name)
        write_file(fn, body, mkdir=0)
        # swap out old version:
        sys.modules.pop(name, 0)
        # add the new version:
        try:
            mod = import_module(name)
            func = getattr(mod, name)
        except Exception as ex:
            raise op_build_err(op, ex, body=body)

        app.info('Created function', name=name, id=op['id'])
        return func


def op_build_err(op, ex, msg=Err.func_not_compilable, err=OpArgParseError, **kw):
    if app.log_level < 20:
        app.debug(msg, **op, exc=ex)
    return err(msg, name=op.get('name'), id=op['id'], exc=ex, **kw)


nil = '\x09'


class Op:
    """A Function node.
    Can optionally pass full msg if wanted in signature, like NR
    """

    create_ax_func = ax_func_tools.create_ax_func

    def parse_args(op, func):
        """
        next_ops     : no effect here, only for sig compat with others
        has_pipe_tail: no effect here, only for sig compat with others
        """
        # f = find_func(op)
        f = func
        # postprocess func, e.g. to msg-ify rx raw output (e.g. tuples for combine_latest)
        # we chose pp to not collide with real postprocess signature args:
        pp = f.get('pp')
        if pp:
            pp = rx.map(pp)

        c_dt, c_cnt, c_err = make_counters(f['name'], op)

        if f.get('is_rx_op'):
            # Handling rx operator turning the messages flow into an aggregate, i.e. a list.
            # We nail the format of that aggregate here, since we always want dicts with headers
            # passed around!

            # CAUTION: self made/derived aggretation operators have to do that on their own:
            try:
                # e.g. op['name'] == 'rx.combine_latest'. in funcs.py we found that it
                # takes streams as input:
                func = f['func']
                if f.get('takes_streams_as_params'):

                    def rxop_which_takes_streams(*streams, pp=pp):
                        return rx.pipe(func(*streams), pp)

                    return rxop_which_takes_streams if pp else func
                # without a postprocessor the raw rx one is good enough:
                ops = [func()]
            except Exception as ex:
                raise op_build_err(op, ex)

            if f['name'].split('_', 1)[0] in ('rx.window', 'rx.buffer'):
                # split for: buffer_with_time[_or_count]
                # TODO: are there more which create aggreates?
                # filter empty aggregates
                ops.append(rx.filter(lambda msgs: bool(msgs)))
                ops.append(rx.map(lambda msgs, op=op, f=f: as_aggr_msg(msgs, f, op)))
                if pp:
                    ops.append(pp)
            return rx.pipe(*ops)

        def call(
            msg,
            func=f['func'],
            name=op['name'],
            op=op,
            is_snk=op['type'] == 'ax-snk' and not op.get('is_virtual_subflow_snk'),
            f=f,
            c_dt=c_dt,
            c_cnt=c_cnt,
            c_err=c_err,
            now=now,
        ):
            # FIXME: why not do this in set_data_exc(a few lines below)?
            # do we even get here (see had_no_exception)?
            if is_exc(msg):
                if c_err:
                    c_err.inc()  # per func
                    err_total().inc()  # total
                # Simply pass thru exceptions to the end (Railway Oriented Programming):
                return msg

            # we let crash if the msg is not a msg
            # # when the previous one was a raw rx operator, we get sometimes tuples of combined events:
            # # e.g. rx.combine:
            # try:
            #     msg['_ids']
            # except:
            #     if isinstance(msg, tuple):
            #         msg = list(msg)
            #     msg = as_msg(msg, f, op)

            if c_dt:
                t0 = now()
            is_async = op.get('async_timeout', 0)
            # FIXME: replace by at exit dyn subscriptions
            app.debug(op['name'])
            try:
                if not is_async or is_async < 0:
                    # when async and do not do timeout control, we are already on other greenlet.
                    res = func(msg)
                else:
                    res = run_async_with_timeout(func, msg, op)
            except Exception as ex:
                # msg['payload'] set there to tuple, published to rxerrors, returns None
                set_data_exc(msg, ex, op=op)
                res = None

            if is_snk:
                # if this is a snk there is no need to mutate messages:
                # he should get anything we have:
                return
            try:
                # convenience: No need to return payload, we can modify inplace:
                if res is not None:
                    msg['payload'] = res
                # This is NOT in for any op, don't rely on it. We add it for the last one in node_red.op.py
                op_id = op['id']
                msg['op'] = op_id
                send_secondary(op, msg)

            except Exception as ex:
                # we cannot assign, allthough we tried to even handle buggered msgs.
                # => fail
                ex.msg = 'Assignment error: %s' % str(msg)
                ex.op = op
                raise  # end of stream
            if c_dt:
                dt = now() - t0
                c_dt.inc(int(dt * 1000000))
                c_cnt.inc()
            return msg

        rxop = rx.map(call)
        if op.get('async_timeout'):

            def op_run_async(msg, rxop=rxop):
                """Gives up order for throughput"""
                # TODO set log hard smells. clear, another greenlet, but still
                # maybe a checkbox in NR?
                return Rx.just(msg, GS).pipe(rx.delay(0, GS), rx.map(set_log), rxop)

            rxop = rx.flat_map(op_run_async)

        return rx.pipe(rxop, rx.filter(had_no_exception))

        # breakpoint()  # FIXME BREAKPOINT
        # rxop = rx.map(call)
        # if op.get('async_timeout'):

        #     def op_run_async(msg, rxop=rxop):
        #         """ Gives up order for throughput"""
        #         return Rx.just(msg, GS).pipe(rx.delay(0, GS), rxop)

        #     rxop = rx.pipe(
        #         rx.flat_map(op_run_async),
        #         # rx.filter(lambda msg: msg['payload'] != 'timeout'),
        #     )

        # return rx.pipe(rxop, rx.filter(filter_exceptions))

        # return rx.pipe(*(wrap_async(rx.map(call), op), rx.filter(filter_exceptions)))


def set_log(msg):
    """Logger will use this as logger_name

    Needed after greenlet changes (async)
    """
    ln = msg['_ids'].get('log')
    if ln:
        gevent.getcurrent().logger_name = ln
    return msg


class Event(Event):
    pass


import gevent

g = getattr


def ct():
    return gevent.getcurrent()


def run_async_with_timeout(func, msg, op, marker='\x09'):
    """When a positive timeout is configured, we enforce it here.

    We do it manual (not in rx) via spawn / event, relying on gevent as underlying async framework.
    """
    to = op['async_timeout']
    ev = Event()
    ev.res = marker

    def run(func=func, msg=msg, op=op, ev=ev):
        # new greenlet, i.e. we have to yet again set the logger:
        set_log(msg)
        ev.res = func(msg)
        ev.set()

    spawn(run)
    ev.wait(to)
    if not ev.res == marker:
        return ev.res
    raise_timeout(msg, op)


# def wrap_async(rxop, op):
#     # FIXME: Will be way too slow. See pycond.py. See asyncalternative.py
#     at = op.get('async_timeout')
#     if not at:
#         return rxop

#     def do_async(msg, rxop=rxop, timeout=at, op=op):
#         return Rx.merge(
#             Rx.just(msg).pipe(
#                 rx.delay(timeout), rx.map(lambda msg, op=op: do_raise_timeout(msg, op)),
#             ),
#             Rx.just(msg).pipe(rx.delay(0, GS), rxop),
#         ).pipe(rx.first())

#     return rx.flat_map(do_async)
