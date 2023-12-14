#!/usr/bin/env python
"""
An fzf based tool to inspect flows.

"""

import json
import os
import time

import gevent
from devapp.app import run_app
from devapp.tools import FLG
from node_red import http_api as api
from node_red.draw.graph_easy import draw


def flags():
    class Flags:
        class server_poll_interval:
            n = 'Auto update poll interval for interactive mode ([sec]. 0: disable)'
            d = 1

        class interactive_mode:
            n = 'Interactive graph inspection'
            d = False

        class draw_flow:
            n = 'Draw ascii art from flow. All plot flags supported (-hf plot to see).'
            d = True

    return Flags


def main():
    run_app(run, flags=flags())


S = {'flow': None, 'pid': None}
wait = time.sleep
flow = lambda: S['flow']


def draw_flow(flow=None):
    flow = flow or flow_fetcher(get_flow=True)
    if not FLG.draw_flow:
        return flow
    flow = draw(flow, no_print=True)
    return flow


def flow_fetcher(get_flow=False):
    last_flw = ''
    intv = FLG.server_poll_interval
    while True:
        f = api.get_flows()['flows']
        if get_flow:
            return f
        s = json.dumps(f)
        if s != last_flw:
            last_flw = s
            S['flow'] = f
            pid = S['pid']
            if pid:
                os.kill(pid, 15)
            if intv == 0:
                return
        wait(intv)


def fzf():
    # https://github.com/dahlia/iterfzf/blob/master/iterfzf/__init__.py
    f = flow()
    tabs = [op['id'] for op in f if op['type'] in ['tab', 'subflow']]

    breakpoint()  # FIXME BREAKPOINT
    # r = sp.Popen('fzf' % , stdin=sp.PIPE)


def run():
    if not FLG.interactive_mode:
        print(draw_flow())
        return
    gevent.spawn(flow_fetcher)
    while True:
        while not flow():
            wait(0.1)
        inp = fzf()
