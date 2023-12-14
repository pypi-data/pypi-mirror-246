"""
Parsing RFC Textual State Tables into flows and python modules

https://tools.ietf.org/html/rfc6733#page-68

state            event            action           next state
-----------------------------------------------------------------
Closed           Start            I-Snd-Conn-Req   Wait-Conn-Ack
                 R-Conn-CER       R-Accept,        R-Open
                                  Process-CER,
                                  R-Snd-CEA

Wait-Conn-Ack    I-Rcv-Conn-Ack   I-Snd-CER        Wait-I-CEA
                 I-Rcv-Conn-Nack  Cleanup          Closed
                 R-Conn-CER       R-Accept,        Wait-Conn-Ack/
                                  Process-CER      Elect
                 Timeout          Error            Closed

"""
from devapp.app import run_app, do, app, system
from devapp.tools import FLG, autoshort, exists, read_file, write_file, reverse_dict
from devapp.tools import gitcmd
from theming.formatting.markdown import deindent
from importlib import import_module
from node_red import http_api as api
from node_red import nr_node_arranger
from ast import literal_eval as liteval
from json import dumps, loads
from collections import OrderedDict as D
from functools import partial
from operator import setitem
import importlib
import inspect
import time
import sys

F = nr_node_arranger.Flags
F.flow_layout.d = 'graphviz'


class Flags:
    autoshort = ''

    class file_name_state_table:
        n = '''Absolute or relative state file name.
        Must be an ASCII table, e.g. copied from an RFC.
        '''
        d = ''

    class event_sources:
        n = 'Event sources generated. Internal means we will subscribe to subjects'
        t = ('inject', 'internal', 'http')
        d = 'inject'

    class subflow:
        n = 'Wrap the flow into a subflow template - specify (regex) the nodes which should be wired to out.\n'
        n += "Example: -s '\.Process$' - matches every operator ending with '.Process'"
        d = ''

    class create_debug_output_node:
        d = True

    class name_tab:
        d = 'State Table Flow in Node RED'

    class flow_output:
        n = '''Absolute or relative file_name to write created flow to - or direct hub upload options.
        - -(dash): Print to stdout
        - hub:r  : Upload to hub, replacing conflicting ids
        - hub    : Upload to hub, delete all on given tab name
        - hub:c  : Upload to hub, clearing everything(!), before upload
        - (empty): No flow file produced

        '''
        d = '-'

    class file_name_svg:
        n = 'filename of svg if it should be written'
        d = ''

    class py_file_name_mod:
        n = 'Absolute or relative file_name of produced python module (- for stdout. Empty: No pymod created).'
        n += '\nIf the file exists we perform a merge of old and new file - so you should be able to add custom code.'
        d = ''

    class py_build_test:
        n = 'Create also a test module (only when py_file_name_mod is given)'
        d = False

    class py_file_name_mod_template:
        n = 'Absolute or relative template file to use'
        d = 'multi_instance.py'

    class py_name_obj:
        d = 'Name of python class to create in pymod. Root of all functions.'
        d = 'obj'

    class py_subs_action_hirarchy:
        n = '''Regex to build an action hirarchy instead of all actions flat.

        Example: Given action names "I_act_1" then supply '^I_,I.' to get "I.act_1", 
                 which creates a hirarchy:
                     class I:
                        def act_1(data, msg):
                            (...)
        '''
        t = 'multi_string'

    class py_file_name_postprocessor_mod:
        n = 'name of module which contains a `def post_process_flow`'
        d = ''


g = getattr


class S:
    obj = None  # name of object
    argv = None  # clie
    states = {}  # all infos
    events = D()  # by order
    actions = D()  # just for looping
    transitions = {}  # used in pymod for asserts
    ctime = time.ctime()
    start_state = None
    statefile = None
    statefile_content = None
    # while pymod building:
    action = action_id = action_table = action_functions = obj = None
    flow = []


# -------------------------------------------------------------------------Table Parser
cols = dict(state=0, event=0, action=0, next_state=0)


def get_cell(k, l):
    p = cols[k]
    if l[p] == ' ':
        return ''
    return l[p:].split()[0]


def get_cell_wipe(k, l, lines):
    """
    Modifies lines with whitespace where continuotions had been:

    Example:
    k = 'next_state'
    l =      '        R-Conn-CER       R-Accept,        Wait-Conn-Ack/     '
    lines = ['                         Process-CER      Elect              ', ...]

    then we return 'Wait-Conn-AckElect' and modify lines to: 
    lines = ['                         Process-CER                         ', ...]
    i.e. with the second line value wiped away
 
    """
    v = get_cell(k, l)
    if not v:
        return v
    i = 0
    while v[-1][0] in ('/', ','):
        l = lines[i]
        vn = get_cell(k, l)
        # replace it with spaces (wipe) in lines
        p = cols[k]
        sp = ' ' * len(vn)
        lines[i] = l[:p] + sp + l[p + len(sp) :]
        v += vn
        i += 1
    return v.replace('/', '')


