#!/usr/bin/env python
"""
= Parsing / Pipeline Building Strategy

Entrypoint: build_pipelines

== Reduce to Python Only Ops

Turn this

```
JSOp1 -> JSOp2 -> AX-Op1 -... AX-Opn -> JSOp3 -> JSOp4
```
into this

```
S1 -> Op1 -> ... -> Opn -> D1
```

I.e.:
. forget irrelveant (since handled by NR) JSOp1 and
replace JSOps2 into an Rx Source, pushing from an ingress subject into AX-Op1
. forget JSOp4 and turn JSOp3 into a snk (subscription, forwarding the data up to NR)


== Build Graph


Building linear pipelines is simple.

But what about general graphs?

This is an example:

```

S1 --> O1 --->           --> O4 --> D1
               O2 --> O3
S2 ---------->      ^    --> D2
                    |
S3 -----------------
```

- n inputs into O2
- m inputs into O3
- k outputs frm O3

Strategy:

. Identify all ops with >1 inputs: Do a Rx.merge over those[1]
. Identify all ops with >1 outputs: Do a rx.share() over those

[1]: Except if they have 'takes_streams_as_params' set - then just pass the srcs into the operator

Problem:

There is no canonical walking order, this is not a tree but an arbitray mesh.
I.e. if we started with S3 we can't merge the upper pipeline before it, since not yet
built.

See build_pipelines, regarding how we do this.
"""

from ast import literal_eval
import os
import json
import time
from copy import deepcopy
from functools import partial
from operator import setitem

import rx as Rx
from devapp.app import app, run_app
from devapp.tools import FLG, define_flags, jdiff
from node_red.draw.graph_easy import draw
from operators.const import ax_pipelines, stop  # , brkts  # , sources
from operators.ops import subflow, tools
from operators.prometheus import start_prometheus_server
from operators.ops.cond import Cond
from operators.ops.exceptions import Err, FuncNotFound, OpArgParseError
from operators.ops.funcs import deserialize, find_func
from operators.ops.join import Join
from operators.ops.op import Op
from operators.ops.src import Src
from operators.err_handling import activate_err_pipeline

# from operators.tools import _multi_sources, shared,  err, by_id
from operators.tools import (
    func_links_to_subj_push,
    by,
    check_wiring,
    err,
    get_share_by_selector,
    is_py,
    oplog,
    wires,
)
from rx import operators as rx
from rx.scheduler.trampoline import Lock

now = time.time


# from node_red.testing import insert_test_graph_into_test_module


class flags:
    autoshort = 'bd'
    short_maxlen = 5
    uc_pytest_export = [
        'Setting flags via environ for pytest',
        'export log_level=10; export plot_before=true; pytest -xs test_share.py  -k sock_com',
    ]

    class plot_before_build:
        n = 'Create plot before building'
        d = False

    class plot_after_build:
        n = 'Create plot after building (incl. virtual nodes)'
        d = False

    class custom_modules:
        """Function signatures must be ident with the originals"""

        n = 'Modules to import, supplying alternative functions for operators'
        d = ''
        t = list

    class environ_values:
        s = 'ev'
        n = 'Take function parameter values from environ'
        d = ''
        t = 'multi_string'

    class metrics:
        class collect:
            n = 'Enable metrics collection for all functions by default'
            d = False

        class prometheus_listener:
            n = 'host:port to start prometheus client http server at (default is port 8000). '
            n += 'Note: Host has to be reachable by Prometheus server.'
            d = ''


define_flags(flags)

rx_gevent_too_late = False
if not hasattr(Lock(), 'hub'):
    rx_gevent_too_late = True


nr_out_remote_snk = 'ax.snk.nr_out'
nr_in_remote_src = 'ax.src.nr_in'


def get_sources_for(id, AP):
    return [op for op in AP['ops'].values() if id in op.get('ws', ())]


def make_nr_src(ext_op_from, ax_id_to, AP):
    """a new virtual op, handling data from nr"""
    srcs = get_sources_for(ax_id_to, AP)
    for s in srcs:
        if s.get('_is_py') is True:
            AP['nr_cut_wires'].append([s['id'], ax_id_to])
    op, id = ext_op_from, ax_id_to
    n = id + '_in'
    AP['nr_sources'][id] = tools.NamedSubject(n)
    m = {
        'id': ((op['id'],), id),
        'type': 'ax-src',
        'name': nr_in_remote_src,
        'kw': {'frm': op, 'nr_src': id},
        'src': [],
        'wires': [[id]],
        'ws': [id],
        'z': op['z'],
        'virtual': True,
    }
    return m


def make_nr_snk(ax_op_from, ext_id_to):
    """a virtual snk op, for comm back to nr"""
    op, id = ax_op_from, ext_id_to
    m = {
        'id': (op['id'], (id,)),
        'type': 'ax-snk',
        'name': nr_out_remote_snk,
        'kw': {'to': by.id(op['id'])},
        'src': [],
        'wires': [],
        'ws': [],
        'z': op['z'],
        'virtual': True,
    }
    return m


def make_wire_hub(op, ws):
    m = {
        'type': 'ax-op',
        'name': 'ax.noop',
        'kw': {},
        'src': [[op['id']]],
        'wires': [ws],
        'ws': ws,
        'z': op['z'],
        '_is_py': True,
    }
    return m


