from functools import partial
from devapp.tools import cast, project

# contains all the global pipeline build state (no data).
# Cleared in build.py at every rebuild, except minor changes:
ax_pipelines = {}

stop = []  # register for pipeline stop functions

# the ones defined in node red:


def d_ax_func_mods():
    return project.root() + '/tmp/lc_client_funcs'


# func sig vals from environ:
env_vals = {}


evfmthint = 'environ values must be like my.http.src:port=8080 or myopid:port=8080'
evvalhint = 'value may be in valid(!) json or simple and will be cast to fitting types'


def parse_env_vals(kvs):
    env_vals.clear()
    if not kvs or not kvs[0]:
        return

    def die(kv):
        from devapp.app import app

        app.die('Wrong environ_values fmt', got=kv, hint=evfmthint, values=evvalhint)

    def p(kv):
        if '=' not in kv:
            die(kv)

        k, v = kv.split('=', 1)
        try:
            k, pk = k.split(':')
            env_vals.setdefault(pk, {})[k] = cast(v)
        except Exception:
            die(kv)

    [p(kv) for kv in kvs]


def tab_label(z, c=[0, {}]):
    """E.g. for counters"""
    p = ax_pipelines
    if p['ts_built'] == c[0]:
        return c[1].get(z, z)
    l = [op['label'] for op in ax_pipelines['ops'].values() if op['type'] == 'tab']
    c[0] = p['ts_built']
    c[1][z] = l[0] if l else z
    return c[1][z]


# used in op.py to create a func:
tmpl_ax_func = """
from operators.ops.tools import rx_operator

def __AX_FUNC_name__():
    class ctx: pass
    subscribed = False

    __AX_FUNC_setup__

    def on_subs(ctx=ctx, subscribed=True):
        pass
        __AX_FUNC_initialize__

    def on_next(data, msg, ctx=ctx):
        payload = data
        __AX_FUNC_func__

    return rx_operator(__AX_FUNC_call_init_subs__on_next=on_next)
"""
rpl_ax_func = {
    'call_init_subs': 'on_subscription=on_subs, ',
}

brkts = {'{', '['}  # treesitter problem with literal brackets :-/
# class sources:
#     blocking_observers = []
#     ms_block = 100
#     stopped = False
