"""
# Error handling.

Railway Oriented Programming. Means: Any operator is followed by an exception filter, preventing further processing.

The exceptions get original msg, operator and payload attached, then pushed to subject rxerrors.

There they are formatted to dicts again, containing all infos.

- If there is a subscription in NR to rxerrors we forward into the processing pipeline
- If not we report via app.error


## Custom processing

Attach a pipeline to ax.src.on_demand(name='errors')

- Structlogging will stop then, you do yours.

### Loop Prevention:

- Messages in that pipeline will be filtered after occurring the second time
"""

import sys
import traceback
from devapp.app import app
from rx import operators as rx
from operators.const import ax_pipelines

# --------------------------------------------------------------------------------------------- Runtime

custom_err_processing_subj_name = 'errors'
exc_res_name = (
    'exception'  # so that we can filter tuples after each op, having this as first member
)


def had_no_exception(msg):
    """Added after ALL map operators (op.py)"""
    # if msg and _is_exc(msg):
    #     app.warn('Filtering msg (exc)', previous_exc=msg['payload'])
    #     return False
    # return True
    # faster:
    try:
        if msg['payload'][0] == exc_res_name:
            assert isinstance(msg['payload'], tuple)
            # yep, this really is an exception message -> Filter it:
            app.warn('Filtering msg (exc)', previous_exc=msg['payload'])
            return False
    except Exception:
        pass
    return True


def is_exc(msg):
    return not had_no_exception(msg)


def set_data_exc(msg, exc, op=None):
    # allowing other subscribers of the error pipeline to get a hold on original message:
    exc.msg = msg
    exc.payload = msg['payload']  # since original payload replaced below:
    exc.op = op

    # subscribed by default by a logger:
    ax_pipelines['rxerrors']['data']['rx'].on_next(exc)

    # convention: payload is tuple `("exception", ...)` if its an exception, filtered after ops
    msg['payload'] = (exc_res_name, exc)


# ----------------------------------------------------------- build time


def format_exc_into_rxerr(exc, _sys_quits={'BdbQuit', 'DieNow'}):
    """all errors from ax_pipelines["rxerrors"] (subscription function)"""
    tb = traceback.format_exc().splitlines()
    cls = exc.__class__.__name__
    if cls in _sys_quits:
        if cls == 'BdbQuit':
            print('Debugger quit detected - bye.')
        else:
            try:
                app.fatal(exc.args[0], **exc.args[1])
            except Exception:
                pass
            print('Fatal - must die')
        sys.exit(1)
    # inserted by , when an operator func raises, set_data_exc, in this module:
    op = getattr(exc, 'op', None) or 'no op'
    pl = getattr(exc, 'payload', None) or 'no payload'
    msg = dict(getattr(exc, 'msg', None) or {})
    msg['payload'] = pl
    rxerr = {'exc': exc, 'tb': tb, 'msg': msg, 'op': op, 'cls': cls}
    return rxerr


def report_err(rxerr):
    """Logging rxerr dicts. Default processor of exceptions.

    Can be used in custom err pipelines as well"""
    # exc kw arg will cause traceback prints in structlogging:
    app.error(rxerr['cls'], exc=rxerr['exc'], payload=rxerr)
    return rxerr


def activate_err_pipeline(AP, mode_build_or_data):
    """
    Called by build.py

    mode: build or data (i.e. lifecycle times)
    AP a dict created by build.py containing all build infos
    """
    m = mode_build_or_data
    b = AP['rxerrors'][m]
    b['rxp'] = b['rx'].pipe(rx.map(format_exc_into_rxerr))

    subs_func = report_err

    # custom processing pipeline?
    if m == 'data':
        from operators.core import src

        s = src.named_subjects.get(custom_err_processing_subj_name)
        if s:

            def subs_func(exc, s=s):
                s.on_next(exc)

    b['subscription'] = b['rxp'].subscribe(subs_func)
