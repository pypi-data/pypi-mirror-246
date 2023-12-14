import importlib
import os
import sys
from functools import partial as p
from inspect import _empty, signature, _VAR_POSITIONAL
from json import loads

import rx as Rx
from devapp.app import app, FLG
from operators.const import d_ax_func_mods, parse_env_vals, env_vals, ax_pipelines
from operators.ops.exceptions import Err, FuncNotFound, OpArgParseError
from operators.ops.subflow import op_env as sf_env_by_op
from operators.tools import oplog
from rx import operators as rx
from devapp.tools import offset_port, cast
from operators.con import connections

Funcs = {}


def load_funcs_from_str(funcs):
    pth, cls = funcs.split(':') if ':' in funcs else (funcs, None)
    if os.path.exists(pth):
        if '/' not in pth:
            pth = './' + pth
        pth, mod = pth.rsplit('/', 1)
        sys.path.insert(0, pth)
        pth = mod.replace('.py', '')
    try:
        funcs = importlib.import_module(pth)
    except Exception as ex:
        msg = 'Could not import'
        app.die(msg, tried_import=pth, hint='specifiy module:class', exc=ex)
    if cls:
        for part in cls.split('.'):
            funcs = getattr(funcs, part)
    return funcs


def build_funcs_tree(funcs, no_lazy_imports=False):
    """funcs can be
    - The top class
    - foo/bar.py:stuff.MyTopClass
    - foo.bar:stuff.MyTopClass
    """
    from operators.core import AX

    if not funcs:
        funcs = AX
    if isinstance(funcs, str):
        funcs = load_funcs_from_str(funcs)
    return funcs_from_package(funcs, no_lazy_imports=no_lazy_imports)


def func_from_rx(fn, f, op_type):
    fn = fn[3:]
    f = Funcs.get(fn)
    if f:
        return f
    else:
        if op_type == 'ax-src':
            rxop = getattr(Rx, fn, None)
        else:
            rxop = getattr(rx, fn, None)
    return add_func(rxop, is_rx=True, is_rx_lib=True) if rxop else None


def func_from_py_module(fn, op):
    """fn like py.json.dumps"""
    breakpoint()  # FIXME BREAKPOINT
    parts = fn[3:].split('.')  # remove "py."
    try:
        f = importlib.import_module(parts[0])
    except ImportError:
        raise OpArgParseError(Err.py_mod_not_importable, fn=fn, op=op['id'])
    for part in parts[1:]:
        f = getattr(f, part, None)
        if f is None:
            return None
    return add_func(f)