def make_noop(op, w):
    m = {
        'type': 'ax-op',
        'name': 'ax.noop',
        'kw': {},
        'wires': [[w]],
        '_orig_wires': [[w]],
        'ws': [w],
        'z': op['z'],
        '_is_py': True,
        # important, don't change (ax-hub finds original by it):
        'id': op['id'] + '.virt.noop',
    }
    for ws in op['wires']:
        if w in ws:
            ws.remove(w)
            ws.append(m['id'])
    op['ws'].remove(w)
    op['ws'].append(m['id'])
    return m


def remember_and_cut_secondary_nr_exit_wires(op, AP):
    """op is py. We remove all wire dests to NR if there is a py dest
    If there is no py dest we remove all but one.
    The removed ones we register at add_outs, and will on_next to them
    after py op result avail (in op.py)

    Effectively we take them out of the pipeline, so that we can change w/o rebuilding
    the pipeline.

    Use case: add debug nodes/UI nodes anywhere w/o rebuild needs.


    Btw: No problem when the NR operator is not a snk but goes back to python (e.g. NR's change op):
    The wire going back to python will result in a virtual source into python, from Node
    => Data will flow back to py, even when sending to NR via add_outs.
    """
    # if op['id'] == 'ac999e11.c5cfd':
    #     op['wires'] = [['sf2i1/aj1', 'f1']]
    #     op['ws'] = ['sf2i1/aj1', 'f1']
    all = AP['ops']
    port = -1
    have = False
    for ws in op.get('wires', ()):
        port += 1
        nrs, pys = [], []
        [(pys if is_py(all[w]) else nrs).append(w) for w in ws]
        if not nrs or (not pys and len(nrs) == 1):
            continue
        have = True
        # remove all but one wire to NR if no pys and all if there are to py wires:
        [ws.remove(w) for w in nrs[0 if pys else 1 :]]
        if pys:
            # when there are py exits (and we removed all wires to NR) we send to NodeRED out of rx, imperatively:
            # Because: WITH py exits, the pipeline can be built and is subscribed to
            AP['add_outs'].setdefault(op['id'], {})[port] = nrs

    op['ws'] = wires(op) if have else op['ws']


def insert_wire_hubs(op, wiring_hubs, py_op_ids, AP):
    wrs = op.get('wires', ())
    # 'wires': [['m1'], ['m2', 'm3'], ['m4']]
    # -> insert a single wire to hub, sharing with m2, m3:
    if not (len(wrs) > 1 and len(wrs) != len(op['ws'])):
        return

    for sws in wrs:
        if len(sws) < 2:
            continue
        h = make_wire_hub(op, sws)
        h['id'] = hid = 'hub-%s' % len(wiring_hubs)
        add_op(h, AP)
        wrs[wrs.index(sws)] = [hid]
        py_op_ids.add(hid)
        wiring_hubs.append(h)
    op['ws'] = wires(op)


def add_op(op, AP):
    app.debug('New operator', **oplog(op))
    AP['ops'][op['id']] = op


def rewire_and_register(flow, AP):
    """Turn JS to py Ops into py sources. Sinks as well. Rest: Remove."""
    py_op_ids = set()
    wiring_hubs = []
    for op in flow:
        kw = op.get('kw')
        if kw is not None:
            op['kw'] = deserialize(op, 'kw')  # parameters for the function, from NR:
        if is_py(op):
            py_op_ids.add(op['id'])
            # add_op(op, AP)
            op['_is_py'] = True
            remember_and_cut_secondary_nr_exit_wires(op, AP)
            insert_wire_hubs(op, wiring_hubs, py_op_ids, AP)
        else:
            op['_is_py'] = False

    flow.extend(wiring_hubs)

    vsnks, vsrcs, noops = [], [], []

    def create_virtual_ops():
        for op in flow:
            if op.get('_is_py'):
                for w in list(op['ws']):
                    # from python to node red:
                    if w not in py_op_ids:
                        noop = None
                        if op.get('type') == 'ax-cond':
                            # requires a python follower, since followed by a filter:
                            # return msg.get('cond').get(nr) will filter all non matching
                            # exits of a cond, but can only be inserted if a python node follows the ax-cond
                            # -> we insert a virtual ax.noop between ax-cond and virtual nr snk
                            noop = make_noop(op, w)
                            noops.append(noop)  # will add those to flow after this loop
                            add_op(noop, AP)
                            py_op_ids.add(noop['id'])
                        vsnk = make_nr_snk(noop or op, w)
                        vsnks.append(vsnk)

            else:
                # node red to python?
                for w in op['ws']:
                    # from node red to python:
                    if w in py_op_ids:
                        vsrcs.append(make_nr_src(op, w, AP))

    create_virtual_ops()
    flow.extend(noops)
    # FIXME: That should not be needed anymore after add_outs feature:
    rm_dupl_ups(vsnks)
    modify_wires_to(vsnks)
    rm_dupl_downs(vsrcs)
    vs = vsnks + vsrcs
    flow.extend(vs)
    [add_op(op, AP) for op in vs]
    py_flow = [o for o in flow if o['id'] in py_op_ids or o in vs]

    # convenience regs:
    srcs, snks = [
        {op['id']: op for op in py_flow if op['type'] == t} for t in ('ax-src', 'ax-snk')
    ]
    return py_flow, srcs, snks


