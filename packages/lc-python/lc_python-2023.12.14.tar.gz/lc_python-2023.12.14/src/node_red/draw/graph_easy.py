# from operators.tools import _multi_sources, _shared, _by_id, err, by_id
# from operators.tools import wires as wires_, get_share_by_selector, check_wiring
import io
import os
from contextlib import redirect_stdout
from functools import partial

from devapp.tools import FLG, define_flags, termwidth, project, exists
from devapp.app import app

from .layout import layout

# from operators.build import wires as wires_, check_wiring, get_share_by_selector


class flags:
    autoshort = ''
    short_maxlen = 5
    uc_redraw = [
        'Auto-redrawing, with markdown level 1 headers, at every rebuild in NodeRED',
        'echo flows.json | entr -dnr build --plot_before --plot_tab_header_prefix="# "',
    ]
    uc_subflow_depth = [
        'Monitor flows.json, redraw on change, into second subflow nesting level.',
        'build -bdpb --dirwatch .:flow -plot_depth 2',
    ]

    class plot_mode:
        n = 'Set output mode. src: graph-easy source.'
        d = 'boxart'
        t = ['boxart', 'svg', 'src']

    class plot_sync_mode:
        n = 'Run all plots blocking, do not spawn off a thread/greenlet'
        d = True

    class plot_depth:
        n = 'Plot depth (how deep we go into subflows)'
        d = 1

    class plot_destination:
        n = 'Where to plot to (filename, - means stdout). $FOO will be replaced by env var.'
        d = '-'

    class plot_write_flow_json:
        n = 'Write the plotted flow as json to the destination'
        d = ''

    class plot_destination_create_dir:
        n = 'Create output directory if not present'
        d = False

    class plot_boxart_maxwidth:
        n = 'Columns to use when plotting boxart. -1: Infinite. 0: Auto.'
        d = 0

    class plot_boxart_maxwidth_fallback:
        n = 'Fallback width when creating plots at undeterminable termwidth situations, e.g. in a pipe'
        d = 200

    class plot_direction:
        n = 'Plot direction (south: vertical, east: horizontal. auto: by termwidth, try east first)'
        d = 'auto'

    class plot_max_label_width:
        n = 'Maximum label width for plots. 0: Unrestricted'
        d = 20

    class plot_all_tabs:
        n = 'If Tabs will be merged then, display wise. Links will be wired'
        d = False

    class plot_tab_header_prefix:
        n = 'How to prefix headers. Default: emacs org mode style. Empty string: No headers (all nodes on one virtual tab.)'
        d = '** '

    class plot_id_short_chars:
        n = 'Number of start characters to reduce ids to (0: do not reduce, -1: omit totally)'
        d = 4


define_flags(flags)

# ------------------------------------------------------------------------------- tools
class F(list):
    __repr__ = __str__ = lambda s: '<the flow list>'


def set_dflt(m, k, f, *args):
    v = m['plot'].get(k)
    if not v:
        v = m['plot'][k] = f(*args)
    return v


def init_ctx(flow, id_short_chars, **kw):
    # clone it:
    flow = [dict(m) for m in flow]
    ctx = dict(locals())
    ctx['sids'] = set()
    ctx['id_short'] = id_short_chars or FLG.plot_id_short_chars
    ctx['max_label_width'] = FLG.plot_max_label_width
    ctx['by_id'] = all = {}
    ctx['all_tabs'] = kw['all_tabs'] or FLG.plot_all_tabs
    ctx['one_canvas'] = not bool(FLG.plot_tab_header_prefix)
    ctx['zs'] = zs = {}
    ctx['tag'] = kw['tag']
    ctx['flow'] = F(ctx['flow'])  # reduce print outs
    ctx['add_outs'] = sno = kw['add_outs'] or {}
    # l['all_wire_dests'] = set()
    sfs, have_sf_io, is_built = [], False, True
    for op in flow:
        if isinstance(op['id'], tuple):
            is_built = True
        op = dict(op)
        if op.get('name', '') in ('ax.subflow:virtual_in', 'ax.subflow:virtual_out'):
            have_sf_io = True
        elif op['type'] == 'subflow':
            sfs.append(op)
        new_op(op, ctx)
    if sfs and not have_sf_io and not is_built:
        init_add_subflow_io_if_not_present(flow, ctx, sfs)
    ctx['graph_opts'] = graph_opts()  # -> ['graph { flow: east; }']
    ctx['out_zs'] = []
    ctx['have_z'] = []
    # when drawing build's py_flows we have no more tabs -> fake them:
    for k in ctx['zs']:
        if not all.get(k):
            new_op({'type': 'tab', 'id': k, 'z': k}, ctx)

    if ctx['all_tabs']:
        tabs = [k for k in ctx['zs'] if all[k]['type'] == 'tab']
        zs['all_tabs'] = l = []
        new_op({'type': 'tab', 'id': 'all_tabs', 'z': 'all_tabs'}, ctx)
        for k in tabs:
            l.extend(ctx['zs'][k])
    return ctx


