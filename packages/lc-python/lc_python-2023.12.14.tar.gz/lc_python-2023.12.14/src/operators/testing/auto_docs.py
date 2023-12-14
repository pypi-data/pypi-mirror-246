from devapp.app import app
import os, json, sys
from devapp.tools import FLG, filter_passwords, exists, project, write_file, read_file
from devapp.tools import define_flags
from node_red.draw.graph_easy import draw
import inspect


class flags:
    autoshort = 'ad'
    short_maxlen = 5

    class pytest_autodoc:
        """
        Create docu pages of the current pytest function within the build dir, containing build flow charts

        We generate the ready made markdown pages, with links to the flow charts.
        Current format only mkdocs.

        We only write the specs (.src) for those charts yet - since this is run while pytesting.
        Producing charts is done later.
        """

        d = False

    class pytest_to_docs:
        n = 'scan build directory for pytest results and get autodocs created'
        d = False

    class ops_ref_page:
        n = '(Only) if you run pytest_to_docs as well in the same docu gen run, then example refs to ../../autodocs/ are added when present'
        d = ''


define_flags(flags)
from theming.formatting import markdown

T = markdown.Mkdocs


class Skip(Exception):
    pass


class S:
    """state - set for each test func's call to def build_pipeline"""

    n_mod = None
    n_func = None
    n_cls = None
    mod = None
    cls = None
    func = None
    fn_doc = None
    d_root = None


from devapp.tools import deindent


def get_img_dir():
    db = dirname(S.fn_doc) + '/auto_img'
    os.makedirs(db, exist_ok=True)
    return db


def get_img_fn():
    fn = '%(mode)s%(tab)s' % S.params
    return '.'.join([S.mod.__name__, S.func.__qualname__, fn])


def add_chart():
    """Called pre and post mode. Rest only pre mode"""
    d = get_img_dir()
    fn = get_img_fn()
    lnk = '\n![%s](./auto_img/%s.svg)\n' % (S.n_func, fn)
    pm, pd, hp = FLG.plot_mode, FLG.plot_destination, FLG.plot_tab_header_prefix
    FLG.plot_tab_header_prefix = '# '
    FLG.plot_mode = 'src'  # we render later
    fn = d + '/' + fn
    FLG.plot_destination = fn + '.src'
    app.info('Writing flow', fn=fn)
    S.params['draw_func']()
    FLG.plot_mode, FLG.plot_destination, FLG.plot_tab_header_prefix = pm, pd, hp
    return lnk


from inflection import humanize


def add_flow(no_details=False):
    flw = json.dumps(S.params['flow'], indent=4)
    f = T.js % flw
    d = get_img_dir()
    fn = d + '/' + get_img_fn() + '.json'
    write_file(fn, flw)
    if no_details:
        return f
    return details('Flow %(mode)s %(tab)s' % S.params, f)


details = lambda s, b: T.details % (s, b)


def incr_header_levels(s, min_levels):
    s = '\n' + s
    return s.replace('\n#', '\n' + min_levels * '#')


def add_doc(body):
    with open(S.fn_doc, 'a') as fd:
        fd.write(body)


source = lambda src: details('Source code', T.py % src)


def do_mod():
    def find_mod(fn):
        for k, v in sys.modules.items():
            if (getattr(v, '__file__', None) or '').endswith(fn):
                return v

    S.mod = mod = find_mod(S.n_mod)
    # fn = lambda n: DTB() + '/' + n
    if not getattr(mod, 'is_auto_doc_file'):
        raise Skip(S.n_mod)
    fn = S.mod.__file__
    S.d_root = S.d_root or project.root()
    f = fn.split(S.d_root, 1)[1][1:].rsplit('.py', 1)[0] + '.md'
    S.fn_doc = os.path.join(S.d_root + '/build/autodocs', f)
    app.info('Generating autodoc file', fn=S.fn_doc)
    b = mod.__doc__
    if not b.strip():
        b = '# %s' % mod.__name__
    b += source(read_file(fn))
    write_file(S.fn_doc, b, mkdir=1)


def do_cls():
    b = '\n\n## %s\n\n' % S.n_cls
    S.cls = getattr(S.mod, S.n_cls)
    b += deindent(S.cls.__doc__ or '')
    add_doc(b)


func_title = lambda fn: humanize(fn.split('_', 1)[1])


def do_func():
    l, H = (2, 'h2') if not S.n_cls else (3, 'h3')
    h = '#' * l
    title = func_title(S.n_func)
    # b = '<a href="#%s">&nbsp;.</a>' % S.n_func
    b = '\n\n' + h + ' ' + title + '\n'
    # b = '\n\n%s %s\n###### %s\n' % ('#' * l, title, S.n_func)
    p = S.cls if S.n_cls else S.mod
    S.func = getattr(p, S.n_func)
    b += incr_header_levels(deindent(S.func.__doc__ or ''), l + 1)
    b += add_chart()
    b += add_flow()
    b += source(inspect.getsource(S.func))
    add_doc(b)