def rm_dupl_downs(virtual_nr_srcs):
    """
    2 NR Ops link down to one pyop.
    The 2 virtual subjects we created must be reduced to one our pyop is subscribed to.
    """

    def chk(op, h={}):
        id = op['id'][1]  # the pyop receiving downstream
        have = h.get(id)
        if not have:
            h[id] = op
            return
        have['id'] = (have['id'][0] + op['id'][0], id)
        virtual_nr_srcs.remove(op)

    [chk(op) for op in list(virtual_nr_srcs)]


def rm_dupl_ups(virtual_nr_snks):
    """
    2 uplinks from one pyop to NR have to be reduced to one.

    Not just for traffic optim but for logical reasons as well:
    When we'd send 2 msgs up to NR from a pyop, then the hub calls
    .send 2 times on his representation (ax-op) of that pyop, which he knows is wired
    to the two NR ops -> every NR op gets 2 messages.
    """

    def chk(op, h={}):
        id = op['id'][0]  # the pyop sending up
        have = h.get(id)
        if not have:
            h[id] = op
            return
        have['id'] = (id, have['id'][1] + op['id'][1])
        virtual_nr_snks.remove(op)

    [chk(op) for op in list(virtual_nr_snks)]


def modify_wires_to(virtual_nr_snks):
    def to_wires(vsnk_op):
        frm = vsnk_op['kw']['to']
        # if frm['type'] == 'ax-cond': f = flow breakpoint()  # FIXME BREAKPOINT
        nrs = vsnk_op['id'][1]
        # reduce to all python ones:
        frm['wires'] = [[w for w in ws if w not in nrs] for ws in frm['wires']]
        # drop except first, when now empty:
        for i in range(len(frm['wires']) - 1, 0, -1):
            frm['wires'].pop(i) if not frm['wires'][i] else 0
        # add node red one to first wire #TODO:
        frm['wires'][0].append(vsnk_op['id'])
        # flatten
        frm['ws'] = wires(frm)
        # breakpoint()  # FIXME BREAKPOINT
        # _by.id[op['id']] = id

    [to_wires(op) for op in list(virtual_nr_snks)]


def register_multi_source_op(multi_sources, op, in_pipe):
    app.debug('Registering multisource', id=op['id'])
    multi_sources.setdefault(op['id'], []).append(in_pipe)


def register_shared_op(shared, op, out_pipe):
    app.debug('Registering shared', id=op['id'])
    shared[op['id']] = out_pipe


def find_op_func(op, AP):
    funcs = AP['funcs']
    try:
        # v = op.get('virtual_subflow')
        # if v:
        #     if v.__name__ == 'InSrc':
        #         assert op['type'] == 'ax-src'
        #         funcs[op['id']] = {'rx': (v(op), [])}
        #     else:
        #         raise FuncNotFound(Err.op_subflow_error, op=op)
        #     return
        if op['type'].startswith('subflow:'):
            app.die('Subflow instances still present', **op)

        if op['type'] == 'ax-cond':
            c, is_filter = Cond.parse_args(op)
            if op.get('is_split') is not False:
                op['is_split'] = not is_filter
            funcs[op['id']] = {'rx': c}
            return

        if op['type'] == 'ax-join':
            subflow.add_env(op, into=op, AP=AP)
            funcs[op['id']] = {'rx': Join.parse_args(**op)}
            return

        kw = op.get('kw')
        if kw is not None:
            op['kw'] = kw
            subflow.add_env(op, into=kw, AP=AP)

        if op['type'] == 'ax-func':
            f = Op.create_ax_func(op)
        else:
            f = find_func(op)
        if op['type'] == 'ax-src':
            s = Src.parse_args(op, f)
            funcs[op['id']] = F = {'rx': s}
        elif op['type'] in ('ax-op', 'ax-snk', 'ax-func'):
            funcs[op['id']] = F = {'rx': Op.parse_args(op, f)}
            _ = 'takes_streams_as_params'
            setitem(F, _, True) if f.get(_) else 0

        v = f.get('share_by')
        if v:
            op['share_by'] = v

    except (FuncNotFound, OpArgParseError) as ex:
        app.warn(ex.args[0], **ex.details)
        op['err'] = ex.args[0]
        AP['err_build'][op['id']] = ex.details


def validate(op):
    srcs = op['src']
    if op['type'] == 'ax-src':
        if srcs:
            raise OpArgParseError(Err.op_validation_src_cannot_have_sources, **op)
    elif op['type'] == 'ax-snk':
        if op['wires']:
            raise OpArgParseError(Err.op_validation_snk_cannot_have_wires, **op)
    elif len(srcs) == 0:
        raise OpArgParseError(Err.op_validation_no_sources, **op)


def remember_all_srcs(l, ctx):
    """just for informational reasons for the user"""
    ctxs = []
    for i in l:
        m = {}
        ctxs.append(m)
        for k in 'src', 'op_ids':
            m[k] = i[1][k]
    ctx['src'] = ctxs  # we just take all (src, op_id, op_ids)


def add_srcs(srcs, l):
    if isinstance(l['src'], list):
        # FIXME: unifiy: always list, even for single source!
        [add_srcs(srcs, i) for i in l['src']]
    else:
        s = l['src']
        # is the source virtual? then its ((nrop1, nrop2), pysrc)
        # we want a list of flat start operators:
        # not the virtual ones created as tuples:
        if isinstance(s, tuple):
            s = s[-1]
        srcs.append(s)