def parse_block(state, block):
    B = S.states[state]
    while block:
        l = block.pop(0)
        ev = get_cell_wipe('event', l, block)
        if ev:
            if not ev in S.events:
                S.events[ev] = {'states': [state]}
            else:
                S.events[ev]['states'].append(state)

            acts = []
            B['events'][ev] = m = {'actions': acts}
            a_ = get_cell_wipe('action', l, block).split(',')
            a_ = act_subs(a_)  # I_foo -> I.foo
            acts.extend(a_)
            m['next_state'] = get_cell_wipe('next_state', l, block)
            [setitem(S.actions, a, True) for a in acts]  # just remember those


import re


def prepare_parse_py_subs_action_hirarchy_regexes():
    S._subs = r = []
    for s in FLG.py_subs_action_hirarchy:
        if s:
            l = s.split(',')
            r.append([re.compile(l[0]), l[1]])


def act_sub(a):
    for frm, to in S._subs:
        a = frm.sub(to, a)
    return a


def check_no_namespace_collisions():
    """
    Foo.Process and we already have Foo.Process.Bar -> NS Collision!
    User has to resolve manually, in the state table. 
    """
    l = S.actions
    for A in l:
        r = [k for k in l if k.startswith(A + '.')]
        if r:
            f = r[0].split('.')[0]
            h = {
                'colliding': {'Class Hirarchy': r[0], 'Action Function': f},
                'hints': [
                    'Possible resolutions:',
                    'Create the hirarchy differently.',
                    'Or append a _ behind the func or within the class!',
                ],
            }
            app.die('Namespace Collision!', json=h)


act_subs = lambda acts: [act_sub(a) for a in acts]


def parse_state_table_file(fn):
    s = read_file(fn, dflt='').replace('-', '_')
    if not s:
        return app.die('not found', fn=fn)
    S.statefile = fn
    return parse_state_table(s)


def parse_state_table(s):
    """
    - One word per cell
    - ---- lines allowed (removed)
    - Left spaces allowed
    - / line sep allowed
    - First row MUST be header with those names: state, event, action, next_state
      and their aligment must be left of columns!

    Example:

        state            event            action           next_state
        -----------------------------------------------------------------
        Closed           Start            I-Snd-Conn-Req   Wait-Conn-Ack
                         R-Conn-CER       R-Accept,        R-Open
                                          Process-CER,
                                          R-Snd-CEA

        Wait-Conn-Ack    I-Rcv-Conn-Ack   I-Snd-CER        Wait-I-CEA
                         I-Rcv-Conn-Nack  Cleanup          Closed
                         R-Conn-CER       R-Accept,        Wait-Conn-Ack-/
                                          Process-CER      Elect
                         Timeout          Error            Closed

    """

    def parse_header_line_for_cols(l):
        entries = 'state', 'event', 'action', 'next_state'
        for k in entries:
            cols[k] = l.index(k)

    S.statefile_content = s = deindent(s).lstrip()
    # clean:
    orig_lines = [l for l in s.splitlines() if l.strip() and l[0] not in ('#', '_')]
    header = orig_lines.pop(0)
    parse_header_line_for_cols(header)
    orig_lines = [l + ' ' * len(header) for l in orig_lines]

    def get_state_blocks(lines):
        blocks = {}
        while lines:
            l = lines.pop(0)
            if l[0] != ' ':
                block = []
                state = get_cell_wipe('state', l, lines)
                S.states[state] = {'events': {}}
                blocks[state] = block
            block.append(l)
        return blocks

    blocks = get_state_blocks(list(orig_lines))

    for state, block in blocks.items():
        if not S.start_state:
            S.start_state = state
        parse_block(state=state, block=block)

    app.info(
        'Parsed state table',
        events=len(S.events),
        states=len(S.states),
        actions=len(S.actions),
    )
    return s


def sort_dicts(*dicts):
    for k in dicts:
        m = {}
        v = getattr(S, k)
        m.update(v)
        v.clear()
        for k in sorted(m):
            v[k] = m[k]


def add_by_id_dicts(*dicts):
    for k in dicts:
        # k: events, actions, states
        v = getattr(S, k)
        # id_by_state, not id_by_stateS
        k = k[:-1] if k.endswith('s') else k
        m = {i: s for i, s in zip(range(len(v)), v)}
        setattr(S, '%s_by_id' % k, m)
        setattr(S, 'id_by_%s' % k, reverse_dict(m))