def funcs_from_package(cls, prefix='', clear=True, no_lazy_imports=False):
    """
    The client delivers a class Hierarchy of callable Functions.

    Here we put that into the map sent to NR at register, so that he knows what we can do.
    We simply walk the tree, recursively:

    clear: Start over, i.e. we are top level.
    """
    from operators.core import ax_core_ops  # , LazyImported

    had_funcs = len(Funcs)

    if clear:
        app.info('Scanning packages for operator functions')
        # TODO: counters reset
        Funcs.clear()
        parse_env_vals(FLG.environ_values)
        Funcs['root'] = cls
        custom_mods = [load_funcs_from_str(mn) for mn in FLG.custom_modules] or ()

        # for ax-func code ops:
        d = d_ax_func_mods()

        os.makedirs(d, exist_ok=True)
        if d not in sys.path:
            sys.path.insert(0, d)

    # remembering the sources, useful for tests, plotting:
    Funcs.setdefault('packages', []).append(cls)

    if not prefix:
        # core ops always under this namespace:
        cls.ax = ax_core_ops
        cls.con = connections.con

    members = list(dir(cls))

    if clear:
        # load custom mods first - they have precedence:
        [funcs_from_package(cm, prefix='custom', clear=False) for cm in custom_mods]
        if 'custom' in members:
            i = members.index('custom')
            if i > 0:
                members.pop(i)
                members = ['custom'] + members

    for k in members:
        # Internal helper functions have to start with _ by convention,
        # the rest is published:
        if k.startswith('_'):
            continue
        kp = ('' if not prefix else prefix + '.') + k
        custom = Funcs.get('custom.' + kp)
        if custom and not k == 'custom':
            custom['patched'] = k  # for whoever needs that
            prf = ''
            if 'patched' in signature(custom['func']).parameters:
                # when this is within the sig, we monkey patch the thing
                # so that internal calls are ALSO passed into the customization
                # plus, the param contains the ref the origin
                prf = 'DEEP '
                custom['func'] = p(custom['func'], patched=getattr(cls, k))
                setattr(cls, k, custom['func'])
            app.warn(f'{prf}patching function', patched=kp)
            Funcs[kp] = custom
            continue

        v = getattr(cls, k)
        if no_lazy_imports and k == 'rx' and isinstance(v, type(rx)):
            funcs_from_package(v, kp, clear=False)

        elif not callable(v):
            continue

        elif isinstance(v, type):
            # inner class hierarchy -> recurse:
            funcs_from_package(v, kp, clear=False)
            continue
        # elif not no_lazy_imports and isinstance(v, LazyImported):
        #     v = v()
        #     funcs_from_package(v, kp, clear=False)
        else:
            kw = {}
            if '.rx.' in kp or kp.startswith('rx.'):
                kw = dict(is_rx=True, incl_msg=False)
            Funcs[kp] = add_func(v, **kw)
    if not prefix:
        l = [k for k in sorted(Funcs) if k not in {'root', 'packages'}]
        app.debug('Have', json=l)
    l = app.info if not prefix else app.debug
    l(f'Scanned {prefix}', total=len(Funcs), functions=len(Funcs) - had_funcs)


def deserialize(op, key):
    v = op.get(key)
    if not isinstance(v, str):
        return v
    try:
        return loads(v)
    except Exception:
        raise OpArgParseError('operator not parseable', key=key, val=v, op=op['id'])


def try_lazy_import(fn):
    parts = fn.split('.')
    f = None
    while parts:
        parts.pop()
        f = Funcs.get('.'.join(parts))
        if f:
            break
    if not f:
        return
    f = f['func']()
    parts = fn.split('.')[len(parts) :]
    for p in parts:
        try:
            f = getattr(f, p)
        except Exception:
            app.error('Not found', fn=fn, missing=p)
            raise
        if not f:
            return
    app.info('Adding lazy', fn=fn)
    Funcs[fn] = f = add_func(f)
    return f


def replace_simple_mutables_with_new_instances(f, kw):
    """Biz func authors may use func caches like _c=[0] in sigs, e.g. in a rate counter function ax.rate
    It is a common error that they forget about that function being the used MULTIPLE times, one for each
    NR operator -> may work with one - will conflict with >1 we give each of them their own instance
    """
    for spec in f.get('params', ()):
        v = spec.get('default')
        if v is not None and spec.get('kind') == 1:
            for mtbl_typ in list, dict:
                if isinstance(v, mtbl_typ):
                    kw[spec['name']] = mtbl_typ(v)


def replace_callables(op, kw):
    """Some funcs allow callables as arguments - here we resolve them
    Example: con.file.watch(filename='func:project.get_my_filename')
    """
    for k, v in kw.items():
        if isinstance(v, str) and v.startswith('func:'):
            f = Funcs.get(v.split('func:', 1)[1])
            if not f:
                raise OpArgParseError(Err.func_not_defined, fn=v, **oplog(op))
            kw[k] = f['func']


