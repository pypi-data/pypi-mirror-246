#!/usr/bin/env python
"""
Arranges calculated flows

For the graphviz layout we need to start this in a dedicated python environ (conda resource graphviz)
"""
import json, os, sys, importlib


try:
    have_pygraphviz = importlib.import_module('pygraphviz')
except ImportError as ex2:
    have_pygraphviz = False

try:
    # because of potential subproc with graphviz:
    from devapp.tools import (
        FLG,
        define_flags,
        project,
        read_file,
        parse_kw_str,
        write_file,
        exists,
    )
    from devapp.app import app, do, system
except ImportError as ex:
    pass

from theming.formatting.markdown import deindent
from operator import setitem as set_
from tempfile import NamedTemporaryFile as TF

env = os.environ

dflt_layout = 'internal'


class Flags:
    autoshort = 'a'

    class flow_layout:
        n = '''Choose a node arranger.'
            internal    |i : Simply offsetting algo.
            event_chains|ec: Simple source to sink following
            graph_easy  |ge: Transferring graph_easy renderings into NodeRED x,y
                             Note: ge is optimized for terminal (asciiart)
            graphviz    |gv: Using pygrapheasy to get x,y
            '''
        t = [
            'i',
            'internal',
            'ec',
            'event_chains',
            'gv',
            'graphviz',
            'ge',
            'graph_easy',
        ]
        d = dflt_layout

    class flow_layout_options:
        n = '''Parametrize the layouter. Format: "k1=v1 k2=v2" or json.
        Example: -flo "flow=east" (for graph_easy)

        Say -flo h to get help about the options understood by a specific engine. 
        '''
        d = ''


try:
    # because of potential subproc with graphviz:
    define_flags(Flags)
except:
    pass

aliases = {'gv': 'graphviz', 'ge': 'graph_easy', 'i': 'internal', 'ec': 'event_chains'}


def layout(mode=None):
    l = FLG.flow_layout if mode is None else mode
    l = FLG.flow_layout if FLG.flow_layout != Flags.flow_layout.d else l
    return aliases.get(l, l)


def verify_engine_availability():
    l = layout()
    if FLG.flow_layout_options in ('h', '-h', 'help'):
        if l == 'graphviz':
            print(deindent(GV.__doc__))
        if l == 'graph_easy':
            print(deindent(GE.__doc__))
        else:
            print('no help available - no options')
        sys.exit(0)
    p = project.root(no_fail=True)

    def check():
        if l in ['internal', 'event_chains']:
            return

        if l == 'graphviz':
            return not have_pygraphviz

    err = check()
    if not err:
        return

    def die(pkg=l, rsc=l):
        m = 'Use ops project command to install %s as local resource' % rsc
        app.die('Install %s' % pkg, hint=m)

    if not p:
        die()

    if l == 'graphviz':
        s = GV.env_act_cmd()
        cmd = s + 'python -c "import pygraphviz; print(pygraphviz.__file__)"'
        r = os.popen(cmd).read()
        if r:
            app.info('Detected graphviz python env', env=r.split('/lib/', 1)[0])
            return
        die('pygraphviz', 'graphviz')


def arrange_xy(flow, mode=None, **kw):
    l = layout(mode)
    flow = list(flow)
    f = {
        'internal': auto_arrange,
        'event_chains': arrange_by_evt_chains,
        'graph_easy': GE.arrange,
        'graphviz': GV.arrange,
    }.get(l)
    if not f:
        app.die('flow layout method not supported', mode=l, **kw)
    m = parse_kw_str(FLG.flow_layout_options)
    m.update(kw)
    return f(flow, **m)


# ----------------------------------------------------------------- globals during calc
class S:
    by_id = None  # all ops by their id
    wire_dests = None
    srcs = None
    processed = None


no_z_types = set(['websocket-listener', 'tab', 'subflow'])


def set_globals(flow):
    S.by_id = dict([(n['id'], n) for n in flow])
    S.wire_dests = set([id for N in flow for w in N.get('wires', []) for id in w])
    S.srcs = [
        op
        for op in flow
        if not op['id'] in S.wire_dests and not op['type'] in no_z_types
    ]
    S.processed = set()