def add_transitions_table():
    """A big table of ids, for fast assertions against data in py funcs
        (Pdb) pp S.transitions
        {0: {11: [16, 13, 19, 5], 21: [6, 1]},
         1: {3: [5, 2], 4: [0, 0], 11: [16, 13, 3], 23: [2, 0]},
         2: {...
    """

    def act_ids(am):
        # am like {'actions': ['I_Snd_Conn_Req'], 'next_state': 'Wait_Conn_Ack'}
        r = [S.id_by_action[a] for a in am['actions']]
        r.append(S.id_by_state[am['next_state']])
        return r

    _ = S.transitions
    for k, v in S.states.items():
        _[S.id_by_state[k]] = {
            S.id_by_event[k1]: act_ids(a) for k1, a in v['events'].items()
        }


def add_misc_infos():
    S.obj = FLG.py_name_obj
    S.cli = ' '.join(sys.argv)
    gi = gitcmd(os.path.dirname(__file__))
    try:
        S.parser_rev = '%(url)s@%(cmd)s' % gi
        S.gitrev = gi['cmd']
    except Exception:
        S.parser_rev, S.gitrev = ('n.a.',) * 2


# ------------------------------------------------------------------------------- Flows


def tab_nz():
    n = z = FLG.name_tab
    z = z.lower().replace(' ', '.')
    return n, z


def add_z():
    n, z = tab_nz()
    for op in S.flow:
        op['z'] = z
    S.flow.insert(0, {'type': 'tab', 'id': z, 'label': n})


def serialize_inner_structs():
    l = ['condition', 'kw', 'port_labels']
    for op in S.flow:
        for k in l:
            c = op.get(k)
            if c is not None and isinstance(c, (dict, list, tuple)):
                op[k] = dumps(c)


class EvtSources:
    ev_src_ops = lambda typ, evt, dest: dict(
        inject={
            'id': evt + '.inj',
            'type': 'inject',
            'name': evt,
            'props': [{'p': 'ev_' + S.obj, 'v': S.id_by_event[evt], 'vt': 'num'}],
            'once': False,  # MUST - NR failes otherwise!
            'repeat': '',
            'crontab': '',
            'onceDelay': 0.1,
            'topic': '',
            'wires': [[dest]],
        },
        http={
            'id': 'evts.http_in',
            'type': 'http in',
            'name': 'events',
            'url': '/event',
            'method': 'get',
            'wires': [],
        },
    ).get(typ)

    def add():
        Eops = EvtSources.ev_src_ops
        root = [op for op in S.flow if op['type'] == 'ax-src']
        assert len(root) == 1
        w = root[0]['wires'][0][0]
        S.event_sources = E = []
        add_debug = False
        for k in FLG.event_sources:
            if k in ('inject', 'internal'):
                add_debug = True
                for e in S.events:
                    E.insert(0, Eops('inject', e, w))
                    # one event to get a stream, todo: better an ax-src
                    if k == 'internal':
                        add_debug = False
                        break

        snk = [op for op in S.flow if op['type'] == 'ax-snk']
        assert len(snk) == 1
        S.flow.extend(E)
        # when there are injects the user wants also a debug node ususally:
        if add_debug:
            id = 'deb_' + snk[0]['id']
            EvtSources.add_debug(id)
            snk[0]['type'] = 'ax-op'
            snk[0]['wires'] = [[id]]

    # def add_source_next_event():
    #     f = S.flow
    #     bs = by(name='by_state')[0]
    #     n = S.obj + '.next_event'
    #     f.insert(2, {'type': 'ax-src', 'name': n, 'id': n, 'wires': [[bs['id']]]})

    def add_debug(id):
        op = {
            'type': 'debug',
            'name': id,
            'active': True,
            'console': True,
            'tostatus': True,
            'wires': [],
            'id': id,
        }
        S.flow.append(op)
        return op

    def wrap_into_subflow(spec):
        n = S.obj
        # sinks = ['ax-snk', 'debug']
        # for op in snks:
        #     op['x'] = 800  # nice and centered right the outs
        #     op['y'] = 500
        srcs = S.event_sources
        _, z = tab_nz()
        sfid = 'sf%s' % n
        sfiid = 'sfi%s1' % n
        out_ops = [op for op in S.flow if re.search(spec, op.get('name', ''))]
        outs = []
        for op in out_ops:
            op['wires'] = []
            outs.append({'id': op['id'], 'port': 0})
        maxx = max([op.get('x', 0) for op in S.flow])
        op_by_state = _ = [op for op in S.flow if op['id'] == n + '_by_state'][0]
        x, y = _['x'], _['y']
        dbg = EvtSources.add_debug('sf_debug_' + S.obj)
        dbg['x'], dbg['y'] = 400, 400
        new = [
            {
                'id': sfid,
                'type': 'subflow',
                'name': n,
                'in': [{'x': x - 300, 'y': y, 'wires': [{'id': op_by_state['id']}]}],
                'out': [{'x': maxx + 200, 'y': y, 'wires': outs}],
            },
            {
                'id': sfiid,
                'type': 'subflow:%s' % sfid,
                'z': z,
                'name': '%s1' % n,
                'env': [],
                'x': 500,  # centered the instance
                'y': 500,
                'wires': [[dbg['id']]],
            },
        ]
        for op in S.event_sources:
            op['wires'] = [[sfiid]]
        for op in S.flow:
            if op.get('z') and op['z'] == z and not op in srcs:
                op['z'] = sfid
        dbg['z'] = z
        new[-1]['z'] = z
        S.flow.extend(new)