def find_func(op):
    """pipeline build time, we need the function object now.

    op['name'] is the ref.

    Not all allowed is also registered, exceptions are:
    name like:
    - 'rx.<rx operator name>' e.g. rx.buffer_with_count
    - 'py:<mod>.<funcname>'   e.g.: py:usjon.loads

    If not registered we need to analyse the raw function reg. signature here - the registered ones had been alread analysed.

    Note also that the convention for custom rx operators is a registration class (namespace) called 'rx', e.g. ax:rx.debatch

    """
    fn = op['name']
    is_rx_op = False  # those won't be wrapped into rx.map

    f = Funcs.get(fn, None)

    if f is None:
        if fn.startswith('py.'):
            # e.g.: 'py:copy.deepcopy', or py:operator...
            f = func_from_py_module(fn, op)
        elif fn.startswith('rx.'):
            f = func_from_rx(fn, f, op['type'])
            is_rx_op = True
        elif fn.startswith('Rx.'):
            f = func_from_rx(fn, f, op['type'])
            is_rx_op = True

        else:
            # TODO: delete this after the con conversion is done:
            # (need to find all non working namespaces after moving con out of ax)
            if fn not in ('xxx', 'notfound', 'math.xxx'):
                # xxx is a functional test, don't stop
                # print(os.environ.get('PYTEST_CURRENT_TEST'))
                app.warn('Not found', fn=fn)
            # f = try_lazy_import(fn)
            f = None
    # ax.rx. (a custom operator in core or project, not in rx stdlib)?
    if '.rx.' in fn or f and f.get('is_rx'):
        is_rx_op = True

    if f is None:
        raise FuncNotFound(Err.func_not_found_or_importable, fn=fn, **oplog(op))

    # we might curry the 'func' -> shallow copy, to not change the original func
    # for the next operator using it:
    f = dict(f)
    f['name'] = fn
    op['metrics_count'] = op.get('metrics_count', FLG.metrics_collect)

    if not f or not isinstance(f, dict) or not f.get('func'):
        raise OpArgParseError(Err.func_not_defined, fn=fn, **oplog(op))
    try:
        kw = deserialize(op, 'kw')  # parameters for the function, from NR:
    except Exception as ex:
        msg = Err.func_parametrize_error
        raise OpArgParseError(
            msg, fn=fn, reason='cannot deserialize kw', signature=f['params'], **oplog(op)
        ) from ex
    if f.get('wants_op'):
        kw['op'] = dict(op)
        kw['op'].pop('kw')  # avoid ciruclar refs

    pp = None
    if kw:
        # maybe single param?
        if not isinstance(kw, dict):
            if len(f['params']) == 1:
                kw = {f['params'][0]['name']: kw}
            else:
                msg = Err.func_parametrize_error
                raise OpArgParseError(
                    msg, fn=fn, params=kw, signature=f['params'], **oplog(op)
                )

        # remove post processor:
        pp = kw.pop('pp', None)
        try:
            insert_env_values(kw, op)
        except Exception as ex:
            raise OpArgParseError(
                msg,
                fn=fn,
                reason='cannot insert_env vals: %s' % ex,
                signature=f['params'],
                **oplog(op),
            )

        replace_callables(op, kw)
        replace_simple_mutables_with_new_instances(f, kw)
        validate_kw_do_fit_sign(f, kw, op, is_rx_op=is_rx_op)
        f['func'] = p(f['func'], **kw)  # I love you, Raymond

    f['is_rx_op'] = is_rx_op
    if pp is not None:
        from operators.post_processors import get_post_proc_func

        pf = get_post_proc_func(pp, op)
        if not pf:
            msg = Err.func_processor_not_found
            raise OpArgParseError(msg, fn=fn, tool=pp, **oplog(op))
        f['pp'] = pf

    if not is_rx_op and op['type'] in ('ax-op', 'ax-snk'):
        func = f['func']
        if f.get('incl_msg'):
            f['func'] = lambda msg, func=func: func(msg['payload'], msg=msg)
        else:
            f['func'] = lambda msg, func=func: func(msg['payload'])
    return f


