#!/usr/bin/env python
import os, sys
from node_red import nrtesting, nrclient as red, log

import time
from devapp.app import dirs, run_app, flag, FLG, app

from random import randint


class TR069:
    def _soap_to_dict(xml):
        return {'parsed': xml}  # demo

    def _job(msg, cmd, args=None):
        msg['body'] = cmd  # no args, demo
        return red.response(msg, wait=2)

    def inform(msg):
        inform = TR069._soap_to_dict(msg['payload'])
        empty = TR069._job(msg, 'InformResponse')


class Functions:
    class create:
        def numbers():
            i = 0
            while True:
                yield i

    class math:
        def sum(data):
            # time.sleep(randint(0, 10) / 10)
            data['sum'] = data['a'] + data['b']
            app.info('sum', **data)
            return data

        def mult(data):
            # time.sleep(randint(0, 10) / 10)
            data['mult'] = data['a'] * data['b']
            app.info('mult', **data)
            return data

    tr069 = TR069


def start():
    h, p = nrtesting.detect_hub_in_process_list('ax-hub_spec.js')
    red.connect(Functions, hubs=':'.join((h, str(p))))


def kill_me():
    # avoiding endless loops on problems
    import time, sys

    time.sleep(20)
    sys.exit(1)


if __name__ == '__main__':
    import gevent

    gevent.spawn(kill_me)

    if not 'pytest' in sys.argv:
        run_app(start)