def action_chain(ev, state):
    id = state + '.' + ev
    m = S.states[state]['events'][ev]
    actions = m['actions']
    # actions.append(m['next_state'])
    c = []
    next_aid = 'set_state.' + m['next_state']
    for a in reversed(actions):
        aid = id + '.' + a
        n = S.obj + '.act.' + a
        c.insert(0, ({'type': 'ax-op', 'id': aid, 'name': n, 'wires': [[next_aid]]}))
        next_aid = aid
    for op in reversed(c):
        S.flow.append(op)
    return c


# ------------------------------------------------------------------------- Results Out
class Out:
    def flow(fn):
        if fn.startswith('hub:') or fn == 'hub':
            if fn == 'hub:r':
                nr_clear = 'ids'
            elif fn == 'hub':
                nr_clear = 'tab:%s' % tab_nz()[1]
            elif fn == 'hub:c':
                nr_clear = 'full'
            else:
                app.die('hub clear mode not understood', hint='help via -h')
            api.upload_flows(S.flow, nr_clear=nr_clear, ensure_hub=True)
        else:
            Out.write('flow', fn, dumps(S.flow, indent=2))

    def pymod(fn, s, prefix_with=''):
        fn = PyTmplCtx._with_ext(fn)  # adds a .py
        fn = Out.write('python module', fn, s, prefix_with=prefix_with)

    def get_fn(fn, prefix_with=''):
        return prefix_with + fn

    def format(fn):
        if not os.system('type black'):
            app.info('Autoformatting with black')
            do(system, 'black "%s"' % fn)
        return fn

    def write(what, fn, s, prefix_with=''):
        if not fn:
            return app.info('No write', what=what)
        if fn == '-':
            return print(s)
        fn = Out.get_fn(fn, prefix_with=prefix_with)
        if not fn.endswith('.py') or not exists(fn):
            write_file(fn, s)
            return Out.format(fn)

        # merge
        pre = 'new_'
        app.info('Trying to merge with existing file', fn=fn)
        os.unlink('old_' + fn) if exists('old_' + fn) else 0
        os.unlink(fn + '.backup') if exists(fn + '.backup') else 0
        app.info('Backing up into', fn=fn + '.backup')
        do(system, 'cp "%s" "%s.backup"' % (fn, fn))
        do(system, 'mv "%s" "old_%s"' % (fn, fn))
        write_file(pre + fn, s)
        Out.format(pre + fn)

        cmd = (
            'diff -DxxVERSION1xx --minimal --ignore-all-space -B "old_%s" "new_%s" > "%s"'
            % (fn, fn, fn,)
        )
        ec = os.system(cmd)
        app.info('Merged', cmd=cmd, exit_code=ec)
        if ec == 2:
            app.error('Merging failed - check back up', fn=fn, fn_old=fn + '.backup')
        os.unlink('old_' + fn)
        os.unlink('new_' + fn)
        s = [l for l in read_file(fn).splitlines() if not 'xxVERSION1xx' in l]
        write_file(fn, '\n'.join(s))
        app.info('have merged %s' % what, fn=fn)
        return fn


# ---------------------------------------------------------- Building the python module
import os