# --------------------------------------------------------------------- graph_easy


class GE:
    """Graph Easy Layouter


    - Requires graph_easy with svg extension
    - Available as resource

    Options:
    - flow=[north|east|south|west]

    See: http://bloodgate.com/perl/graph/manual/hinting.html
    """

    def get_ge_xy(id, p):
        l = p.split(' %s ' % id)
        if len(l) < 2:
            return
        if len(l) > 2:
            app.die('Multiple Id problem', id=id)
        pre = l[0]
        lt = pre.split('\n')
        x = len(lt[-1])
        y = len(lt)
        return x, y

    def arrange(flow, **kw):
        """
        Suboptimal: Graph easy makes cornered wires, NR makes Beziers from left ->
        lots of crossings..."""
        set_globals(flow)
        # m = {op['id']: 'id:%s' % i for i, op in zip(range(len(flow)), flow)}
        # M = {v: k for k, v in m.items()}
        pd = kw.get('flow', 'east')
        ge = ['graph { flow: %s; }' % pd]
        for op in flow:
            attr = ''
            if not op['id'] in S.wire_dests or 1:
                # via this we try align sources a bit:
                attr = ' { start: %s; } ' % pd
            for w in op.get('wires', []):
                for d in w:
                    ge.append('[ %s ] -> %s [ %s ]' % (op['id'], attr, d))
        from devapp.tools import project

        with TF() as fp:
            fp.write('\n'.join(ge).encode('utf-8'))
            fp.seek(0)
            G = project.root() + '/bin/graph-easy --as=boxart'
            g = os.popen('cat "%s" | %s' % (fp.name, G)).read()

        app.info('Replacing xy with graph_easy output')
        for op in flow:
            xy = GE.get_ge_xy(op['id'], g)
            if not xy:
                continue
            op['x'] = xy[0] * 10
            op['y'] = xy[1] * 20


# --------------------------------------------------------------------- python arranger

# the one we use by default in tests


def auto_arrange(flow, **kw):
    """x incr. left to right, y incr. top to bottom"""
    set_globals(flow)
    for tab in set([t['id'] for t in flow if t['type'] == 'tab']):
        nodes_on_tab = [t for t in flow if t.get('z') == tab]
        auto_arrange_on_tab(nodes_on_tab)
    return flow


def auto_arrange_on_tab(nodes):
    inputs = [n for n in nodes if not n['id'] in S.wire_dests]
    x = 0
    y = 100
    if not inputs:
        app.warn('No inputs - cannot auto arrange', json=nodes)
    for n in inputs:
        x += 200
        auto_arrange_flow(n, x, y)


def auto_arrange_flow(n, x, y):
    """recursive, we go down he wires"""
    if not n.get('z') or n.get('type') == 'tab':
        # cfg object
        return
    n['x'] = n.get('x', x - 50) + 50
    n['y'] = y
    # japp.info(n['id'])
    for w in n.get('wires', ()):
        for d in w:
            app.debug('arranging wire', wire=d, n=n)
            y += 100
            try:
                auto_arrange_flow(S.by_id[d], x, y)
            except Exception as ex:
                app.error(
                    str(ex) + ' could not arrange flow (check your wires)', d=d, **n
                )
                if d == '':
                    app.warn('You seem to have a loose end, i.e. a subpipe w/o a snk')
                breakpoint()  # FIXME BREAKPOINT
                print('breakpoint set')


# ------------------------------------------------------------------ evt chains arranger

DX = 250
DY = 35


def arrange_by_evt_chains(flow, **kw):
    """
    Build from sources to the right, going down with new parallel ops after a branch

    ev1 -> ax-cond -> act1.1 -> act1.2 -> snk1.1
    ev2 ->                             -> snk1.2
    ev3 ->         -> act2.1 -> act2.2 -> snk2.1
                                        
    """
    set_globals(flow)
    y = DY
    for src in S.srcs:
        x = DX
        y = build_chain(frm=src, x=x, y=y)