def insert_env_values(kw, op):
    """
    app client -ev ax.socket.src:port=12343
    """
    # we do NOT go over all sig params but only over the ones given in flows.json
    # so that the user can control what is parametrizable
    # Not sure though if too inconvenient but for sure better supportable (otherwise anything is possible on the CLI)
    sf_env = None
    if '/' in op['id']:
        sf_env = sf_env_by_op(op, ax_pipelines) or None
    for key in kw:
        v = None
        ev = env_vals.get(key)
        if ev:
            v = ev.get(op.get('id'), ev.get(op.get('name')))
        if sf_env and v is None:
            v = cast(sf_env.get(key))
            if v is not None:
                app.info('Updating env from subflow environ', val=v, key=key)

        if v is not None:
            ov = kw.get(key)
            if isinstance(v, dict) and isinstance(ov, dict):
                app.info('From env - updating', key=v)
                ov.update(v)
            else:
                # passwords taken care by structlogging
                app.info('From env', key=v)
                kw[key] = v
        else:
            if key == 'port':
                kw[key] = offset_port(kw[key])


def validate_kw_do_fit_sign(f, kw, op, is_rx_op):
    """
    Avoiding run time errors by checkging if the func params from node red (kw)
    actually fit the signature
    """
    # if 'set_resp' in str(dict(locals())):
    #    breakpoint()  # FIXME BREAKPOINT
    p = f['params']
    kw_have = []

    # sources do not get msgs at runtime. rx ops wrap that
    if op['type'] == 'ax-src' or is_rx_op and not f.get('takes_streams_as_params'):
        start = 0
    else:
        # operators do get a message in at runtime, as first param:
        # arbitary name - we skip checking that:
        start = 1
    have_kw = False
    for param in p[start:]:
        n = param['name']
        if n in kw:
            kw_have.append(n)
            continue
        if (
            (param.get('default', _empty) != _empty)
            or (n == 'observer' and f.get('wants_observer'))
            or n == 'msg'
        ):
            continue
        if param['kind'] == 4 and param == p[-1]:
            have_kw = True
            continue
        fn = f.get('name', 'n.a.')
        raise OpArgParseError(Err.param_value_req, op=op['id'], param=n, name=fn)

    if have_kw:
        return
    for k in kw.keys():
        if k not in kw_have:
            raise OpArgParseError(
                Err.param_not_understood, func=f['name'], op=op['id'], param=k
            )


def add_func(v, is_rx=None, is_rx_lib=False, incl_msg=False):
    """Registering a Function - with sig params"""
    # func wants full message (e.g. headers) or simply the payload?
    im = keys = sig = share_by = None
    try:
        sig = signature(v).parameters
        share_by = sig.get('share_by')
        keys = [param_def(sig[k], v) for k in sig]
        im = (bool(sig.get('msg')) and len(sig) > 1) or incl_msg
        is_rx = bool(sig.get('is_rx')) or is_rx
    except Exception as ex:
        if getattr(v, '__name__') not in ('dumps', 'loads'):
            app.warn(Err.func_no_sig, err=ex)

    m = {'func': v, 'params': keys, 'incl_msg': im, 'is_rx': is_rx}
    if sig and sig.get('observer'):
        # telling src.py to have a pushing data source:
        m['wants_observer'] = True
    elif sig and is_rx_lib:
        for p in sig:
            arg = sig[p]
            if arg.kind == _VAR_POSITIONAL:
                if 'Observable' in str(list(dict(sig).values())[0]):
                    m['takes_streams_as_params'] = True
    if share_by:
        m['share_by'] = share_by.default
    if sig and sig.get('op'):
        m['wants_op'] = True
    return m


def param_def(p, func):
    m = {'kind': int(p.kind), 'name': p.name}
    if p.default != _empty:
        m['default'] = p.default
    return m


def funcs_pretty(F):
    """when sending our funcs over to the hub at register we don't want objects"""
    m = {}
    for k, v in F.items():
        if k in ('packages', 'root', 'custom_modules'):
            continue
        m[k] = dict(v)
        m[k]['func'] = str(v['func']).split(' ')[1]
    return m