class PyTmplCtx:
    """
    We create a lot of infos which is useful in templates

    All attrs of the state class S are replaced into templates like this:

    S.foo = 'bar' ->  "_FOO_" in template will be turned into "bar"
    if bar is dict we also build an assigment list variable:
    S.foo_assigns = 'i=1;j=2' ->  "_FOO_ASSIGNS_" gets the list
    (IDE aligns at first open, but we try also to convert using black)

    In templates we search for  t_py_mod and t_action funcs and replace their source.

    That allows IDE assisted template editing.
    """

    _mark_rm_from_here = ' # -- rm'
    _with_ext = lambda s: s if s.endswith('.py') else s + '.py'
    _empty_pth = tuple([c for c in '!' * 100])

    # as parsed:
    states = events = actions = None

    class repl:
        pass

    @classmethod
    def import_template(Py):
        dn = os.path.dirname
        fn = Py._with_ext(FLG.py_file_name_mod_template)
        modn = fn.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        dirs = './', dn(__file__) + '/pymod_templates/', ''
        for dir in dirs:
            if exists(dir + fn):
                break
        if not os.path.exists(dir + fn):
            app.die('Template not found', fn=fn, in_dirs=dirs)
        fn = os.path.abspath(dir + fn)
        S.mod_template = fn
        sys.path.insert(0, dn(fn))
        tmod = importlib.import_module(modn)
        return tmod

    @classmethod
    def add_inner_classes(Py, add, cur_pth, action):
        clss = action.split('.')
        ind = len(clss) - 1
        for i in range(0, ind):
            if clss[i] != cur_pth[i]:
                add(' ' * 4 * i + 'class %s:' % clss[i])
        return tuple([i for i in clss[:-1]]) + Py._empty_pth

    @classmethod
    def build_module(Py):
        S.tmod = TM = do(Py.import_template)
        afs = []
        add = afs.append
        # action template
        AT = Py.tmpl('t_action')
        if AT:
            cur_pth = Py._empty_pth
            for a in S.actions:
                cur_pth = Py.add_inner_classes(add, cur_pth, a)
                # parts = a.split('.')
                # for i in range(len(parts)-1):
                #     if parts[i]
                # for p in parts[:-1]:

                # for p in a.split('.')[:-1]

                S.action = a
                S.action_func = a.rsplit('.', 1)[-1]
                S.action_id = S.id_by_action[a]
                S.action_table = Py.make_action_table(a)
                ind = len(a.split('.')[:-1]) * ' ' * 4
                s = Py.replace_template(AT)
                s = ind + s.replace('\n', '\n' + ind)
                add(s)
        S.action_functions = '\n\n'.join(afs)
        s = Py.replace_template(Py.tmpl('t_py_mod'))
        app.info('Python module built')
        return s

    @classmethod
    def tmpl(Py, name):
        at = getattr(S.tmod, name, None)
        return inspect.getsource(at) if at else None

    @classmethod
    def test_build_module(Py):
        AT = Py.tmpl('t_test')
        TF = []
        for S.state, evts in S.states.items():
            evts = evts['events']
            S.state_id = S.id_by_state[S.state]
            for e, acts in evts.items():
                S.event = e
                S.state_next = _ = acts['next_state']
                S.state_id_next = S.id_by_state[_]
                s = Py.replace_template(AT)
                TF.append(s)
        S.test_functions = '\n\n'.join(TF)
        s = Py.replace_template(Py.tmpl('t_py_test_mod'))
        app.info('Python test module built')
        return s

    @classmethod
    def make_action_table(Py, a):
        '''Useful in Docstrings of Action Functions
        Example Template:

            def t_action():
                def _ACTION_(data, msg, v=verify):
                    """
                    _ACTION_TABLE_
                    """
            v(data, _ACTION_ID_, '_ACTION_')

        Result:

            def I_Snd_Conn_Req(data, msg, v=verify):
                """
                Start =>  Closed -> Wait_Conn_Ack: I_Snd_Conn_Req
                """
                v(data, 0, 'I_Snd_Conn_Req')

            def R_Accept(data, msg, v=verify):
                """
                R_Conn_CER => 
                - Closed        -> R_Open            : R_Accept, Process_CER, R_Snd_CEA
                - Wait_Conn_Ack -> Wait_Conn_AckElect: R_Accept, Process_CER
                - Wait_I_CEA    -> Wait_Returns      : R_Accept, Process_CER, Elect
                """
                v(data, 1, 'R_Accept')
            (...)
        '''
        o = []
        add = o.append
        T = '- %s -> %s: %s'
        r = []
        evs = D()
        for st, v in S.states.items():
            for ev, chain in v['events'].items():
                acts = chain['actions']
                if a in acts:
                    evs.setdefault(ev, []).append(
                        [st, chain['next_state'], ', '.join(acts)]
                    )

        for ev, sts in evs.items():
            if not sts:
                continue
            add(ev + ' => ')
            if len(sts) == 1:
                # single lines only for only one state for that event:
                o[-1] += T[2:] % tuple(sts[0])
                continue
            # create a list of states:
            l = [max(len(k[i]) for k in sts) for i in range(3)]
            for strt, end, acts in sts:
                add(T % (strt.ljust(l[0]), end.ljust(l[1]), acts))
        return '\n'.join(o)

    noval = lambda S, k: k.startswith('_') or callable(g(S, k))

    @classmethod
    def create_dicts_assigns(Py, s):
        """Find all dict assigns and create them from dicts
        A dict assign is an assignment sequence: k1=v1; ...

        """
        m = '_DICT_ASSIGNS_'
        vs = lambda s: "'%s'" % s if isinstance(s, str) else s
        for part in s.split(m)[:-1]:
            v = part.rsplit('\n', 1)[-1].split()[-1]
            assert v[0] == '_' and v == v.upper(), 'dict assign key not valid'
            k = v[1:].lower()
            d = g(S, k)
            assert isinstance(d, dict)
            va = '; '.join(
                ['%s = %s' % (k.replace('.', '_'), vs(v)) for k, v in d.items()]
            )
            setattr(S, k + '_dict_assigns', va + Py._mark_rm_from_here)

    @classmethod
    def replace_template(Py, s):
        s = deindent(s.split('def ', 1)[1].split('\n', 1)[1])

        keys = lambda: [k for k in dir(S) if not Py.noval(S, k)]
        Py.create_dicts_assigns(s)

        # longest first:
        for k in reversed(sorted(keys(), key=len)):
            kt = '_%s_' % k.upper()
            if kt in s:
                v = g(S, k)
                v = str(v)
                if '\n' in v:
                    # find the indent of the kt keyword and index all other lines with it
                    ind = len(s.split(kt, 1)[0].rsplit('\n', 1)[-1])
                    v = v.replace('\n', '\n' + ' ' * ind)
                s = s.replace(kt, v)
        s = '\n'.join([l.split(Py._mark_rm_from_here, 1)[0] for l in s.splitlines()])
        return s