def build_chain(frm, x, y):
    # if frm['type'] == 'debug':
    #     breakpoint()  # FIXME BREAKPOINT
    if frm['id'] in S.processed:
        return y
    S.processed.add(frm['id'])
    frm['x'] = x
    frm['y'] = y
    for w in frm.get('wires', []):
        for d in w:
            y = build_chain(S.by_id[d], x + DX, y)
            y += DY
    return y


class GV:
    """Graphviz Layouter

    - Requires graphviz and pygraphviz either in current python env or
      installed as resource - we'll switch to its python env and comm.
      via a file
    - Available as resource

    Options:
    - write_svg=<fn>: Will save an svg for inspection

    See: https://www.graphviz.org/
    """

    env_act_cmd = lambda: 'set -a; . "%s/bin/dot" && ' % project.root()

    def run_in_graphviz_env():
        assert have_pygraphviz
        fn = sys.argv[-1]
        with open(fn) as fd:
            s = json.loads(fd.read())
        svg = GV.run_pygraphviz(s['flow'], **s['opts'])
        with open(fn + '.svg', 'w') as fd:
            fd.write(svg.decode('utf-8'))

    def run_pygraphviz(flow, **kw):
        pgv = have_pygraphviz
        A = pgv.AGraph(directed=True, strict=True, rankdir='LR', rank='same')
        A.graph_attr['epsilon'] = '0.001'
        nodelist = [op['id'] for op in flow if op.get('z')]
        # A.add_nodes_from(nodelist)
        for op in flow:
            if op['id'] in nodelist:
                for w in op.get('wires', []):
                    for d in w:
                        A.add_edge(op['id'], d)

        A.layout(prog='dot')
        svg = A.draw(format='svg')
        return svg

    def arrange(flow, **kw):
        """entry from devapp"""
        set_globals(flow)

        if have_pygraphviz:
            svg = run_pygraphviz(flow, **kw)
        else:
            with TF() as fd:
                fd.write(json.dumps({'opts': kw, 'flow': flow}).encode('utf-8'))
                cmd = GV.env_act_cmd() + 'python %s run_graphviz "%s"'
                # calling us within the env:
                cmd = cmd % (__file__, fd.name)
                # we want stdio: Todo: check multiprocessing for that
                err = os.system(cmd)
                fn = fd.name + '.svg'
                svg = read_file(fn, dflt='')
                # write_file('/tmp/foo.svg', svg)
                if err or not svg:
                    app.die('SVG creation in subprocess failed')
                if exists(fn):
                    os.unlink(fn)

                # os.unlink(fd.name + '.svg')
        fn = kw.get('write_svg')
        if fn:
            write_file(fn, svg)
            app.info('Written', fn=fn)
        GV.set_xy_from_svg(flow, svg)
        GV.pan_and_stretch(flow, **kw)
        return flow

    def set_xy_from_svg(flow, svg):
        import io
        import xml.etree.ElementTree as ET

        xy = set(['x', 'y'])

        f = io.StringIO(svg)
        tree = ET.parse(f)
        for el in tree.getroot().getchildren()[0].getchildren():
            if not ('class', 'node') in el.items():
                continue
            for c in el.getchildren():
                if 'x' in c.keys():
                    d = {k: int(float(v)) for k, v in c.items() if k in xy}
                    if not d:
                        app.die('svg format error')
                    try:
                        S.by_id[el.getchildren()[0].text].update(d)
                    except Exception as ex:
                        print('breakpoint set')
                        breakpoint()
                        keep_ctx = True

    def pan_and_stretch(flow, **kw):
        minx = min(op.get('x', 0) for op in flow)
        miny = min(op.get('y', 0) for op in flow) - 20
        lx, ly = kw.get('lx', 2), kw.get('ly', 2)
        for op in flow:
            if op.get('x'):
                op['x'] -= minx
                op['y'] -= miny
                op['x'] = int(op['x'] * lx)
                op['y'] = int(op['y'] * ly)


if __name__ == '__main__':
    if 'run_graphviz' in sys.argv:
        GV.run_in_graphviz_env()
