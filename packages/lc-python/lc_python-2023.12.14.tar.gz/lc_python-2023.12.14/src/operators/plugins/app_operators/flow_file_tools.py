#!/usr/bin/env python
"""
Tools for converting flow files
"""

import json
import os
import sys

from devapp.app import app, run_app
from devapp.tools import FLG, jdiff, shorten, walk_dir
from operators.tools import oplog


def main():
    class Flags:
        autoshort = ''

        class action:
            n = 'Action to run. ' + action_help()
            n += '\nExample:  app fft -a reindex -if flows.json -of same\n'
            t = sorted(actions)
            d = 'pretty'

        class in_file:
            n = 'Filename for flow (- for stdin)'
            d = '-'

        class out_file:
            n = 'Filename to write cleaned up flow to (- for stdout. "same": change the original file)'
            d = '-'

        class directory:
            n = 'When given we operate on all .json files in given directory'
            d = ''

        class backup:
            n = 'When outfile is "same" create a backup file'
            d = True

        class force:
            n = 'Do not ask for confirmation'
            d = False

    run_app(run, flags=Flags)


def run():
    if FLG.directory:
        if not sys.stdin.isatty():
            app.die('recursive mode only with confirmation')
        D = os.path.abspath(FLG.directory)

        files = walk_dir(D, lambda d, fn: fn.endswith('.json'))
        if not files:
            return
        [convert_file(f) for f in files]
        return

    if FLG.in_file in ['-', 'stdin']:
        flow = '\n'.join(sys.stdin.readlines())
        nf, old = convert_flow(flow)
        write_file(nf, old=flow)

    else:
        convert_file(FLG.in_file)


def write_file(new, old):
    if not new:
        return
    fn = FLG.out_file
    if fn in ('-', 'stdout'):
        return
    fn_in = FLG.in_file

    diff = jdiff(old, new)
    if diff:
        app.info('Diff', diff=diff, rev=jdiff(new, old))
    if fn == 'same':
        if not diff and not FLG.action == 'pretty':
            app.info('Unchanged', fn=fn_in)
            return
        if fn_in in ('-', 'stdin'):
            app.die('Cannot know <same> filename to write to when in pipe mode')
            return
        fn = fn_in
        if not FLG.force:
            app.warn('Convert', file=fn_in)
            r = input('Confirm [y|N|q]: ')
            if r.lower() == 'q':
                app.die('Exit')
            if r.lower() != 'y':
                print('unconfimred')
                return

        if FLG.backup:
            # why? because .pyc is alwasy git ignored already:
            os.system('mv "%s" "%s.pyc"' % (fn_in, fn_in))

    with open(fn, 'w') as fd:
        fd.write(json.dumps(new, indent=4))
    app.warn('Have written', fn=fn)


def convert_file(fn):
    FLG.in_file = fn
    if not os.path.exists(fn):
        app.die('Not found', fn=fn)
    app.info('Reading', fn=fn)
    with open(fn) as fd:
        flow = fd.read()
    nf, old = convert_flow(flow)
    write_file(nf, old=old)


def convert_flow(flow):
    try:
        flow = json.loads(flow) if isinstance(flow, str) else flow
    except Exception as ex:
        app.warn('Cannot parse flow', ex=ex)
        return None, None
    new = getattr(Actions, FLG.action)(flow)
    if FLG.out_file in ('-', 'stdout'):
        print(json.dumps(new, indent=4))
    return new, flow


import uuid


