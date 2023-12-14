"""
Builder of Node Red Config, i.e. serializable lists which are understood by mocha.

Can be sent over via the control websocket as msg.reconfigure by the test program.
"""
import json

from devapp.app import app
from node_red.nr_node_arranger import arrange_xy, no_z_types

# for docu, to have it:
last_build = [None]


def escaped_flow(flow):
    """
    Flows with inner dict args must be sent json esacped inside to NR
    i.e. like this (see also export in browser):
    {"name": "mynode", "kw": "{\"foo\": \"bar\"}"}
    """

    def kwe(m):
        for k, v in m.items():
            # wires ok, what else?
            if k not in ('kw',):
                continue
            if isinstance(v, (dict, list)):
                m[k] = json.dumps(v)
        return m

    # this may json-dumped and imported in NR:
    return [kwe(i) for i in flow]


class op:
    """Supports the building of NR operators programatically, ready for nr_config"""

    def build_(
        name_, typ, id=None, wires=None, x=None, y=None, z=None, outputs=None, **kw
    ):
        m = {'name': name_, 'type': typ}
        if id:
            m['id'] = id  # auto added by nr_config when having full flow
        if wires:
            m['wires'] = wires  # auto added, by connecting to next one
        if z:
            m['z'] = z
        if x:
            m['x'] = x
        if y:
            m['y'] = y
        if outputs:
            m['outputs'] = outputs
        m.update(kw)
        return m

    class nr:
        _f_templ = """
        p = msg.payload
        if (!p.{name}) p.{name}=0
        {action}
        return msg
        """

        def func(name_, action=None, func_=_f_templ, **kw):
            action = action or 'p.{name} += 1'
            kw['func'] = func_.replace('{action}', action).replace('{name}', name_)
            return op.build_(name_, kw.pop('typ', 'function'), **kw)

    class ax:
        def op(
            name_,
            typ='ax-op',
            id=None,
            z=None,
            x=None,
            y=None,
            wires=None,
            outputs=None,
            async_timeout=0,
            deep_copy=False,
            **kw,
        ):
            """builds the nr import dict for an ax node"""
            d = dict(locals())
            if not async_timeout:
                d.pop('async_timeout')
            if not deep_copy:
                d.pop('deep_copy')
            if not outputs:
                d.pop('outputs')
            return op.build_(**d)

        def cond(name, condition, **kw):
            m = {
                'type': 'ax-cond',
                'name': name,
                'condition': json.dumps(condition),
                'outputs': len(condition),
            }
            m.update(kw)
            return m

        def join(
            name,
            id=None,
            typ='ax-join',
            accumulate=True,
            build='object',
            count='',
            ipc_via='',
            joiner='m[payload][id]',
            joinerType='str',
            key='topic',
            mode='auto',
            property='update_payload',
            propertyType='msg',
            timeout='',
            reduceExp='',
            reduceFixup='',
            reduceInit='',
            reduceInitType='',
            reduceRight=False,
            wires=None,
            **kw,
        ):
            d = dict(locals())
            d.pop('kw')
            return op.build_(
                d.pop('name'), d.pop('typ'), d.pop('id'), d.pop('wires'), **d
            )

        def src(name, **kw):
            return op.ax.op(name, typ='ax-src', **kw)
        def snk(name, **kw):
            return op.ax.op(name, typ='ax-snk', **kw)
        def snk_mem(wait_count=None, **kw):
            return op.ax.op('ax.snk.mem', typ='ax-snk', wait_count=wait_count, **kw)


ax_op = op.ax.op  # backwards compat
def rx_op(name, **kw):
    return op.ax.op('rx.' + name, **kw)
mem_snk = op.ax.snk_mem()


def get_clean_snk():
    """working with the ax_core_ops's mem snk, for tests"""
    from operators.core import ax_core_ops

    m = ax_core_ops.snk._mem_snk
    m.clear()
    return m


def cond(c, **kw):
    m = {
        'type': 'ax-cond',
        'name': 'my_condition',
        'condition': json.dumps(c),
    }
    m.update(kw)
    return m


