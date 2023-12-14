import pycond
from operators.ops.exceptions import Err, OpArgParseError
from operators.ops.funcs import Funcs
from operators.ops.tools import deserialize
from operators.prometheus import with_metrics

pycond.ops_use_symbolic_and_txt()


def err_handler(msg, cfg, exc, **kw):
    exc.msg = msg
    exc.op = cfg['nrop']
    raise exc


class Cond:
    """
    ax-cond node

    This is
    - either a simple filter, passing on only matching data
    - or a stream splitter into n substreams

    sub_strms: False -> we are a filter

    Else we group_by and send into substreams, dependent on conditioon

    Example:
    condition a list of single conditions: [cond1, cond2, True], where cond1,2 an
    axcondition, and True a catch all one, requires 3 substreams,
    given as list, after the ax-cond operator.
    """

    @classmethod
    def parse_args(cls, op):
        """pycond does the main work of building the op"""
        # we get the cond via json, have not tuples for keys, i.e use dot format to go deep:
        cond = deserialize(op, 'condition')
        if isinstance(cond, dict) and cond.get('expression'):
            # all in the condition param, not field by field (handy for NodeRed single json value)
            kw = cond
            cond = cond['expression']
        else:
            kw = op

        cfg = {
            'deep': '.',
            'match_any': kw.get('match_any', False),
            'into': 'cond',
        }
        cfg['add_cached'] = kw.get('add_cached', True)
        # if c:
        #     cfg['add_cached'] = 'payload' if c is True else c
        if 'params' in kw:
            cfg['params'] = deserialize(kw, 'params')
        if 'asyn' in kw:
            cfg['asyn'] = deserialize(kw, 'asyn')

        if not kw.get('match_msg'):
            cfg['prefix'] = 'payload'

        for _lp in ('lookup_provider',):
            lp = kw.get(_lp)
            if lp:
                parts = lp.split('.')
                c = Funcs['root']
                while parts:
                    part = parts.pop(0)
                    c = getattr(c, part, None)
                    if not c:
                        raise OpArgParseError(
                            Err.cond_lookup_provider_not_found, op=op['id'], lp=lp
                        )
                cfg['lookup_provider'] = c
        if isinstance(cond, dict):
            # qualifier, no splitter
            op['is_split'] = False
        cfg['err_handler'] = err_handler
        # collides:
        cfg['nrop'] = op
        try:
            qs = pycond.qualify(cond, get_type=True, **cfg)
            is_single = qs[1]
            # breakpoint()   # FIXME BREAKPOINT
            qs = (with_metrics(op['name'], qs[0], op),) + qs[1:]
            rxq = pycond.rxop(cond, qualifier=qs, **cfg)
        except Exception as ex:
            _ = Err.cond_filter_not_parseable
            raise OpArgParseError(_, id=op['id'], n=op['name'], err=ex) from ex

        return rxq, is_single