class Actions:
    def pretty(flow):
        """Indenting the flow"""
        return flow

    def reindex_long(flow, as_json=False):
        """Generating long Ids."""
        return Actions.reindex(flow, as_json=as_json, longids=True)

    def reindex(flow, as_json=False, longids=False):
        """Generating small ids"""
        app.info('Reindexing flow')

        def ax(op):
            return op.get('name').split('.')[-1]

        # lu = { 'ax-src': lambda op: 'src-' + ax(op), 'ax-snk': lambda op: 'snk-' + ax(op), 'ax-op': lambda op: 'ax-' + ax(op), 'any': lambda op: '', }
        type_counts = {}
        smalls = set()
        have_nids = set()
        tabs = {}  # tab ids to their replaced ones

        def nr_in_name(op):
            n = op.get('name', '')
            i = ''.join([s for s in n if s.isdigit()])
            return i

        def new_id(op, longids=longids):
            # if 'tab' not in str(op): breakpoint()  # FIXME BREAKPOINT
            sep = '.' if longids else '_'
            nr = ''
            t = op['type']
            if t.startswith('subflow:'):
                t = 's_f_i'  # -> sfi will be short
                # t = op['type'].split(':', 1)[1] + 'i'
                # t = ''.join([c for c in t])
            else:
                t = t.replace('subflow', 'sub_flow')
                t = t.replace(':', '_')
                # nr = nr_in_name(op)
                # if nr:
                #     t += '_%s_%s' % (nr, sep)
            h = type_counts.get(t)
            if not h:
                ts = t.replace('-', '_').replace(' ', '_')
                ts = shorten(ts, '', maxlen=10, all_shorts=smalls)
                smalls.add(ts)
                type_counts[t] = h = [0, ts]
            h[0] = count = h[0] + 1
            z = ''
            if op.get('z'):
                z = tabs[op['z']].split(sep, 1)[0] + sep
            if nr:
                nid = z + h[1][:-1]
                if nid not in have_nids:
                    if longids and z:
                        pass
                    else:
                        return nid
            nid = '%s%s%s' % (z, h[1], count)
            if longids and op.get('name'):
                nid = nid + sep + op.get('name', op.get('label', ''))
                nid = nid.replace(' ', '')
            # if nid in have_nids: breakpoint()  # FIXME BREAKPOINT
            assert nid not in have_nids
            return nid

        # first generate long ids for all:
        fs = json.dumps(flow, indent=2)
        for op in flow:
            id = op['id']
            nid = str(uuid.uuid4()).replace('_', '')
            fs = fs.replace('"%s"' % id, '"%s"' % nid)
            fs = fs.replace('"subflow:%s"' % id, '"subflow:%s"' % nid)
        flow = json.loads(fs)

        ids = [op['id'] for op in flow]
        all = {op['id']: op for op in flow}
        have_sfi = False
        for id in ids:
            op = all[id]
            # if op.get('name') in ('rolling_aggregation', 'arrange_data'):
            #    breakpoint()  # FIXME BREAKPOINT
            # keep the doctor away:
            if op['type'].startswith('subflow:'):
                have_sfi = True
            if have_sfi and op['type'] == 'subflow':
                raise Exception('Subflows must be first')
            nid = new_id(op)
            if op.get('type') in {'tab', 'subflow'}:
                tabs[id] = nid
            if nid != id:
                app.debug('New id', newid=nid, **oplog(op))
            have_nids.add(nid)
            # we simply hammer the new ids into the string, changing any occurrance:
            # that's why we converted to uuid before this all:
            # if op['type'] == 'subflow': breakpoint()  # FIXME BREAKPOINT
            for f, t in [[id, nid], ['subflow:%s' % id, 'subflow:%s' % nid]]:
                fs = fs.replace('"%s"' % f, '"%s"' % t)

        return fs if as_json else json.loads(fs)

    def clean(flow):
        """Removing dangling nodes, i.e. nodes with input but no wires into it"""

        def e(*a, **kw):
            return app.info(*a, **kw)

        rm = set()
        all = {op['id']: op for op in flow}
        e('have ops', count=len(all))
        dests = {id: all[id] for op in flow for ws in op.get('wires', [[]]) for id in ws}
        e('have wire dests', count=len(dests))
        zs = {}
        [zs.setdefault(op.get('z'), []).append(op) for op in flow]
        e('have zs', count=len(zs))
        have_hub = False

        for op in flow:
            id = op['id']
            if op['type'] == 'ax-hub' and not have_hub:
                e('Have ax-hub')
                have_hub = True
                continue
            if op['type'] == 'tab':
                ops = zs.get(id, [])
                if not ops:
                    e('tab w/o ops', id=id)
                    rm.add(id)

            elif op['type'] == 'subflow':
                ops = zs.get(id, [])
                i = [k for k in all.values() if k['type'].startswith('subflow:%s' % id)]
                e(
                    'subflow',
                    name=op.get('name', ''),
                    id=id,
                    instances=len(i),
                    ops=len(ops),
                )
                if not i:
                    rm.add(id)
                    [rm.add(o['id']) for o in ops]
            elif op.get('z') and not op.get('wires'):
                # autonmous subflow?
                if id not in dests:
                    sf = get_sf_tmpl(op, all)
                    if sf and not sf['in']:
                        e('Autonmous subflow instance - keeping it:', id=id)
                        continue
                    e('Dangling:', id=id)
                    rm.add(id)
        e('removing ops', count=len(rm), ops=rm)
        flow = [op for op in flow if op['id'] not in rm]
        return flow


def get_sf_tmpl(sfi, all):
    return all.get((sfi['type'] + ':').split(':')[1])


actions = [p for p in dir(Actions) if not p.startswith('_')]


def action_help():
    r = []
    for a in actions:
        f = getattr(Actions, a)
        r += ['*%s*: %s' % (a, f.__doc__.strip())]
    return '. '.join(r)


if __name__ == '__main__':
    main()