def to_tabs_dict(l, dflt_tabid, dflt_flowid):
    """
    create default format for input: {tabname -> {flown1: [ops]}}
    """
    # return {dflt_tabid: {dflt_flowid: l}}

    zs = {}
    ops = None
    subs = []

    for op in l:
        # convenience feature like string, nested list, we keep on same tab
        # then before:
        try:
            z = op['z']
        except Exception as ex:
            if isinstance(op, dict) and op['type'] == 'subflow':
                subs.append(op)
                continue
            z = dflt_tabid
        flws = zs.get(z)
        if not flws:
            flws = zs[z] = {dflt_flowid: []}
        try:
            fid = op['flowid']
        except Exception as ex:
            fid = dflt_flowid
        ops = flws.setdefault(fid, [])
        ops.append(op)

    # rearrange subflows into sth like:
    # {'subflows': {'mysub': [<subflow def>, <firstop>, ...]}}
    d = {dflt_flowid: []}
    for s in subs:
        zs.setdefault('subflows', {})[s['id']] = l = zs.pop(s['id'], d)[dflt_flowid]
        l.insert(0, s)
    for s in subs:
        # when we create like sf=dict(type='subflow', in=[..]) then we have a python error. so we use in_
        s['in'] = s.pop('in_', s.get('in'))
    return zs


def nr_config(
    l,
    default_tab_name='tests',
    dflt_flw_name='dflt',
    wrap_dflt_all=False,
    add_nr_io=False,
    get_infunc_dflt_opid=False,
    auto_insert_hub=True,
    funcs_namespace=None,
    test_io_nodes=None,
    arrange_nodes=True,
):
    """
    De-simplify the config from a test into a compatible input for the flow function,
    i.e. with tabs and hub

    add_nr_io:
        Wrap the flow into Node Red Test Websocket IO.
        If True     -> use first and last op
        Else: 2-list ->
            - Use given 2 ops for in and out.
            - Set all with their z to z='tests', so that nr_io works
        True is the one for programmatic flows, with z='tests' or empty
        2 list is handy for recorded flows, where just the 2 I/O ops where added



    """
    # maybe only on demand, i.e. when a function ref is in?
    replace_funcs_with_names(l, funcs_namespace=funcs_namespace)
    if not l:
        raise Exception('No config')
    # We understand this structuring format: {tabname -> {'flow1': [ops], 'flow2': ..}}
    if not isinstance(l, dict):
        l = to_tabs_dict(l, default_tab_name, dflt_flw_name)

    if add_nr_io and isinstance(add_nr_io, list):
        # works only when i/o nodes on 'tests':
        tin = add_nr_io[0]
        z = tin['z']

        def z_to_tests(m, z):
            if 'z' in m and m['z'] == z:
                m['z'] = 'tests'

        l['tests'] = l.pop(z)
        [z_to_tests(m, z=z) for m in l['tests'][dflt_flw_name]]
        default_tab_name = 'tests'

    dtn = default_tab_name
    if add_nr_io:
        if not l.get(dtn, {}).get(dflt_flw_name):
            # add a NR IO wrappable test if nothing is there yet:
            l.setdefault(dtn, {}).setdefault(dflt_flw_name, ['ax.hello'])

    C, i = [], 0
    # {'tests': {'dflt': ['math:sum', {'name': 'snk:into_mem', 'type': 'ax-snk'}]}}
    infunc_dflt_opid = None
    hubs = []
    for tabn, flws in l.items():
        app.info('tab', name=tabn)
        C.append(tab(tabn))

        for flwn, flw in flws.items():
            add_nodred = bool((wrap_dflt_all or flwn == dflt_flw_name) and add_nr_io)
            i += 1
            out = ''
            if add_nodred:
                out, io = add_node_red_websocket_for_test(
                    tabn, flwn, dflt_flw_name, C, flw
                )

            ctx = {
                'i': i,
                'flow_name': flwn,
                'z': flwn if tabn == 'subflows' else tabn,
                'dflt_out': out,
                'hubs': hubs,
            }
            flw = complete_nodes(flw, ctx)

            f = wire(flw, ctx, dflt_out=ctx['dflt_out'])

            if add_nodred:
                if isinstance(add_nr_io, list):
                    i, o = add_nr_io
                    io[0]['wires'][0][1] = i['id']
                    # o is wired up, part of the e.g. recorded flow
                    o['wires'] = [[ctx['dflt_out']]]
                else:
                    if f[0]['type'] != 'ax-src':
                        infunc_dflt_opid = f[0]['id']
                        # was 'wires': [['ws.out.dflt'], ['_']]
                        io[1]['wires'][0][1] = infunc_dflt_opid
                    else:
                        io[1]['wires'][0] = []

            i = ctx['i']
            C.extend(f)
    if len(hubs) == 0 and auto_insert_hub:
        C.append(hub(tabn))
    elif len(hubs) > 1:
        raise Exception('More than 1 ax-hubs', str(hubs))
    if arrange_nodes:
        C = arrange_xy(C)
    _ = out_fd_2
    last_build[0] = [dict(i) for i in C]
    # _(json.dumps(C, indent=4))
    _('Have flow', flow='\n%s\n' % json.dumps(C))
    return (C, infunc_dflt_opid) if get_infunc_dflt_opid else C