# -------------------------------------------------------------------- End Sink Finding
# for dynamic subscriptions

# cache for already scanned external operators:
# _scanned_ids = {}


def find_snks(id, AP):
    """the recursion for function: find_ext_snks"""
    scanned = AP['ids_scanned_for_ext_snks']
    have = scanned.get(id)
    if have:
        return have
    scanned[id] = sks = []
    ops = AP['ops']
    op = ops[id]
    l = wires(op)
    if op['type'] == 'link out':
        l.extend(op['links'])

    if not l:
        sks.append(id)
    else:
        for nwid in l:
            nw = ops[nwid]
            if not nw['wires']:
                sks.append(nwid)
            else:
                sks.extend(find_snks(nwid, AP))
    return sks


def find_ext_snks(id, ctx, AP):
    """
    Continue all branches and find final sources

    We remember here if the end snk is dyn or not.
    """
    op = AP['ops'][id]
    # virtual ones (NR comm) are tuples:
    if not isinstance(id, tuple):
        assert op['type'] == 'ax-snk'
        return {id: {'subscription': 'always'}}

    asnks = []
    for i in id[1]:
        asnks.extend(find_snks(i, AP))
    if not asnks:
        asnks = [op['id']]
    snks = {}
    for id in asnks:
        op = AP['ops'][id]
        s = 'on_demand' if op['type'] in AP['dyn_snk_types'] else 'always'
        snks[id] = {
            'subscription': s,
            'current': 'unknown' if s == 'on_demand' else 'always',
        }
    return snks


def register_pipe(pipe, ctx, AP):
    id = ctx['op_id']
    m = dict(ctx)
    m['snk'] = id
    m['rxpipe_id'] = id if pipe else None
    srcs, snks = [], {}
    if pipe:
        add_srcs(srcs, ctx)
        snks = find_ext_snks(id, ctx, AP)
    m['srcs'] = srcs
    m['snks_ext'] = snks
    AP['pipes'].append(m)
    AP['rxpipes'][id] = {'rx': pipe, 'subscription': None}


nil = b'\x01'


def share_by_select_func(selector):
    def f(msg, n=selector, nil=nil):
        msg = dict(msg)
        for s in selector:
            pl = msg['payload'].get(s, nil)
            if pl != nil:
                msg['payload'] = pl
                return msg
        return nil

    return f


def add_share_by_selector(rx_list, selector):
    rx_list.append(rx.map(share_by_select_func(selector)))
    rx_list.append(rx.filter(lambda msg, nil=nil: msg != nil))


def oplog(op):
    return {'id': op['id'], 'n': op.get('name'), 'w': op.get('wires')}


build_loop_detection = {0: 0}
build_loop_detection_max_tries_allowed = 100


def detect_build_loop(op):
    op_id = op['id']
    l = build_loop_detection
    if l.get(op_id, 0) > build_loop_detection_max_tries_allowed:
        app.error('Loop detected', **op)
        raise Exception('Hit build infinite loop')
    if op_id in l:
        l[op_id] += 1
    else:
        l[op_id] = 0


def bld_sub_pipe(
    op_id,
    multi_sources,
    shared,
    AP,
    is_shared=False,
    is_multi_source_op=False,
    last_build={0: 0},
):
    """
    Build a fragment of a pipeline.

    Begins at
    - a source
    - an operator with 2 or more wires in

    Ends at:
    - a snk
    - an op with 2 or more wires out

    is_multi_source_op: op is an operator with 2 sources
    is_shared         : op is one of many wires

    conditions are done via sharing, followed by a subsequent filter for the matched con.
    """
    ctx = {'op_ids': []}
    # ctx['err'] = ex.details
    # register_pipe(None, ctx)
    op = by.id(op_id)
    m = dict(op)
    detect_build_loop(op)

    app.info(
        'Building %(type)s %(name)s' % m,
        kw=m.get('kw', ''),
        id=op['id'],
        shared=is_shared,
        multisource=is_multi_source_op,
    )
    if err(op):
        return
    nfo = oplog(op)

    if is_multi_source_op:
        if len(multi_sources[op_id]) != len(op['src']):
            # source subpipes up to us not yet all built:
            return
        app.debug('Handling multisource pipe', op=op_id)
        l = multi_sources.pop(op_id)
        src_streams = [i[0] for i in l]
        remember_all_srcs(l, ctx)
        xop = AP['funcs'][op['id']]
        if xop.get('takes_streams_as_params'):
            app.info('Combining %s streams' % len(src_streams), **nfo)
            rx_src = src_streams[0].pipe(xop['rx'](*src_streams[1:]))
            rx_list = []
        else:
            # normal function ops get the merged input streams. RxPy ops get them as arguments
            rx_src = Rx.merge(*src_streams)
            rx_list = [xop['rx']]
        nfo['is_multi_source_op'] = True

    elif is_shared:
        # built for every wire of the op, which was rx.shared
        rx_src, ctxm, deep, nr, is_split, share_by_selector = shared.pop(op_id)
        app.debug('Handling shared pipe', op=op_id)
        ctx.update(ctxm)

        rx_list = []
        if share_by_selector:
            add_share_by_selector(rx_list, share_by_selector)
        rx_list.append(rx.map(tools.share_at(op, deep_cp=deep)))

        if deep is None:
            # deep = None: forward the original, the others get copies.
            # But if we don't do this, the copies will see all the syncronous
            # operatios *following* in this stream:
            rx_list.append(rx.delay(0))

        if is_split:

            def f(msg, nr=nr):
                # pycond's rx op puts into the msg which one matched: (Pdb) msg['cond'] = {0: False, 1: False, 2: True}
                return msg.get('cond').get(nr)

            rx_list.insert(0, rx.filter(f))

        # if 'noop' in str(op): breakpoint()  # FIXME BREAKPOINT
        rx_list.append(rxop(op, AP))
        nfo['is_shared'] = True

    else:
        ctx['src'] = op_id
        # also subflows have this, as virtual in op:
        assert op['type'] == 'ax-src'
        rx_src, rx_list = rxop(op, AP)

    app.debug('Building fragment', **nfo)

    # special situation:
    # S1 -> O1  -> O2 -> O3 -> D1
    #        |           ^
    #        |___________|
    # the first op of a shared subpipe may be multisource, like O3.
    # then that op will be popped from rx_list, since he'll be the first after
    # the merged pipe (is_first flag does that in the multisource handler below):
    if is_shared and is_multi_source_chk_and_reg(
        multi_sources, op, rx_src, rx_list, ctx, is_first=True
    ):
        # handled in next loop calling this function (until all are built)
        return

    bld_linear_fragment(ctx, op_id, op, rx_src, rx_list, shared, multi_sources, AP)