def new_op(op, ctx):
    op['plot'] = pm = {}  # all plot specific infos here
    pm['id'] = op['id']
    pm['type'] = op['type']
    pm['z'] = op.get('z')
    if ctx['one_canvas']:
        pm['z'] = 'canvas'
        if op['type'] == 'tab':
            pm['id'] = 'canvas'
    z = op.get('z')
    if z:
        ctx['zs'].setdefault(z, []).append(op)
    ctx['by_id'][pm['id']] = op
    set_flat_wires(op)
    pm['layout'] = layout(op, ctx)
    return op


def set_flat_wires(op):
    op['plot']['wires_flat'] = [w for ws in op.get('wires', ()) for w in ws]


def init_add_subflow_io_if_not_present(flow, ctx, subflow_ops):
    for op in subflow_ops:
        for i in op.get('in', ()):
            nr = -1
            for w in i['wires']:
                nr += 1
                m = {
                    'id': op['id'] + 'in',
                    'type': 'io_in',
                    'name': 'I%s' % nr,
                    'wires': [[w['id']]],
                    'z': op['id'],
                }
                new_op(m, ctx)
        nr = -1
        for i in op.get('out', ()):
            nr += 1
            id = op['id'] + 'out_%s' % nr
            m = {
                'id': id,
                'type': 'io_out',
                'name': 'I%s' % nr,
                'z': op['id'],
            }
            new_op(m, ctx)
            for w in i['wires']:
                oop = ctx['by_id'][w['id']]
                oop['wires'][w['port']].append(id)
                set_flat_wires(oop)


def shw(p):
    # debug Tool only
    os.system("echo '%s' | '%s' -as boxart" % (p, get_graph_easy()))


tabs = {}
# ------------------------------------------------------------------------------- entry


# get_graph_easy = lambda: project.get_present_resource_location('graph_easy')
def get_graph_easy():
    # prefer any std installed one:
    # fn = project.root() + '/bin/graph-easy'
    # if exists(fn):
    #     return fn
    return 'graph-easy'  # $PATH


def draw(
    flow,
    ctx=None,
    cur_depth=0,
    all_tabs=False,
    add_outs=None,
    depth=None,
    id_short_chars=None,
    z_match=None,
    no_print=False,  # return the plot, don't print it to stdout
    tag='',
):
    """
    http://bloodgate.com/perl/graph/manual/hinting.html
    """
    if not get_graph_easy():
        return
    exclude = 'xxx'
    if not flow:
        return
    depth = depth or FLG.plot_depth
    if not depth:
        return
    cur_depth += 1
    if cur_depth > depth:
        return

    if not ctx:
        ctx = init_ctx(**dict(locals()))

    for z, ops in sorted(ctx['zs'].items()):
        if z in ctx['have_z']:
            continue
        try:
            zop = ctx['by_id'][z]
        except Exception as ex:
            zop = {'plot': {'type': 'subflow'}}
        if z_match and z != z_match:
            continue
        if not z_match:
            try:
                zop['plot']['type']
            except Exception as ex:
                print('breakpoint set')
                breakpoint()
                keep_ctx = True
            if zop['plot']['type'] == 'subflow':
                continue
            if ctx['all_tabs'] and not z == 'all_tabs':
                continue
        ctx['have_z'].append(z)
        g = draw_ops_z_group(ops, ctx, cur_depth)
        ctx['out_zs'].append([zop['plot']['layout'].box_title(), g])
        # shw(g)
    if z_match:
        return
    plot = {'svg': plot_svg, 'boxart': plot_boxart, 'src': plot_src}[FLG.plot_mode]
    if no_print:
        f = io.StringIO()
        with redirect_stdout(f):
            plot(ctx)
        return f.getvalue()
    return {FLG.plot_mode: plot(ctx)}


# def wrap_into_group(group_id, plot, ctx):
#     op = ctx['by_id'][group_id]
#     opl = op['plot']['layout']
#     r = '( %s \n %s \n ) %s' % (opl.box_title(), plot, opl.node_layout(),)
#     return r


def draw_ops_z_group(ops, ctx, cur_depth):
    """group of ops, e.g. on a tab or of a subflow"""
    by_id = ctx['by_id']
    o = []
    for op in ops:
        d = []
        frm = set_dflt(op, 'box', new_box, op, ctx)
        if op['plot']['type'] == 'subflow_inst':
            draw(ctx['flow'], ctx, z_match=op['plot']['subflow'], cur_depth=cur_depth)

        for w in op['plot']['wires_flat']:
            t = by_id[w]
            d.append(wire_con(op, t, ctx))

        if op['id'] in ctx['add_outs']:
            t = dict(op)
            t['wires'] = []
            t['type'] = 'secondary_nr_out'
            t['id'] = 'scnd_' + op['id']
            t = new_op(t, ctx)
            d.append(wire_con(op, t, ctx))

        if ctx['all_tabs']:
            if op['type'] == 'link out':
                for w in op.get('links', ()):
                    t = by_id[w]
                    d.append(link_con(op, t, ctx))

        if not d:
            d = [frm]

        o.extend(d)
    o = '\n'.join(o)
    return o


