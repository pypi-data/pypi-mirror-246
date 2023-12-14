from operators.ops.funcs import Funcs
from functools import partial
from operators.ops.op import ax_func_tools


class post_processors:
    def combine(msgs):
        n = dict(msgs[0])
        n['payload'] = [m for m in msgs]
        return n

    def combine_payloads(msgs):
        msgs[0]['payload'] = [m['payload'] for m in msgs]
        return msgs[0]


T = '''
def %(name)s(data):
    if 1:
%(body)s
    return msg

'''


def get_post_proc_func(pp, op):
    pf = lambda pp: Funcs.get(pp) or getattr(post_processors, pp, None)
    if not isinstance(pp, dict):
        f = pf(pp)
        if f:
            return f
    else:
        f = pf(pp.pop('func', 'x'))
        if not f:
            return None
        if isinstance(f, dict):
            f = f['func']
        f = partial(f, **pp)
        return f
    s = pp
    if pp[0] == '{':
        s = 'msg = %s' % pp
    s = ('\n' + s).replace('\n', '\n        ')

    name = ax_func_tools.clean_func_name('pp_' + op['id'])
    s = T % {'name': name, 'body': s}

    func = ax_func_tools.create_func(name, s, op)
    return func