def bld_linear_fragment(ctx, op_id, op, rx_src, rx_list, shared, multi_sources, AP):
    app.debug('Building fragment', **oplog(op))
    while True:
        ctx['op_id'] = op_id
        ctx['op_ids'].append(op_id)
        validate(op)

        if op['type'] == 'ax-snk':
            app.debug('Encountered snk, new pipe', **op)
            rx_list.append(rx.catch(s_catch))
            register_pipe(pipe(rx_src, rx_list), ctx, AP)
            return

        ws, deepc, is_split, ok_wires = check_wiring(op)
        sbv = op.get('share_by')
        sbss = [(get_share_by_selector(w, op, sbv) if sbv else None) for w in ok_wires]
        if len(ok_wires) > 1:
            app.debug('Shared', wires=ok_wires)

            rx_list.append(rx.share())
            rx_pipe = pipe(rx_src, rx_list)
            nr = 0
            for w in ok_wires:
                dc = deepc
                # the first output always gets the original message, no need to deepc:
                # this is how node red does it as well:
                if deepc and nr == 0:
                    # the None indicates this is the original of an otherwise copied stream:
                    dc = None
                register_shared_op(
                    shared, by.id(w), (rx_pipe, ctx, dc, nr, is_split, sbss[nr])
                )
                nr += 1
            return
        try:
            sbss[0]
        except Exception as _:
            print('current op: ', op)
            print('file: ', __file__)
            err = _cur_build_axpipelines[0].get('err_build')
            if err:
                app.error('Build error(s)', json=err)
            app.error('Your flow is unbuildable - breakpoint set for inspection.')
            breakpoint()  # FIXME BREAKPOINT
            app.die('Unbuildable flow', silent=True)
        if sbss[0]:
            add_share_by_selector(rx_list, sbss[0])

        op_id = ok_wires[0]  # let crash if not present, this is a dangling op
        op = by.id(op_id)
        app.debug('Next non sharing op', **oplog(op))
        if is_multi_source_chk_and_reg(multi_sources, op, rx_src, rx_list, ctx):
            return
        # if op['id'] == 'sfi3':
        #     breakpoint()
        rx_list.append(rxop(op, AP))
        continue


def rxop(op, AP):
    """returns the find_func results"""
    xop = AP['funcs'][op['id']]['rx']
    return xop


def is_multi_source_chk_and_reg(multi_sources, op, rx_src, rx_list, ctx, is_first=False):
    srcs = op['src']

    def healthy_sources(srcs):
        return [id for id in srcs if not (err(id))]

    # Using set because: Are the sources actually one and the same op?
    # if len(healthy_sources(srcs)) < 2:
    # TODO: Test this! Is the data duplicated when the one source has 2 wires to op?
    if len(set(healthy_sources(srcs))) < 2:
        return

    # more sources -> merge:
    if is_first:
        # will added again in multisource subpipe:
        rx_list.pop()
    rx_pipe = pipe(rx_src, rx_list)
    register_multi_source_op(multi_sources, op, (rx_pipe, ctx))
    return True


# def rx_list_with_subflow_ops(rx_list, sf_out_port=0):
#     # the .share has to insert this:
#     r, p = [], 0
#     for rxop in rx_list:
#         if isinstance(rxop, subflow.Instance):
#             if rxop == rx_list[-1]:
#                 # for earlier instances we've set port 0, since, if its not plain 1:1 wiring we would have called this on the earlier one already:
#                 p = sf_out_port
#             r.extend(subflow.pipe_insert(rxop, p, rx_list, r, ax_pipelines))
#         else:
#             r.append(rxop)
#     return r


def pipe(rx_src, rx_list):
    # rx_list = rx_list_with_subflow_ops(rx_list)
    return rx_src.pipe(*rx_list)


