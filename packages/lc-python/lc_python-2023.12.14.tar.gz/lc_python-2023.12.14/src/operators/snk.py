import os

from devapp.app import app
from devapp.tools import repl_dollar_var_with_env_val
from node_red.tools import js
from operators.ops.tools import rx_operator

# ------------------------------------------------------------------------------ mem

# ------------------------------------------------------------------------------ socket


def file_out(filename, sep='\n', clear=False, write='payload', flush=False, is_rx=True):
    filename = repl_dollar_var_with_env_val(filename)
    filename = os.path.abspath(filename)
    dn = os.path.dirname(filename)
    sep = sep.encode('utf-8')
    if not os.path.exists(dn):
        os.makedirs(dn)
    if clear:
        os.unlink(filename) if os.path.exists(filename) else 0
    fd = [0]

    def open_file(filename=filename):
        try:
            fd[0] = open(filename, 'ab')
        except Exception as ex:
            app.error('could not open', fn=filename)

    def write_file(data, msg, filename=filename, write=write, flush=flush):
        data = msg if write == 'msg' else data
        try:
            if isinstance(data, (dict, list)):
                data = js(data)
            data = data if isinstance(data, bytes) else data.encode('utf-8')
            fd[0].write(data + sep)
            fd[0].flush() if flush else 0
        except Exception as ex:
            app.error('could not write', fn=filename, exc=ex)

    def close(filename=filename):
        try:
            fd[0].close()
        except Exception as ex:
            app.error('could not close', fn=filename)

    return rx_operator(
        on_subscription=open_file, on_next=write_file, on_completed=close
    )