def build_tree():
    add = S.flow.append
    add(
        {
            'id': 'root',
            'type': 'ax-src',
            'name': S.obj + '.next_event',
            'wires': [['by_state']],
        }
    )
    st_conds = []
    st_ws = []
    st_ws_l = []
    add(
        {
            'id': 'by_state',
            'type': 'ax-cond',
            'name': 'by_state',
            'wires': st_ws,
            'condition': st_conds,
            'match_msg': True,
            'port_labels': st_ws_l,
        }
    )
    add({'id': 'end', 'type': 'ax-snk', 'name': 'ax.dump', 'wires': []})
    for state in S.states:
        add(
            {
                'id': 'set_state.' + state,
                'type': 'ax-op',
                'name': S.obj + '.set_state',
                'label': 'Set: ' + state,
                'icon': 'font-awesome/fa-tags',
                'kw': {'to_state': S.id_by_state[state]},
                'wires': [['end']],
            }
        )
    app.info('added %s end state setters' % len(S.states))

    for state, events in S.states.items():
        events = events['events']
        ev_state_ws = []
        ev_state_cond = []
        ev_ws_l = []
        add(
            {
                'id': state,
                'type': 'ax-cond',
                'name': state,
                'wires': ev_state_ws,
                'condition': ev_state_cond,
                'port_labels': ev_ws_l,
                'match_msg': True,
            }
        )
        st_conds.append([S.obj + '.state', 'eq', S.id_by_state[state]])
        st_ws.append([state])
        st_ws_l.append(state)

        for ev, acts in events.items():
            ev_state_cond.append([S.obj + '.event', 'eq', S.id_by_event[ev]])
            ev_ws_l.append(ev)
            c = action_chain(ev, state)
            ev_state_ws.append([c[0]['id']])


def set_ax_cond_outputs_from_wires():
    for op in S.flow:
        if op['type'] == 'ax-cond':
            op['outputs'] = len(op['wires'])


def prefix_ids_with_pyobj():
    """avoides conflicts with other nodes:
    prefix all with S.obj, e.g. 'peer_'
    """

    def prefix(op):
        op['id'] = S.obj + '_' + op['id']
        wsl = list(op.get('wires'))
        op['wires'] = [[S.obj + '_' + id for id in ws] for ws in wsl]

    [prefix(op) for op in S.flow]


from tempfile import NamedTemporaryFile as NTF


def postprocess_flow(fn):

    fn = PyTmplCtx._with_ext(fn)  # adds a .py
    s = read_file(fn, dflt='')
    if not s:
        app.die('Postprocess not found', fn=fn)
    lines = s.splitlines()
    r = []
    while lines:
        l = lines.pop(0)
        if not l.startswith('def post_process_flow('):
            continue
        while True:
            r.append(l)
            l = lines.pop(0)
            if not l.startswith(' '):
                break
        break
    if not r:
        app.die('Did not find post_process_flow function in ', fn=fn)
    app.info('Postprocessing flow', frm_file=fn)
    f = NTF(delete=False)
    fn = f.name + '.py'
    d = os.path.dirname(f.name)
    sys.path.insert(0, d)
    os.unlink(f.name)
    write_file(fn, '\n'.join(r))
    mod = import_module(f.name.rsplit('/', 1)[-1])

    class states:
        pass

    class events:
        pass

    for c, m in ((states, S.id_by_state), (events, S.id_by_event)):
        [setattr(c, k, v) for k, v in m.items()]
        [setattr(c, '_%s' % v, k) for k, v in m.items()]

    mod.post_process_flow(S.flow, by=by, st=states, ev=events)


def by(flow=S.flow, **kw):
    app.info('Searching operators', **kw)
    f = flow
    for k, v in kw.items():
        f = [op for op in f if op.get(k) == v]
    return f