def s_catch(exc, src):
    # those shall be handled out of stream and not enter any furhter processing
    ax_pipelines['rxerrors']['data']['rx'].on_next(exc)
    return src


def clear_all(ext_out, dyn_snk_types, into=ax_pipelines):
    # set up all globals. Only api one is ax_pipelines:
    # unsubscribe_many('all')
    AP = into
    ns = tools.NamedSubject
    for m in ['build', 'data']:
        try:
            s = AP['rxerrors'][m]['subscription']
            s.dispose() if s else 0
        except Exception:
            pass  # normal
    AP.clear()

    # fmt:off
    AP['ids_scanned_for_ext_snks'] = {}
    AP['ops']                       = {}
    AP['prebuild_pyops']            = {}
    AP['ts_built']                  = now()
    AP['minor_changes']             = []  # no rebuild
    AP['add_outs']         = {}  # simple node red outs, w/o pipeline effect
    AP['nr_sources']                = {}  # simple node red outs, w/o pipeline effect
    AP['nr_cut_wires']              = []  # which wires have to be cut on NR to prevent sending Py-Py Traffic down
    AP['ext_out']                   = ext_out or (lambda msg, op: None)
    AP['rxpipes']                   = {}
    AP['pipes']                     = []
    AP['err_build']                 = {}
    AP['dyn_snk_types']            = dyn_snk_types or []
    AP['funcs']                     = {}
    AP['envs']                      = {}
    AP['rxerrors']                  = {}
    # fmt:on

    for m in ['build', 'data']:
        AP['rxerrors'][m] = {'rx': ns(m), 'subscription': None}
    # The last remaining global config state:
    # Any lookup of an op by id will check AP from now on - those lookups are done at build time.
    # (I can't see that op by id lookups are done at run time - that would crash then. but func bodies have no ref to the op anyway)
    by.id = partial(by._id, frm=AP)


def set_dangling_err(op):
    if op['type'] != 'ax-src':
        if not op['src']:
            op['err'] = 'NoSource'
            return
    if op['type'] == 'ax-snk':
        return
    ws = op.get('wires')
    if ws in ([], [[]]):
        op['err'] = 'Dangling'


def remove_not_present_wires_and_links(ops, _empty=[]):
    for id, op in ops.items():
        ids = [op.get('links', _empty)]
        [ids.append(l) for l in op.get('wires', _empty)]
        rm = []
        for s in ids:
            for wid in s:
                if wid not in ops:
                    rm.append([wid, s])
        for k, l in rm:
            l.remove(k)
            app.error('Removed Missing Node ID', missing=k, in_=l, op=op)


def rm_error_sources(op):
    rm = ()
    for id in op.get('src'):
        if by.id(id).get('err'):
            rm += (id,)
    for id in rm:
        op['src'].remove(id)


# ONLY! for having access to build errors stored in AP, during build
_cur_build_axpipelines = [{}]


def build_pipelines(flow, ext_out=None, dyn_snk_types=None, force_rebuild=None):
    """
    Entrypoint.

    flow is node red compatible graph.
    ext_out is a function handling outgoing (non in stream) data, e.g. to NR
        sig: def my_ext_out(msg, op) (where op is the operator representating the dest)
    dyn_snk_types: list of types with dynamic subscriptions. We must remember those for later subscribe_many

    all build state will be kept in ax_pipelines dict
    """
    # before changing ax_pipelines we build into here, in order to see if re-sub is
    # actually needed (could be a minor change not affecting us).
    AP = _cur_build_axpipelines[0] = {}
    clear_all(ext_out, dyn_snk_types, into=AP)
    build_loop_detection.clear()
    drawplot = partial(draw, flow, tag='_prebuild_')
    if FLG.plot_before_build:
        app.info('Pre build visualization')
        drawplot()
    # insert_test_graph_into_test_module(flow)
    activate_err_pipeline(AP, 'build')

    func_links_to_subj_push(flow)

    def group_into_tabs_cfg_and_subflows(flow):
        # tabs and config:
        tabs, cfg = {}, {}
        for op in flow:
            op['type']
            z = op.get('z', op['id'])
            tabs.setdefault(z, {})[op['id']] = op
        cfg.update(tabs.pop('', {}))
        sfs = [z for z in tabs if tabs[z][z]['type'] == 'subflow']
        # subflows:
        sfs = {z: tabs.pop(z) for z in sfs}
        return tabs, cfg, sfs

    # we'll mangle wires, remember their origs:
    [setitem(op, '_orig_wires', deepcopy(op.get('wires'))) for op in flow]

    tabs, AP['cfg'], AP['sfs'] = group_into_tabs_cfg_and_subflows(flow)
    prebuild = {}
    if not tabs:
        app.error('No matching tabs in flows.json')
        import sys

        sys.exit(1)
    for tab in tabs:
        app.info('Building', tab=tab)
        prebuild[tab] = p = bld_tab_ops(tab, AP, tabs)
        AP['prebuild_pyops'][tab] = p[0]
    req, diff = does_change_require_rebuild(AP)
    if not req and not force_rebuild:
        for k in 'ops', 'add_outs':
            ax_pipelines[k] = AP[k]
        ax_pipelines['minor_changes'].append(now())
        app.warn('Skipping rebuild - minor change', diff=diff)
        return False

    if force_rebuild:
        app.warn('Force rebuild is set', change='major' if req else 'minor')
    else:
        if diff is None:
            app.info('Full build - initial version')
        else:
            fd = diff.pop('fulldiff', None)
            app.warn(
                'Full rebuild - major change', diff=diff
            )  # CAUTION: do NOT json colorize, has tuple idxs!
            if fd:
                app.debug('Full diff', diff=fd)

    # we keep those to allow mutations of e.g. kw when building, which would otherwise
    # lead to have a major change detected:
    AP['prebuild_pyops_serialized'] = str(AP['prebuild_pyops'])
    # breakpoint()  # FIXME BREAKPOINT
    unsubscribe_many(which='all')
    clear_all(ext_out, dyn_snk_types, into=ax_pipelines)
    start_prometheus_server()
    ax_pipelines.update(AP)
    for tab in tabs:
        axp = build_tab(AP, *prebuild[tab])
    activate_err_pipeline(AP, 'data')
    return axp