def register_new_test_func(pyt):
    l = pyt.split('::')
    funcs = []
    mod = l[0]
    funcs.append(do_mod) if mod != S.n_mod else 0
    S.n_mod = mod
    cls = None
    if len(l) > 2:
        cls = l[1]
        funcs.append(do_cls) if cls != S.n_cls else 0
    S.n_cls = cls
    S.n_func = l[-1].replace('(call)', '').strip()
    funcs.append(do_func)
    return funcs


dirname = os.path.dirname


def do_pre_build(flow, draw_func, pyt):
    todo = register_new_test_func(pyt)
    try:
        [f() for f in todo]
    except Skip as ex:
        app.log('Skipped', what=str(ex))
        return


def gen_build_doc(mode, flow, draw_func, tab=''):
    """We generate the markdown docs while running pytest process
    - we generate graph specs and write flow files for out of process analysis

    """
    pyt = os.environ.get('PYTEST_CURRENT_TEST')
    if not pyt:
        app.die('This is not a pytest run - cannot generate build doc')
    if not flow:
        return app.info('empty flow', tab=tab, pytest=pyt)
    S.params = dict(locals())
    app.info('Generating build doc', mode=mode, test=pyt)
    if mode == 'pre_build':
        do_pre_build(flow, draw_func, pyt)
    else:
        g = add_chart()
        f = add_flow(no_details=True)
        b = T.closed_admon('Flow post build: tab %s' % tab, '\n'.join([g, f]))
        add_doc(b)


# dir_pytest_base = '/tmp/testlogs'


# def test_mod_path():
#     t, rest = os.environ['PYTEST_CURRENT_TEST'].split('::', 1)
#     l = t.split('/')
#     l[-1] = l[-1].replace('.py', '')
#     if l[-1] in sys.modules:
#         m = sys.modules[l[-1]].__file__.replace(project.root(), '')
#         m += '::' + rest
#         return m
#     raise Exception('check sys modules')


# def testlog_filedir():
#     if FLG.write_build_log == 'pytest':
#         d = dir_pytest_base + project.root() + test_mod_path()
#     else:
#         # not really useful this:
#         d = FLG.write_build_log.format(**filter_passwords(os.environ)).strip()
#     d = d.replace(' (call)', '')
#     if not exists(d):
#         app.warn('Creating build_log directory', dir=d)
#         os.makedirs(d)
#     return d


# def write_build_log(which, flow, draw_func, tab=None):
#     """called (while pytest is running) when env flag: --write_build_log is set"""
#     if not flow:
#         return
#     pm, pd, hp = FLG.plot_mode, FLG.plot_destination, FLG.plot_tab_header_prefix
#     FLG.plot_tab_header_prefix = '# '
#     FLG.plot_mode = 'src'
#     d = testlog_filedir()
#     if tab:
#         which += '.' + tab
#     with open(d + '/flow.%s.json' % which, 'w') as fd:
#         fd.write(json.dumps(flow, indent=4))
#     FLG.plot_destination = fn = d + '/graph_easy.' + which
#     app.info('Writing flow pre', fn=fn)
#     draw_func()
#     FLG.plot_mode, FLG.plot_destination, FLG.plot_tab_header_prefix = pm, pd, hp
#     app.info('Have written build log ', dir=d, which=which)


# def gen_mkdocs_docu():
#     dt = FLG.write_build_log.split('{', 1)[0]
#     if not dt or not exists(dt):
#         app.die('Testlogs not present', dir=dt, hint='--write_build_log')

#     def walk_dir(directory, crit=None):
#         crit = (lambda *a: True) if crit is None else crit
#         files = []
#         j = os.path.join
#         for (dirpath, dirnames, filenames) in os.walk(directory):
#             files += [j(dirpath, file) for file in filenames if crit(dirpath, file)]
#         return files

#     r = {'title': '# Test Logs'}
#     j = os.path.join

#     def h(s, levels):
#         return levels * '#' + ' ' + s

#     def docu_module(dir, ctx, hir):
#         d = os.path.basename(dir)
#         n_mod, post = dir.split('::', 1)
#         if '::' in post:
#             n_cls, n_test = post.split('::', 1)
#         else:
#             n_cls, n_test = '', post
#         n_test = n_test.replace(' (call)', '').strip()
#         mt = h(n_mod, hir)

#         m = ctx.setdefault()
#         ctx['title'] = hir * '#' + ' ' + n_ntest

#         breakpoint()  # FIXME BREAKPOINT

#     def recurse(d, ctx, hir=0):
#         for f in os.listdir(d):
#             ds = j(d, f)
#             if os.path.isdir(ds):
#                 files = os.listdir(ds)
#                 if 'flow.json' in files:
#                     docu_module(ds, ctx, hir)
#                 else:
#                     ctx[f] = m = {}
#                     recurse(ds, m, hir + 1)
#             else:
#                 app.warn('file found - no action', file=ds)

#     recurse(dt, ctx=r)
#     breakpoint()  # FIXME BREAKPOINT
