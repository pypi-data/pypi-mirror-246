#!/usr/bin/env python
"""
Tools for converting flow files
"""

import json
import os
import stat
import sys
from functools import partial

from devapp.app import app, run_app
from devapp.tools import FLG, define_flags, read_file, write_file
from operators.plugins.app_operators.flow_file_tools import Actions as FFTActions
from operators.plugins.app_operators.term_flow_inspector import draw_flow
from operators.plugins.app_operators.term_flow_inspector import flags as inspector_flags
from operators.plugins.app_operators.term_flow_inspector import flow_fetcher


def main():
    class Flags:
        autoshort = ''

        class action:
            n = 'Action to run. ' + action_help()
            t = sorted(actions)
            d = 'create_nr_test'

        class test_name:
            n = 'Name of test to create (when action is create_nr_test) Format: <test module full file name>:<test_name>.'
            d = ''

        class incl_flow_chart:
            d = False

        class gen_docu_format:
            from operators import build  # noqa
            from node_red.draw.graph_easy import draw  # noqa

            n = 'Type of documentation to generate from test logs (action: gen_docu_from_build_test_logs)'
            d = 'mkdocs'

        # class open_editor:
        #     n = 'Open the editor on the test module where a test was added'
        #     d = True

    define_flags(inspector_flags())
    run_app(run, flags=Flags)


def run():
    getattr(Actions, FLG.action)()


tmpl_head = '''
import node_red.testing as T
from node_red import http_api as api
client = T.AsyncClient
P = lambda data: api.post('test_in', data=data).json()
T.Pytest.init()
'''

tmpl_func = '''

def %s():
    """
    <graph>
    """
    f = api.upload_flows(T.TestFlow.locate())['flows']
    c = client.connect()
    breakpoint()
    pass


'''


class Actions:
    def create_nr_test():
        """Creating a test from current Node Red flow. NodeRED must be running.

        All plot flages supported.

        Example: lc tt --plot_depth 4 -a create_nr_test -tn test_subflows.py:test_nested_subflow
        """
        # -------------------------------------- validate test_name
        n = FLG.test_name
        if not ':' in n:
            app.die('Testname like mytestmod.py:test_foo')
        mod, n = n.split(':')
        fnmod = os.path.abspath(mod)
        if not os.path.exists(fnmod):
            app.die('Not found', fnmod=fnmod)
        if not n.startswith('test'):
            app.die('test_name must start with "test"')
        # -------------------------------------- add test to test mod
        s = read_file(fnmod)
        if 'def %s()' % n in s:
            app.die('test already present', mod=fnmod, test=n)
        parts = s.split('\ndef ', 1)
        pre, post = parts if len(parts) > 1 else (s, '')
        if post:
            post = '\ndef ' + post
        for line in tmpl_head.strip().splitlines():
            if not line in pre:
                pre += '\n' + line
        pre += '\n'

        func = tmpl_func % n
        # -------------------------------------- chart
        flow = flow_fetcher(get_flow=True)
        flow = FFTActions.clean(flow)
        flow = FFTActions.reindex(flow)
        chart = '(no flow chart created)'
        if FLG.incl_flow_chart:
            chart = draw_flow(flow).replace('\n', '\n    ')

        func = func.replace('<graph>', chart)

        d = fnmod.rsplit('/', 1)[-1][:-3]
        fnf = os.path.dirname(fnmod) + '/flows/%s/%s.json' % (d, n)
        if sys.stdin.isatty():
            print(func)
            msg = 'Add this to %s and write %s [Y|qn]? ' % (fnmod, fnf)
            if input(msg).lower() in ('n', 'q',):
                print('Unconfirmed')
                return
        s, wf = pre + post + func, partial(write_file, chmod=(stat.S_IWOTH,))
        write_file(fnmod, s)
        write_file(fnf, json.dumps(flow, indent=2), mkdir=True)
        app.info(
            'Have added test to test module and written flows json file',
            tn=n,
            mod=fnmod,
            fnf=fnf,
        )
        app.info("Tip: ':e' reloads open vim buffers")
        app.info('Run via', cmd='\npytest -xs %s -k %s\n' % (fnmod, n))
        # no: we are root in the container:
        # if sys.stdin.isatty() and FLG.open_editor:
        #     os.system('${EDITOR:-/usr/bin/vim} "%s"' % fnmod)


#     def gen_docu_from_build_test_logs():
#         """Convert test logs (--write_build_log) to docu"""
#         if FLG.gen_docu_format != 'mkdocs':
#             app.die('Not supported', fmt=FLG.gen_docu_format, supported='mkdocs')
#         from operators.testing.auto_docs import gen_mkdocs_docu

#         return gen_mkdocs_docu()


actions = [p for p in dir(Actions) if not p.startswith('_')]


def action_help():
    r = []
    for a in actions:
        f = getattr(Actions, a)
        r += ['*%s*: %s' % (a, f.__doc__.strip())]
    return '. '.join(r)


if __name__ == '__main__':
    main()