def does_change_require_rebuild(AP):
    """What actually changed between the new AP and the currently running ax_pipelines"""
    if not ax_pipelines:
        # process start:
        return True, None
    for p in ('cfg', 'envs'):
        if AP[p] != ax_pipelines[p]:
            app.info('major change - cfg / env diff', was=ax_pipelines[p], now=AP[p])
            return True, jdiff(AP[p], ax_pipelines[p])

    oldtabs = literal_eval(ax_pipelines['prebuild_pyops_serialized'])
    newtabs = AP['prebuild_pyops']
    diff = {k: jdiff(ax_pipelines[k], AP[k]) for k in ['ops', 'add_outs']}
    # with open('f1.py', 'w') as fd:
    #     fd.write(str(ax_pipelines['ops']))
    # with open('f2.py', 'w') as fd:
    #     fd.write(str(AP['ops']))
    #
    if len(oldtabs) != len(newtabs):
        return True, diff

    check_params = {
        'dflt': ['kw', 'name', 'wires', 'type'],
        'ax-func': ['finalize', 'initialize', 'func'],
        'ax-cond': ['condition', 'match_msg'],
        'ax-op': ['async_timeout', 'deep_copy'],
    }

    for tab in oldtabs:
        if tab not in newtabs:
            app.info('major change, tab missing', tab=tab)
            return True, diff
        po, pn = oldtabs[tab], newtabs[tab]
        if len(po) != len(pn):
            return True, diff
        pnm = {op['id']: op for op in pn}
        for opo in po:
            opn = pnm.get(opo['id'], {})
            chk = check_params.get('dflt')
            add = check_params.get(opn.get('type'))
            if add:
                chk = list(chk)
                chk.extend(add)

            for p in chk:
                if opo.get(p) != opn.get(p):
                    return (
                        True,
                        {
                            'fulldiff': diff,
                            'differing key': p,
                            'was': opo.get(p),
                            'is': opn.get(p),
                        },
                    )
    return False, diff


def bld_tab_ops(tab, AP, tabs):
    """All ops on a tab"""
    # ax_pipelines['subflows'].update(S)
    # id -> op dict:
    tab_ops = tabs[tab]
    AP['ops'].update(tab_ops)
    # if 1 or FLG.plot_before:
    #     draw(flow)

    # _by.id['chk']['err'] = 'no source'
    # remove irrelevant ops:
    remove_not_present_wires_and_links(tab_ops)
    # we flatten the wires, no difference in [[a], [b]] and [[a,b]]

    subflow.recurse_into(tab_ops, AP)
    # we got a lot of more ops, so again:
    flow = list(tab_ops.values())
    [setitem(op, 'ws', wires(op)) for op in flow]
    # insert virtual sources wiring hubs and snks:
    py_flow, srcs, snks = rewire_and_register(flow, AP)
    # We need to know if we are multisource:
    # -> set into any wire destination of an op the op into src list:
    [setitem(op, 'src', []) for op in py_flow]
    [by.id(w)['src'].append(op['id']) for op in py_flow for w in op['ws']]

    drawplot = partial(
        draw,
        py_flow,
        all_tabs=True,
        add_outs=AP['add_outs'],
        tag=tab + '.post_build',
    )
    if FLG.plot_after_build:
        app.info('Build result visualization')
        drawplot()

    return py_flow, srcs, snks


def build_tab(AP, py_flow, srcs, snks):
    [find_op_func(op, AP) for op in py_flow]
    [set_dangling_err(op) for op in py_flow]

    # groups = build_groups(py_flow, srcs, snks)

    # If an op is in err status we must mark as err all
    # - to the left (back in time) until the first sharing point or a src
    # - to the right until the first merging point
    for pe in [propagate_err_left, propagate_err_right]:
        [pe(op) for op in py_flow if op.get('err')]
    [rm_error_sources(op) for op in py_flow]

    multi_sources, shared = {}, {}
    build_sub = partial(bld_sub_pipe, AP=AP, multi_sources=multi_sources, shared=shared)
    # build first subpipe fragments:
    for id_, src in srcs.items():
        if not src.get('err'):
            build_sub(src['id'])

    # we built the first subpipes for all known ax-src ops.
    # the subpipes in between are built in varying order, there is no canonical way,
    # how to walk that graph, since it's NOT (always) a tree.
    # SO: We loop - determining subpipe fragments on the way, register and pop, until
    # no new ones emerge:
    iteration = 0
    while True:
        iteration += 1
        if iteration > 1000000:
            app.die('Cannot resolve pipeline mesh')

        if not multi_sources and not shared:
            break

        for mso, pipes in dict(multi_sources).items():
            build_sub(mso, is_multi_source_op=True)

        for op_id, pipes in dict(shared).items():
            # op_id the first op of the subpipe after the sharing point:
            # if op['id'] == '3cdb82f9.1014fe':
            #    breakpoint()
            build_sub(op_id, is_shared=True)

    return ax_pipelines