def new_box(op, ctx):
    r = op['plot']['layout'].draw()
    return r


def wire_con(frm, to, ctx):
    to_box = set_dflt(to, 'box', new_box, to, ctx)
    return '%s -> %s' % (frm['plot']['box'], to_box)


def link_con(frm, to, ctx):
    to_box = set_dflt(to, 'box', new_box, to, ctx)
    return '%s -> %s' % (frm['plot']['box'], to_box)


def add_conn(op, d):
    breakpoint()  # FIXME BREAKPOINT


def graph_opts(direction=None):
    d = direction or FLG.plot_direction
    d = {'auto': 'east'}.get(d, d)
    m = 'graph { flow: %s; ' % d
    # breaks unicode - we do it in title:
    # if FLG.plot_max_label_width:
    #     m += 'autolabel: %s; ' % FLG.plot_max_label_width
    return m + '}'


# ------------------------------------------------------------------------------ boxart
is_stdout = lambda fn: fn in ('stdout', '-')


def run_plot_sync(ctx, fn, as_='boxart', _tab=None, cb=None):
    params = dict(locals())
    params.pop('cb')
    params.pop('_tab')

    go = ctx['graph_opts']
    for tab, spec in ctx['out_zs']:
        if _tab and tab != _tab:
            continue
        spec = go + '\n' + spec
        cmd = "echo '%s'" % spec
        if not as_ == 'src':
            cmd += '| "%s" --as=%s 2>/dev/stdout' % (get_graph_easy(), as_)
        # TODO: Popen, PIPE:
        out = os.popen(cmd).read()
        # cb: checks for too wide the first run and changes plot direction if so:
        cb(tab, out, **params) if cb else write_plot(tab, out, fn, params['as_'])


def write_plot(tab, plot, fn, as_):
    hp = FLG.plot_tab_header_prefix
    if not as_ == 'src' and hp:
        plot = FLG.plot_tab_header_prefix + tab + '\n\n' + plot
    if is_stdout(fn):
        print('\n%s\n' % plot)
    else:
        with open(fn, 'a') as fd:
            fd.write(plot)


import json


def run_plot(ctx, as_, cb=None):
    fn = FLG.plot_destination
    # an indirection to get varying graph files for multiple drawings per run (e.g. pre/post build)
    fn = fn.replace('_plot_tag_', ctx['tag'])
    create = (FLG.plot_destination_create_dir,)
    if not is_stdout(fn):
        hint = 'ususally done by cfl.document, via flags argument'
        app.info('FLG.plot_destination set to file', fn=fn, hint=hint)
        d = os.path.dirname(os.path.abspath(fn))
        if not os.path.exists(d):
            if not create:
                raise Exception('Directory not present: %s' % d)
            os.makedirs(d)
        if os.path.exists(fn):
            os.unlink(fn)
        w = FLG.plot_write_flow_json
        if w and w in fn:
            with open(fn + '.flows.json', 'w') as fd:
                fd.write(json.dumps([i for i in ctx['flow']], indent=2))

    plot = partial(run_plot_sync, as_=as_, ctx=ctx, fn=fn, cb=cb,)
    if FLG.plot_sync_mode:
        return plot()
    from threading import Thread

    Thread(target=plot).start()


def fits_termwidth(plot, w=None):
    w = w or termwidth() or FLG.plot_boxart_maxwidth_fallback
    l = plot.splitlines()
    while l:
        if len(l.pop(0)) > w:
            return False
    return True


def plot_boxart(speclines):
    """On auto we try first then change direction to south if too small """

    def handle_too_wide(tab, plot, direction, max_width, **params):
        if direction == 'south' or max_width == -1 or fits_termwidth(plot, max_width):
            return write_plot(tab, plot, params['fn'], params['as_'])
        params['ctx']['graph_opts'] = graph_opts(direction='south')
        return run_plot_sync(_tab=tab, **params)

    htw = partial(
        handle_too_wide,
        direction=FLG.plot_direction,
        max_width=FLG.plot_boxart_maxwidth,
    )
    return run_plot(speclines, as_='boxart', cb=htw)


def plot_src(speclines):
    return run_plot(speclines, as_='src')


# --------------------------------------------------------------------------------- svg
def plot_svg(ctx):
    return run_plot(ctx, as_='svg')