# -------------------------------------------------------------------------------- Main
def run():
    nr_node_arranger.verify_engine_availability()
    do(prepare_parse_py_subs_action_hirarchy_regexes)
    fn = FLG.file_name_state_table
    do(parse_state_table_file, fn=fn)
    do(check_no_namespace_collisions)
    do(sort_dicts, 'actions', 'events')
    do(add_by_id_dicts, 'states', 'events', 'actions')
    do(add_transitions_table)
    do(add_misc_infos)  # git rev, cli line entered - for docstrings in autogen code
    do(build_tree)
    do(EvtSources.add)
    # do(EvtSources.add_source_next_event)
    do(set_ax_cond_outputs_from_wires)
    do(prefix_ids_with_pyobj)

    fn = FLG.flow_output
    if fn:
        # if 0:
        #     do(add_root_event_source)
        #     do(build_event_flows)
        #     do(insert_state_splitters)
        fnpp = FLG.py_file_name_postprocessor_mod
        if fnpp:
            flow = do(postprocess_flow, fn=fnpp)
        write_file('flows.py', str(S.flow))
        do(add_z)
        do(
            nr_node_arranger.arrange_xy,
            S.flow,
            tab=tab_nz()[1],
            lx=1.2,
            ly=1.2,
            write_svg=FLG.file_name_svg,
        )
        sf = FLG.subflow
        if sf:
            do(EvtSources.wrap_into_subflow, spec=sf)
        do(serialize_inner_structs)
        write_file('flowss.py', str(S.flow))
        import json

        write_file('foo.json', json.dumps(S.flow, indent=4))

        do(Out.flow, fn=fn)

    fn = FLG.py_file_name_mod
    if fn:
        S.fn_py_mod = Out.get_fn(fn).rsplit('.py', 1)[0]
        s = do(PyTmplCtx.build_module)
        do(Out.pymod, fn, s, fl=10)
        do_test = FLG.py_build_test
        if do_test:
            s = do(PyTmplCtx.test_build_module)
            do(Out.pymod, fn, s, fl=10, prefix_with='test_')

    # return S.flow


main = lambda: run_app(run, flags=Flags)

# def rm_dubs():
#     ops with same sources -> unify. No. chaos.
#     have = set()
#     rm = []
#     for op in [o for o in list(flow) if o['type'] == 'ax-op']:
#         n, ws = op['name'], op['wires'][0]
#         if n in have:
#             continue
#         have.add(n)
#         all = [op for op in flow if op['name'] == n and op['wires'][0] == ws]
#         if len(all) > 1:
#             app.info('removing action ops with same dests', json=all)
#             rm.append(all)
#     for ops in rm:
#         n = ops[0]['name']
#         if n == 'I.Disc':
#             breakpoint()  # FIXME BREAKPOINT
#         for op in ops:
#             for sop in flow:
#                 for ws in sop['wires']:[['set.Wait_Returns']]},
#                     if op['id'] in ws:
#                         ws.remove(op['id'])
#                         ws.append(n)
#             flow.remove(op)
#         flow.append(op)
#         op['id'] = n


# -------------------- Arch: The old flow, where all action nodes had been unique
# followed by conds when multiple states
# def n_state(s):
#     return S.obj + '.state.%s' % s


# def n_act(s):
#     return S.obj + '.do.%s' % s


# ids = set()


# def uid(n):
#     i = '0'
#     while n in ids:
#         i = str(int(i) + 1)
#         if n.split('.')[-1].isdigit():
#             n = n.rsplit('.', 1)[0]
#         n += '.' + i
#     ids.add(n)
#     if 'Reject.4' in n:
#         breakpoint()  # FIXME BREAKPOINT
#     return n


# def ops_event_start(ev, ev_id):
#     r = []
#     for k in FLG.event_sources:
#         r.append(ev_src_ops(ev, ev, typ=k))
#         if not r[-1]:
#             app.die('Source event typ not supported', typ=k)
#     return r


# def ops_event_end(last_op, have=set()):
#     if last_op['id'] in have:
#         return []
#     have.add(last_op['id'])
#     ts = last_op['kw']['target_state']
#     r = []
#     ws = last_op['wires']
#     for k in FLG.event_sources:
#         if k == 'internal':
#             continue
#         r.append(ev_snk_ops(ts, typ=k))
#         id = r[-1]['id']
#         if not ws:
#             ws.append([])
#         if id not in ws[0]:
#             ws[0].append(id)
#     return r


# build_event_flows = lambda: [do(build_event_flow, ev, m) for ev, m in S.events.items()]


# def build_event_flow(ev, mev):
#     """
#     ev = 'Start'
#     mev: {'states': ['Closed']}
#     """
#     nfo = partial(app.info, event=ev)
#     n, ev_state_cond_id = ev, ev + '.by_state_cond'
#     start_ops = do(ops_event_start, ev, ev_state_cond_id)
#     [setitem(o, 'states', D()) for o in start_ops]
#     [sources.add(o['id']) for o in start_ops]

#     flow.extend(start_ops)

#     for state in mev['states']:
#         last_op = do(build_action_chain, state, ev, last_op=start_ops)
#         eevs = ops_event_end(last_op)
#         flow.extend(eevs)


