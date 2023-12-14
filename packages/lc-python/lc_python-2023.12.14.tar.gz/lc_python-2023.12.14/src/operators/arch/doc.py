# All deprecated. New ismkdocs

"""
Asciidoc generator from pytest runs

1. Insert this into your test module:

    doc_file = True

2. Make sure your test functions call 

    test_func_doc(graph=graph) # e.g. done at build_flow, the usual test flow builder

3. at the end of the documented functions (pytest runs in order of occurrance):

    def test_last():
        from operators.doc import write_doc
        write_doc()


Then when you run pytest with export make_doc=true it will generate the files within
the docu folder.
"""

import inspect
import json
import os

# from importlib import import_module
import socket
import sys
import time
from pprint import pformat

import inflection
from devapp.tools import Pytest
from operators.ops.funcs import Funcs

srclink = lambda fn: '%s[icon:code[]^]' % fn

# fmt:off
make_doc = os.environ.get('make_doc')
host     = socket.gethostname()
who      = os.popen('whoami').read().strip()
git_rev  = os.popen('git rev-parse HEAD').read().strip()
dn       = os.path.dirname
js       = lambda s: json.dumps(s, indent=2, default=str)
h1       = lambda s: h(s, 1)
h2       = lambda s: h(s, 2)
h3       = lambda s: h(s, 3)
h        = lambda s, nr: '=' * (nr + S[0]['hir']) + ' ' + s
# fmt:on

ctx = {}  # States by module name
S = [0]  # current state for current module

docu_run_output = []


def add_docu(msg, **kw):
    """called directly by the test funcs"""
    docu_run_output.append([msg, kw])


def add_previous_test_docu_out():
    """
    Usually the func doc is built BEFORE the func is run.
    *While* running it appended to docu_run_output array, possibly.

    Here we add that to the adoc built before, i.e. this must be called at the next (or last func doc)

    """
    if not docu_run_output:
        return
    d = ['', '[cols="1a,5a",frame="none", grid="none"]', '|====']
    # .Output (a is for format: adoc)
    # [cols="1a,5a"]
    # |====
    # |streameasdd items
    # |
    # [source, python]
    # {'count': 10000, 'dt': 603}
    # |====
    py = '[source, python]'
    for msg, kw in docu_run_output:
        s = ''
        # when the output is long, we wrap it into a collapsible:
        coll, collh, collf = False, '', ''
        for k, v in kw.items():
            v = pformat(v)
            if len(v.split('\n')) > 5:
                coll = True
            s += '%s = %s\n' % (k, v)
        s = T.source(s, 'python').strip()
        if coll:
            h = ', '.join(list(kw.keys()))
            s = T.title(h, T.collapsible(s).strip()).strip()
        d.append('| %s\n|\n%s\n' % (msg, s.strip()))
    d.extend(['|====', ''])
    add('\n'.join(d))
    docu_run_output.clear()


def add(s, title=''):
    d = S[0]['doc']
    d.append('')
    if title:
        d.append('.' + title)
    d.append(s.strip())


def test_func_doc_(graph=None):
    """graph may be delivered, than at func doc, else searched in func, cls, mod"""
    if make_doc:
        if init_doc():
            if mod_doc():
                if class_doc():
                    func_doc(graph=graph)


class T:

    mod_meta = '''
- file: %(file)s
- host: %(host)s
- who: %(who)s
    '''
    js = '''
    '''
    title = (
        lambda t, s: '''
.%s
%s
    '''
        % (t, s.lstrip())
    )

    source = (
        lambda s, lang='unknown': '''
[source, %s,indent=0,options="nowrap"]
----
%s
----
    '''
        % (lang, s)
    )

    collapsible = (
        lambda s: '''
[%%collapsible]
====
%s
====
    '''
        % s
    )

    comment = (
        lambda s: '''
////
%s
////
'''
        % s
    )


def test_func_doc(graph=None):
    test_func_doc_(graph=graph)


# def read_docs_file():
#     fn = S[0]['doc_root'] + '/docs.py'
#     if not os.path.exists(fn):
#         return ''
#     with open(fn) as fd:
#         s = fd.read()
#     exec(s, globals())
#     return docs