def propagate_err_left(err_op):
    """
    mark all err to after the first previous sharing point
    """
    # go left:
    for id in err_op['src']:
        print(id)
        op = by.id(id)
        # conditions may not have ANY failing dests -> take them out:
        if len(op['ws']) > 1 and not op['type'] == 'ax-cond':
            return
        # source of error op has only one wire (to err op) -> take it out as well:
        op['err'] = 'propagated'
        if op['type'] == 'ax-src':
            return
        # recurse:
        propagate_err_left(op)


def propagate_err_right(err_op):
    """
    mark all err to before the first merging point"""
    if err_op['type'] == 'ax-snk':
        return
    for id in err_op['ws']:
        op = by.id(id)
        if len(op['src']) > 1:
            return
        propagate_err_right(op)


def subs_change(id, mode='subscribed'):
    return subscribe_many(which=id, mode=mode)


def subscribe_many(which='all', mode='subscribed', dyn_snk_status=None):
    """
    all: clear
    internal: Only subscribe to pipes with internal snks
    dyn_snk_status:
        if not None, we subscribe all which are not subscribed at any endpoint
        e.g. {ws.out.dflt='subscribed'}

    This is called for dyn subs everytime the first or last websocket connects
    """
    if rx_gevent_too_late:
        app.warn(
            'UNPATCHED GEVENT',
            err='Gevent is not patched in RX - might result in missing subscriptions!',
            remedy='from devapp import gevent_patched (in your client)',
        )
    # if which == 'internal':
    #     breakpoint()  # FIXME BREAKPOINT
    is_subs_change = False
    if not (which == 'all' or which == 'internal'):
        is_subs_change = True
        dyn_snk_status = {which: mode}

    axp = ax_pipelines
    pipes = axp.get('pipes')
    if not pipes:
        return
    ops = axp['ops']
    rxpipes = axp.get('rxpipes')

    for p in pipes:
        id = p['op_id']
        pipe_id = p['rxpipe_id']
        if not pipe_id:
            app.warn('Pipeline not built', id=id, err=p.get('err'))
            continue
        ops[id]
        rxp = rxpipes[pipe_id]
        sbc = rxp.get('subscription')

        if which == 'internal':
            if is_remote(p, 'snk'):
                continue

        if dyn_snk_status is not None:
            stati = {}
            dss = dyn_snk_status
            # dss sent by hub at register status, current state of e.g. websockets:
            if is_subs_change:
                # is the subscrption change relevant for this pipe:
                if which not in p['snks_ext']:
                    continue

            for sid, status in p['snks_ext'].items():
                if status['subscription'] == 'always':
                    stati['subscribed'] = True
                s = dss.get(sid)
                if s:
                    status['current'] = s
                    stati[s] = True

            if mode == 'subscribed' and not stati.get('subscribed'):
                continue
            if mode == 'unsubscribed' and not stati.get('unsubscribed'):
                continue

        if mode == 'unsubscribed':
            if not sbc:
                continue
            app.info('Unsubscribing', id=id)
            sbc.dispose()
            rxp['subscription'] = None
            p['subscription'] = 'unsubscribed'
        else:
            if sbc:
                continue
            app.info('Subscribing', id=id)
            try:
                rxp['subscription'] = rxp['rx'].subscribe(lambda x: x)
            except Exception:
                print('breakpoint set')
                breakpoint()
            p['subscription'] = 'subscribed'
        time.sleep(0)


def unsubscribe_many(which='all', clear_pipelines=False):
    if which == 'all':
        # see kv.py redis - resetting the connection pool:
        # otherwise problems at e.g. pytest:
        for f in stop:
            try:
                if isinstance(f, dict):
                    app.warn('calling stop', stopper=f['name'])
                    f = f['func']
                else:
                    app.warn('calling stop', f=f)
                f()
            except Exception:
                pass
        stop.clear()
    subscribe_many(which, mode='unsubscribed')
    if clear_pipelines:
        ax_pipelines.clear()


def is_remote(pipe, what):
    n = nr_out_remote_snk if what == 'snk' else nr_in_remote_src
    if ax_pipelines['ops'][pipe[what]]['name'] == n:
        return True


def start():
    from operators.ops.funcs import funcs_from_package
    from operators.core import AX

    fn = FLG.flows_file
    if not os.path.exists(fn):
        app.die('Flows file not found', fn=fn)
    with open(fn) as fd:
        f = fd.read()
    f = json.loads(f)
    fns = FLG.function_namespace
    if not fns:
        F = AX
    funcs_from_package(F)
    build_pipelines(f)


def main():
    class main_flags:
        autoshort = ''

        class flows_file:
            n = 'Filename of flows'
            d = 'flows.json'

        class function_namespace:
            n = 'Function namespace to use appart from ax:'
            d = ''

    define_flags(main_flags)
    run_app(start)


if __name__ == '__main__':
    main()