def add_node_red_websocket_for_test(tabn, flwn, dflt_flw_name, C, have):
    # we still ahve uncompleted nodes:
    have = {op['id']: op for op in have if isinstance(op, dict) and 'id' in op}
    io = flow_io(tabn, flwn)
    for op in io:
        if op['id'] not in have:
            C.append(op)
    out = io[-2]['id']
    if flwn == dflt_flw_name:
        assert io[-2]['type'] == 'websocket out'
        assert io[0]['type'] == 'websocket-listener'
    return out, io


def tab(tab):
    return {'id': tab, 'type': 'tab', 'label': tab.capitalize(), 'disabled': False, 'info': ''}
def nod(*a, **kw):
    return dict(id=a[0], type=a[1], name=a[2], z=a[3], **kw)
def hub(tab):
    return nod('hub', 'ax-hub', 'ax-hub', tab)


def flow_io(tab, n):
    """an input path (wsin, cfgobj, func). n = name of flow, tab = z"""
    id_ws = 'ws.srv.' + n
    id_ws_in = 'ws.in.' + n
    id_ws_out = 'ws.out.' + n
    id_in_dbg = 'debug.in.' + n

    wscfg = nod(
        id_ws,
        'websocket-listener',
        '',
        tab,
        path='/ws/%s/%s' % (tab, n),
        wholemsg='true',
    )
    wsin = nod(
        id_ws_in,
        'websocket in',
        '',
        tab,
        client='',
        server=id_ws,
        wires=[[id_in_dbg, '_']],
    )
    debugin = nod(id_in_dbg, 'debug', '', tab, active=True)
    # [{"id":"23fa5e9e.64a792","type":"debug","z":"tests","name":"","active":true,"tosidebar":true,"console":false,"tostatus":false,"complete":"false","statusVal":"","statusType":"auto","x":740,"y":320,"wires":[]}]
    wscfg.pop('z')
    wsout = nod(
        id_ws_out,
        'websocket out',
        '',
        tab,
        client='',
        server=id_ws,
        wires=[],
    )
    # order matters! first:in, last: out for our flw
    return [
        wscfg,
        wsin,
        wsout,
        debugin,
    ]


def is_op(s):
    return isinstance(s, (str, dict))
def out_fd_2(s, **kw):
    return app.info(s, **kw)


def autoid(node, ctx):
    if node['type'] == 'subflow':
        return ctx['flow_name']
    return '-'.join(
        [
            node['name'].rsplit(':', 1)[-1],
            node['type'].replace('ax-', ''),
            str(ctx['i']),
        ]
    )