# state_setter_name = lambda a: 'set.%s' % a

# ops_by_actname = D()
# sources = set()
# by_id = {}


# def build_action_chain(state, ev, last_op):
#     """Insert post act state conditions if we have more state inputs into an action"""

#     # if ev == 'R_Conn_CER':
#     #     breakpoint()  # FIXME BREAKPOINT
#     m = S.states[state]['events'][ev]
#     acts = list(m['actions'])
#     acts.append(m['next_state'])
#     while acts:
#         a = acts.pop(0)
#         app.debug('Action', a=a, state=state, evt=ev)
#         n = n_act(a) if acts else state_setter_name(a)
#         op = ops_by_actname.get(a)
#         if not op:
#             id = a + '.id'
#             op = {
#                 'id': id,
#                 'name': n,
#                 'type': 'ax-op',
#                 'kw': {},
#                 'wires': [],
#                 'states': D(),
#             }
#             if not acts:
#                 op['kw'] = {'target_state': a}
#             flow.append(op)
#             ops_by_actname[a] = op
#         for k in to_list(last_op):
#             k['states'][state] = op['id']
#         last_op = op
#     return last_op


# to_list = lambda a: a if isinstance(a, list) else [a]


# def cap(s):
#     return ''.join([c for c in s if c.upper() == c and not c == '_'])


# # def insert_state_splitters():
# #     by_id.update(dict([(n['id'], n) for n in flow]))
# #     nr = 0
# #     for op in list(flow):
# #         nr += 1
# #         s = op.pop('states', 0)
# #         if not s:
# #             continue
# #         tid_by_states = tbs = D()
# #         # state target id
# #         for st, tid in s.items():
# #             tbs.setdefault(tid, []).append(st)
# #         if len(tbs) == 1:
# #             op['wires'] = [[list(tbs.keys())[0]]]
# #         else:
# #             id = '%s.pc' % op['id']
# #             n = ''
# #             c = []
# #             for i, v in zip(range(len(tbs)), tbs.values()):
# #                 n += '%s:%s\n' % (i + 1, ','.join([cap(j) for j in v]))
# #                 c.append([S.obj + '.state', 'in', v])
# #             op['wires'] = [[id]]
# #             cond = {
# #                 'id': id,
# #                 'type': 'ax-cond',
# #                 'name': n,
# #                 'wires': [[k] for k in tbs.keys()],
# #                 'condition': c,
# #                 'outputs': len(c),
# #             }
# #             flow.insert(nr, cond)
# #             i += 1


# def add_root_event_source():
#     assert not flow
#     return {'type': 'ax-src', 'name': S.obj + '_events', 'wires': []}


# def build_tree():
#     st_evs = []
#     add = flow.append
#     add(
#         {
#             'id': 'root',
#             'type': 'ax-src',
#             'name': S.obj + '_events',
#             'wires': [['by_state']],
#         }
#     )
#     add({'id': 'by_state', 'type': 'ax-cond', 'name': 'by_state', 'wires': st_evs})
#     add({'id': 'end', 'type': 'ax-sink', 'name': 'ax.dump', 'wires': []})

#     for s, evs in S.states.items():
#         evs = evs['events']
#         for ev, ai in evs.items():
#             chain = []
#             id = '%s.%s' % (s, ev)

#             for a in ai['actions']:
#                 chain.append({'id': id + '.' + a, 'type': 'ax-op', 'name': a})
#             i = ai['next_state']
#             chain.append(
#                 {'id': id + '.' + i, 'type': 'ax-op', 'name': i, 'wires': [['end']]}
#             )
#             st_evs.append([chain[0]['id']])
#             for i in range(len(chain) - 1):
#                 chain[i]['wires'] = [[chain[i + 1]['id']]]
#             flow.extend(chain)


# def build_tree():
#     add(
#         {
#             'id': 'root',
#             'type': 'ax-src',
#             'name': S.obj + '_events',
#             'wires': [['by_event']],
#         }
#     )
#     ev_conds = []
#     ev_ws = []
#     add(
#         {
#             'id': 'by_event',
#             'type': 'ax-cond',
#             'name': 'by_event',
#             'wires': ev_ws,
#             'condition': ev_conds,
#         }
#     )
#     add({'id': 'end', 'type': 'ax-sink', 'name': 'ax.dump', 'wires': []})
#     for ev, states in S.events.items():
#         ev_state_ws = []
#         ev_state_cond = []
#         add(
#             {
#                 'id': ev,
#                 'type': 'ax-cond',
#                 'name': 'by_ev_state',
#                 'wires': ev_state_ws,
#                 'condition': ev_state_cond,
#             }
#         )
#         ev_conds.append(ev)
#         ev_ws.append([ev])

#         states = states['states']
#         for s in states:
#             ev_state_cond.append(s)
#             c = action_chain(ev, s)
#             ev_state_ws.append([c[0]['id']])