# todo: expo

# git_rev = 'master'
def init_doc():
    add_previous_test_docu_out()
    m = Pytest.add_pytest_infos()
    # cov.switch_context(this_test())
    fn = m['file']
    s = S[0] = ctx.get(fn)
    if s == False:
        return s
    if s == None:
        S[0] = s = ctx[fn] = m
        s.update({'doc': [], 'hir': 0})
        s['have'] = set()
        s['who'] = who
        s['host'] = host
        s['date'] = time.ctime()
        s['repo_root'] = d = repo_root()
        s['doc_root'] = dr = d + '/' + os.environ.get('d_doc', 'doc')
        s['d_img'] = dr + '/assets'
        s['rel_sourcedir'] = '{d_repo}'
        # s['other_docs'] = read_docs_file()
    s.update(m)
    return True


def mod_doc():
    def load_mod(fn):
        for k, v in sys.modules.items():
            if (getattr(v, '__file__', None) or '').endswith(fn):
                return v
        # return import_module(fn.rsplit('.py', 1)[0].replace('/', '.'))

    fn = S[0]['file']
    if have(fn):
        return True
    mod = S[0]['mod'] = load_mod(fn)
    mf = getattr(mod, 'doc_file', None)
    if not mf:
        # quick rejects for all following calls to test_func_doc from for all in this fn
        ctx[S[0][fn]] = False
        return
    S[0]['doc_file'] = fn.rsplit('.', 1)[0]
    add_adoc_file_name()

    d = (mod.__doc__ or '').strip()
    if d.startswith('= '):
        h, d = (d + '\n').split('\n', 1)
        head = h.strip().split(' ', 1)[1]
    else:
        head = 'Test Log'

    f = '%(rel_sourcedir)s/%(file)s' % S[0]
    add('= ' + srclink(f) + ' ' + head)
    add_adoc_attributes()
    add(d)

    fs = Funcs['packages']
    fs = fs if isinstance(fs, list) else [fs]
    s = inspect.getsource(fs[0])  # the others are core ops, no need to docu always
    if s:
        add(T.source(s, 'python'), title='Project Function Namespace')
    add_graph(mod)
    return done(fn)


def class_doc():
    n = S[0]['class']
    if have(n):
        return True
    # this is a module test:
    if is_mod_level_test():
        return True
    done(n)
    cls = S[0]['cls'] = getattr(S[0]['mod'], n, None)
    if not cls:
        return False
    n = inflection.titleize(cls.__name__)
    add(h2(n))
    d = cls.__doc__ or ''
    d = deindent(d)
    add(d)
    add_source(cls, 'test class code', split='def test')
    add_graph(cls)
    return True


def func_doc(graph=None):
    fn = S[0]['test']
    if is_mod_level_test():
        func = getattr(S[0]['mod'], fn, None)
        h = h2
    else:
        func = getattr(S[0]['cls'], fn, None)
        h = h3
    if not func:
        return
    fnt = fn.split('_', 1)[1] if fn.startswith('test') else fn
    t = inflection.humanize(fnt)
    add(h(t))
    add(deindent(func.__doc__ or ''))
    if graph:
        func.graph = graph
    add_graph(func)
    add_source(func, 'test function code')


def add_source(obj, title, split=None):
    s = inspect.getsource(obj)
    if split:
        s = s.split(split, 1)[0]
    t, s = s.split('\n', 1)
    if s.lstrip().startswith('"""'):
        s = s.split('"""', 2)[2]
    else:
        t += '\n'

    # s = deindent(t + s)
    s = t + s

    # add(T.collapsible(T.source(s, 'python')))
    s = T.source(s, 'python')
    if len(s.split('\n')) > 50:
        s = T.title(title, T.collapsible(s))
    add(s)


# ------------------------------------------------------------------------------- tools


def have(obj):
    return obj in S[0]['have']


def done(obj):
    S[0]['have'].add(obj)
    return True


def is_mod_level_test():
    return S[0]['class'].endswith('(call)')