def complete_nodes(l, ctx):
    """
    Builds the node dicts list for the test flow, as wanted by the node-red test suite.
    - Adds ids and z
    - creates ax-op dicts from string only nodes

    This is recursive, whenever we have a splitflow, e.g. after ax-cond: [[]]

    Assumptions: Our test tab, name tests, with some base comm nodes already configured as init flow in test_server.js

    """
    # we allow [foo, [bar, baz]] - (which should actually be [foo, [[bar, ..], [baz]]]) - only the first stream is one []
    if isinstance(l, str):
        l = [l]

    f = []  # returned. the original flow but with all string ops replaced
    i = have_hub = 0
    for node in l:
        if isinstance(node, str):
            node = {'name': node, 'type': 'ax-op'}
        # subflow? -> recurse:
        if isinstance(node, list):
            node = [complete_nodes(n, ctx) for n in node]
        else:
            ctx['i'] += 1
            if not node.get('id'):
                node['id'] = autoid(node, ctx)
            node['wires'] = node.get('wires', [])
            if node['type'] not in no_z_types:
                node['name'] = node.get('name', node['id'])
                node['z'] = node.get('z') or ctx['z']
        f.append(node)
        if isinstance(node, dict) and node['type'] == 'ax-hub':
            ctx['hubs'].append(node)
        i += 1
    return f


def wire(l, ctx, dflt_out):
    """
    Wire not declared outputs
    Also deliver back the flat graph which node red wants

    """
    f = []  # contains the total flow
    prev_node = None
    i = -1
    for node in l:
        # try:
        #     if node['id'] == 'sub1_inst':
        #         breakpoint()  # FIXME BREAKPOINT
        # except:
        #     pass
        i += 1
        # splitflow e.g. after cond? -> recurse:
        if isinstance(node, list):
            if i + 1 < len(l):
                out = l[i + 1]['id']  # the node behind the subflow
            else:
                out = dflt_out  # on top level normall ws.out
            fis = [wire(n, ctx, dflt_out=out) for n in node]
            if prev_node.pop('-no_deep_copy-', None):
                ws = [[n[0]['id'] for n in fis]]
            else:
                ws = [[n[0]['id']] for n in fis]
            prev_node['wires'] = w = ws
            if prev_node['type'] == 'ax-cond':
                prev_node['outputs'] = len(w)
            [f.extend(sub) for sub in fis]
        else:
            f.append(node)
            if prev_node and (
                (
                    prev_node['type'].startswith('ax-')
                    and not prev_node['wires']
                    and not prev_node['type'] == 'ax-snk'
                )
                or prev_node['wires'] == 'next_op'
            ):
                if prev_node['wires'] == 'next_op':
                    prev_node['wires'] = []
                prev_node['wires'].append([node['id']])
            prev_node = node

    # non default flows really have to specify their wiring:
    if ctx['flow_name'] == 'dflt':
        for n in f:
            if n['wires'] == [] and n['type'] in ('ax-op', 'ax-src'):
                n['wires'] = [[dflt_out]]
    return f


def replace_funcs_with_names(l, funcs=None, funcs_namespace=None):
    """
    We allow in test programs to directly define the function, i.e. not as string

    Example:
    ax_op("ax.hello"       , foo=42)
    ax_op(ax_core_ops.hello, foo=42) # must be ident, more handy for code browsing.

    Here we turn the func ref back to a string, pointing to the exposed Func's name,
    like if the format would have been serializable.
    """
    if funcs is None:
        from operators.ops.funcs import Funcs

        if funcs_namespace:
            from operators.ops.funcs import funcs_from_package

            funcs_from_package(funcs_namespace)

        funcs = dict(
            [
                (v.get('func') if isinstance(v, dict) else None, k)
                for k, v in Funcs.items()
            ]
        )
    if isinstance(l, dict):
        [replace_funcs_with_names(v) for v in l.values()]
        return

    for i in range(len(l)):
        n = node = l[i]
        # n can be simply the function or {name: <func>, id: ..}
        if isinstance(n, dict):
            n = n.get('name')
            if not n:
                continue

        if isinstance(n, tuple):
            l[i - 1]['-no_deep_copy-'] = True
            n = l[i] = list(n)
        if isinstance(n, list):
            replace_funcs_with_names(n, funcs)
            continue
        if not callable(n):
            continue
        if n == node:
            l[i] = s = funcs.get(n)
        else:
            node['name'] = s = funcs.get(n)
        if s is None:
            breakpoint()  # FIXME BREAKPOINT
            raise Exception('Function not exposed', n)
