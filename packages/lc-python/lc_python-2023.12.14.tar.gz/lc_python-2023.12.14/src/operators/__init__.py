from devapp.tools import define_flags
from operators.core import AX


class flags:
    autoshort = 'op'
    short_maxlen = 5

    class op_join_default_timeout:
        n = 'Join default timeout'
        d = 1.0


define_flags(flags)


import inspect


def list_ops():
    from operators.ops.funcs import build_funcs_tree, Funcs
    from rx import operators
    from devapp.tools import deindent
    from devapp.app import app, FLG

    # we list those as well:
    AX.rx = operators
    f = build_funcs_tree(FLG.client_functions, no_lazy_imports=True)

    def explore(name, op):
        func = op.pop('func', 0)
        if not func:
            return
        op['doc'] = deindent(func.__doc__)
        try:
            op['source'] = inspect.getsource(func)
        except Exception as ex:
            # normal e.g. for rx namespace helper ops
            return
        return op

    r = {k: explore(k, v) for k, v in Funcs.items() if isinstance(v, dict)}
    r = {k: v for k, v in r.items() if v}
    return r