def add_graph(obj):
    # avoid dupilcation when cls already has it
    s = S[0]
    have = s.setdefault('graphs', set())
    g = getattr(obj, 'graph', None)
    if not g:
        return
    gl = [g] if not isinstance(g, list) else g
    for g in gl:
        gba, gsvg, t = g, None, ''
        if isinstance(g, dict):
            if 'graph' in g:
                gr = g['graph']
                gba, gsvg, t = gr.get('boxart'), gr.get('svg'), g.get('title', '')
            else:
                gba, gsvg = g.get('boxart'), g.get('svg')
        if gba in have:
            continue
        add(t)
        if not gsvg:
            add(T.source(gba))
        else:
            add(T.comment(gba))
            c = s.get('class')
            if '(call)' in c:
                c = ''
            c = ('_%s_' % c) if c else ''
            fn = (
                s['d_img']
                + '/'
                + s['file'].replace('/', '_')
                + '_'
                + c
                + s['fn']
                + '.svg'
            )
            fn = fn.replace('.py_', '__')
            # take out the date (git diffs suck else)
            ss = '<!-- Generated at '
            pre, post = gsvg.split(ss, 1)
            post = post.split(' by', 1)[1]
            gsvg = pre + ss + post
            with open(fn, 'w') as fd:
                fd.write(gsvg)
            # fn = fn.replace(s['d_img'], '{d_img}')
            fn = fn.replace(s['d_img'], './assets')
            add('image:%s[%s]' % (fn, t))
        have.add(gba)
        from node_red.nr_config_builder import last_build
        from operators.build import ax_pipelines as axp

        j = json.dumps(last_build[0], indent=4)
        add(T.title('setup', T.collapsible(T.source(j, 'javascript'))))
        j = pformat(axp).split(' at 0x')
        r = [j[0]]
        for part in j[1:]:
            r.append(' at 0x...>' + part.split('>', 1)[1])
        add(T.title('built', T.collapsible(T.source(''.join(r), 'python'))))


def dl(l, ws):
    if l[:ws] == ' ' * ws:
        return l[ws:]
    return l


def deindent(s):
    if not s.strip():
        return s
    ls = s.splitlines()
    if len(ls) == 1:
        return ls[0].strip()
    ws = len(ls[1]) - len(ls[1].lstrip())
    return ('\n'.join([dl(l, ws) for l in ls])).strip()


def write_doc():

    if not make_doc:
        return
    fnd = S[0]['doc_root'] + '/docs.adoc'
    if os.path.exists(fnd):
        with open(fnd) as fd:
            s = fd.read()
        fn = S[0]['adoc_file'].rsplit('/', 1)[-1].split('.adoc')[0]
        if not ('<<' + fn) in s:
            raise Exception('%s not in %s' % (fn, fnd))

    add_previous_test_docu_out()
    add('---')
    add(T.mod_meta % S[0])
    doc = S[0]['doc']
    for i in (0, 1):
        while not doc[i]:
            doc.pop(i)

    # doc += ['// DOCS: %s' % json.dumps(S[0]['other_docs'])]
    if 'docs.adoc' in os.listdir(S[0]['doc_root']):
        doc += ['', 'include::./docs.adoc[]', '']
    doc = '\n'.join(doc)
    try:
        df = S[0]['adoc_file']
    except Exception as ex:
        print('breakpoint set')
        breakpoint()
        keep_ctx = True
    with open(df, 'w') as fd:
        fd.write(doc)
    os.system('chmod 777 "%s"' % df)
    print('Written:', df)
    S[0] = 0


def add_adoc_attributes():
    # l = [':foo: bar']
    l = [':toc:', ':toclevels: 4']
    if 'attrs.adoc' in os.listdir(S[0]['doc_root']):
        l.insert(0, 'include::./attrs.adoc[]')
    l = '\n'.join(l)
    if l:
        add(l)


def repo_root():
    d = os.path.abspath(dn(__file__))
    while not '.git' in os.listdir(d):
        d = dn(d)
    return d


def add_adoc_file_name():
    d = S[0]['doc_file'].rsplit('/', 1)[-1]
    fn = S[0]['doc_root'] + '/' + d + '.adoc'
    S[0]['adoc_file'] = fn
