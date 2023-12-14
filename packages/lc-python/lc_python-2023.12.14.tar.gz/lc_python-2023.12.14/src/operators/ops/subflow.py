from copy import deepcopy
from functools import partial

from devapp.app import app

# ---------------------------------------------------------------------------- building

"""
Strategy:
    A subflow is a single box ref to a set of boxes, with
    - 0/1 in wiring
    - any out wiring variation
    - overwritable config
    - possibly nested secondary subflow refs

    We do NOT create and register dedicated subflow pipelines but rather
    - clone all operators of subflows into their referencing parent, i.e. arrange the flow
    before pipeline building as if the subflow feature was not used.

    Upside: We do not have to care about inner NodeRED comm relations, that could get tricky otherwise.

    Downside clearly is that building time goes up - but up to now this seems not a problem.


"""


id_sf = lambda op: (op['type'] + 'subflow:').split('subflow:')[1]
new_id = lambda id, pth: '%s/%s' % (pth, id)
sf_instances = []
wire_sources = {}


def op_env(op, AP):
    """
    For creating the rx func partials at build.py

    ops within subflow instances are prefixed with sfi1/.../opid and sfs may have envs,
    registered at ax_pipelines:
    """
    envs = AP['envs']
    sfi = op['id'].rsplit('/', 1)[0] if '/' in op['id'] else None
    return envs.get(sfi)


def add_env(op, into, AP):
    env = op_env(op, AP)
    n = op.get('name')
    if not env or not n:
        return

    def add_nv(k):
        kf = k.split(':', 1)[1]  # what the function sig needs
        v = env[k]
        into[kf] = v
        app.debug('Value from env', name=k, id=op['id'], v=v)

    # eg ax.hello:name
    [add_nv(k) for k in [ek for ek in env if ek.startswith(n + ':')]]


def overlay_env(have, tmpl, inst):
    h = dict(have)
    for k in tmpl, inst:
        e = k.get('env', ())
        for nv in e:
            # creds have no value key:
            if not 'value' in nv:
                assert nv['type'] == 'cred'
            h[nv['name']] = nv.get('value', '')
    return h


# ---------------------------------------------- the recursion function, which unwraps:


def rewrite_ids(sfi_op, into, AP, pth, envs):
    """
    Recursively digging into nested subflow instance hirarchies
    Involves deepcopies of ops.
    """
    app.debug('Unwrapping subflow instance', id=sfi_op)
    sf_id = id_sf(sfi_op)
    z = sfi_op['z']
    sfi_op['type'] = 'subflow-instance'
    dests = sfi_op['wires']
    # the set of template ops:
    sf_ops = AP['sfs'][sf_id]
    sf_tmpl = sf_ops[sf_id]
    e = overlay_env(envs.get(pth) or {}, sf_tmpl, sfi_op)
    pth = sfi_op['id']
    if e:
        envs[pth] = e
    nid = partial(new_id, pth=pth)
    # wid = partial(new_wire_id, pth=pth, sf_ops=sf_ops)

    r = (
        {}
    )  # container for the new ops instances - 'into' dict will be updated with it
    inner_sfs = {}
    for id, op in sf_ops.items():
        # Create instance ops from template ops:
        op = deepcopy(op)
        op['z'] = z
        # e.g. ao1 -> sfi1/ao2

        op['id'] = oid = nid(op['id'])
        if id == sf_id:
            sf_instances.append({'op': sfi_op, 'tmpl': sf_tmpl, 'ops': r})
            sf_tmpl = op
            continue  # the template

        r[oid] = op
        if id_sf(op):
            inner_sfs[oid] = op
    add_wire_sources(r, prefix=pth + '/')

    app.debug('Adding instance ops', count=len(r) - 1)
    into.update(r)
    into.pop(sfi_op['id'])  # job done, we are rewired

    if inner_sfs:
        app.debug('Inner subflow instances', ids=list(inner_sfs.keys()))
        [
            rewrite_ids(op, into=into, AP=AP, pth=pth, envs=envs)
            for id, op in inner_sfs.items()
        ]


def add_wire_sources(ops, prefix=''):
    [
        wire_sources.setdefault(prefix + id, []).append(op)
        for op in (ops.values() if isinstance(ops, dict) else ops)
        for ws in op.get('wires', ())
        for id in ws
    ]


replace_wire_id = lambda id, orig, new: [id] if id != orig else new


def replace_wire(op, orig, new):
    """
    From:
            ->
        op1 -> sfi1(-> inner_op2)
                   (-> inner_op3)
    To:
        op1 -> inner_op2

    Orig: one id. new: a list of ids

    """
    # TODO: clumsy, there must be a one liner to replace matching ids with a list:
    r = []
    for ws in op['wires']:
        r.append([])
        [r[-1].extend(replace_wire_id(w, orig, new)) for w in ws]
    op['wires'] = r


def rewrite_wires(sfi, ops, AP):
    pth = sfi['op']['id']
    nid = partial(new_id, pth=pth)

    # in:
    ins = sfi['tmpl']['in']
    if ins:
        ins = ins[0]['wires']
        real_targets = [nid(iw['id']) for iw in ins]
        srcs = wire_sources[pth]
        [replace_wire(s, pth, real_targets) for s in srcs]
        add_wire_sources(srcs)

    # inner:
    for id, op in sfi['ops'].items():
        r = []
        for ws in op.get('wires', ()):
            r.append([])
            [r[-1].append(nid(w)) for w in ws]
        op['wires'] = r

    # out:
    outs = sfi['tmpl']['out']
    for out, dest in zip(outs, sfi['op']['wires']):
        for src in out['wires']:
            src_op = sfi['ops'][nid(src['id'])]
            try:
                src_op['wires'][src['port']].extend(dest)
            except IndexError as ex:
                # wire like [].
                # we cannot correct here, already duplicated
                # happens only when created programmatically
                msg = 'Wires not correct - need to be nested list. [[]] if empty, not []'
                app.error(msg, op=src_op, wires=[])


# --------------------------------------------------- entry from build.py:
def recurse_into(tab_ops, AP):
    wire_sources.clear()
    sf_instances.clear()
    envs = {}
    sfs = []
    for op in list(tab_ops.values()):
        if id_sf(op):
            sfs.append(op)

    add_wire_sources(tab_ops)
    for op in sfs:
        rewrite_ids(op, into=tab_ops, AP=AP, pth=(), envs=envs)

    for sfi in sf_instances:
        rewrite_wires(sfi, tab_ops, AP)

    AP['ops'].update(tab_ops)
    AP['envs'].update(envs)


# def new_wire_id(id, pth, sf_ops, op=None):
#     if id in sf_ops and id_sf(sf_ops[id]):
#         if not op:
#             breakpoint()  # FIXME BREAKPOINT
#             return
#         wire_sources.setdefault(id, []).append(op)

#     return new_id(id, pth)


# # -------------------------------------------------- sfi input rewiring tools:
# def extend_wires(src, r, sfi_ws):
#     r.extend(sfi_ws)
#     # register this op for the deeper level rewirings:
#     [wire_sources.setdefault(i, []).append(src) for i in sfi_ws]


# def rpl_wires_to_sfi_with_its_wires(src, ws, id, sfi_ws):
#     r = []  # the wire sources' wires, with new ids
#     [(r.append(w) if w != id else extend_wires(src, r, sfi_ws)) for w in ws]
#     return r


# def wire_sfi_sources_into_it(sfi_op):
#     breakpoint()  # FIXME BREAKPOINT
#     id, sfi_ws = sfi_op['id'], sfi_op['wires'][0]  # only 0 for sfi
#     srcs = wire_sources.get(id)
#     if not srcs:
#         app.warn('Subflow op has unused input ports', **sfi_op)
#         return
#     for src in srcs:
#         src['wires'] = [
#             rpl_wires_to_sfi_with_its_wires(src, ws, id, sfi_ws) for ws in src['wires']
#         ]


# def xrewrite_wires(sfi_op, into, AP, pth, envs):
#     """
#     Recursively digging into nested subflow instance hirarchies
#     Involves deepcopies of ops.
#     """
#     app.debug('Unwrapping subflow instance', id=sfi_op)
#     sf_id = id_sf(sfi_op)
#     z = sfi_op['z']
#     sfi_op['type'] = 'subflow-instance'
#     dests = sfi_op['wires']
#     # the set of template ops:
#     sf_ops = AP['sfs'][sf_id]
#     sf_tmpl = sf_ops[sf_id]
#     e = overlay_env(envs.get(pth) or {}, sf_tmpl, sfi_op)
#     pth = sfi_op['id']
#     if e:
#         envs[pth] = e
#     nid = partial(new_id, pth=pth)
#     wid = partial(new_wire_id, pth=pth, sf_ops=sf_ops)

#     r = {}  # container for the new ops instances - 'into' dict will be updated with it
#     inner_sfs = {}
#     for id, op in sf_ops.items():
#         # Create instance ops from template ops:
#         op = deepcopy(op)
#         op['z'] = z
#         if op['id'] == sf_id:
#             sf_tmpl = op
#             continue  # the template
#         # e.g. ao1 -> sfi1/ao2
#         op['id'] = id = nid(op['id'])
#         wsl = op.get('wires')
#         if wsl:
#             op['wires'] = [[wid(w, op=op) for w in ws] for ws in wsl]
#         r[id] = op
#         if id_sf(op):
#             inner_sfs[id] = op

#     for iw in sf_tmpl['in']:
#         sfi_op['wires'] = [[wid(w['id']) for w in iw['wires']]]
#         # we'll remove the instance, has no meaning on NR, so rewire:
#         wire_sfi_sources_into_it(sfi_op)

#     for ow in zip(sf_tmpl['out'], dests):
#         breakpoint()  # FIXME BREAKPOINT
#         for src in ow[0]['wires']:
#             op = sfi_op if src['id'] == sf_id else r[wid(src['id'])]
#             op['wires'][src['port']].extend(ow[1])

#     app.debug('Adding instance ops', count=len(r) - 1)
#     into.update(r)
#     into.pop(sfi_op['id'])  # job done, we are rewired

#     if inner_sfs:
#         breakpoint()  # FIXME BREAKPOINT
#         app.debug('Inner subflow instances', ids=list(inner_sfs.keys()))
#         [
#             reindex(op, into=into, AP=AP, pth=pth, envs=envs)
#             for id, op in inner_sfs.items()
#         ]


#     def sfi():
#         """Subflow instance operator. do nothing"""

#         def _sfi(source):
#             def subscribe(observer, scheduler=None):

#                 return source.subscribe(
#                     observer.on_next,
#                     observer.on_error,
#                     observer.on_completed,
#                     scheduler,
#                 )

#             return rx.create(subscribe)

#         return _sfi


# def find_all_subflows(flow):
#     new = lambda op: {
#         '_': op.get('name', op['id']),
#         'tmpl': op,
#         'flw': {},
#         'instances': [],
#         'inner_subflows': set(),
#     }

#     S = {op['id']: new(op) for op in flow if op['type'] == 'subflow'}
#     f = []
#     for op in flow:
#         f.append(op)
#         t = op['type'].split('subflow:', 1)
#         if len(t) == 2:
#             # subflow instance, z is containing tab or subflow
#             id = t[1]
#             S[id]['instances'].append(op)
#         z = S.get(op.get('z'))
#         if not z:
#             continue
#         # we remove subflow ops from the flow
#         f.pop()
#         z['flw'][op['id']] = op
#         if len(t) == 2:
#             z['inner_subflows'].add(t[1])
#     return S, f


# class subflow:
#    def virtual_out(data, msg, sf_id):
#        # FIXME: remove sf env
#        env = msg.get('_env')
#        if env and env[-1]['@'] == sf_id:
#            env.pop()
#        return

#    def virtual_in():
#        pass


# class Instance:
#    def __init__(self, op):
#        self.op = op


# nr = [0]


# class InSrc:
#    rx_list = ()
#    is_virt_in_src = False

#    def __init__(self, op, func=None, pth=''):
#        self.op = op
#        self.is_virt_in_src = op.get('name') == 'ax.subflow:virtual_in'
#        self.func = func
#        self.pth = pth
#        nr[0] += 1
#        self.is_nr = nr[0]

#    def pipe(self, *rx_list):
#        self.rx_list = rx_list
#        return self

#    def __str__(self):
#        n = 'SFIntSrc' if not self.is_virt_in_src else 'VirtIn'
#        r = 'real' if self.func else 'loose'
#        return '%s %s(%s):%s[%s rx ops] %s' % (
#            self.is_nr,
#            n,
#            r,
#            self.op['id'],
#            len(self.rx_list),
#            self.pth,
#        )

#    def clone(self, pth):
#        s = InSrc(self.op, self.func, '/'.join([pth, self.pth]))
#        s.rx_list = list(self.rx_list)
#        return s

#    __repr__ = __str__


# def add_in_source(spec, specs):
#    """
#    When this is a subflow than also the first op is a source if python:
#    First op can be again a subflow!
#    """
#    #
#    in_ = spec['tmpl']['in']
#    if not in_:
#        # subflow startswith a source - no problem, won't have in wires:
#        return
#    all = spec['flw']
#    if not in_[0]['wires']:
#        op = op1 = spec['tmpl']
#        # all[op['id']] = op
#        # op['wires'] = []
#        op['z'] = id
#    else:

#        op = op1 = all[in_[0]['wires'][0]['id']]
#        spec['op_in'] = op
#        # # special case:
#        # while op1['type'].startswith('subflow:'):
#        #     spec1 = specs.get(op1['type'].split(':', 1)[1])
#        #     op1 = spec1['op_in']  # was done before this one, so has this
#        # spec['op_in'] = op
#        if not is_py(op1):
#            # the first phyical op of a (nested) subflow is not python
#            # we let the builder create a virtual pair then:
#            return

#    # fmt:off
#    n = {
#        'z':               op['z'],
#        'type':            'ax-src',
#        'id':              'virt_in:' + spec['tmpl']['id'],
#        'name':            'ax.subflow:virtual_in',
#        '_is_py':           True, # otherwise a virtual NR comm pair would be created in build
#        'virtual_subflow': InSrc,
#        'wires':           [[op['id']]],
#    }
#    # fmt:on

#    app.info('Added virtual source', to=op, src=n)
#    all[n['id']] = n
#    for op in spec['instances']:
#        op['_is_py'] = True


# def new_snk(op, spec, port):
#    sf_id = spec['tmpl']['id']
#    n = {
#        'z': op['z'],
#        'type': 'ax-snk',
#        'id': ('virt_out:%s:' % port) + sf_id,
#        'name': 'ax.subflow:virtual_out',
#        'kw': {'sf_id': sf_id},
#        'is_virtual_subflow_snk': True,  # required for op.call
#        '_is_py': True,
#        'wires': [],
#    }
#    app.info('Created virtual snk', snk=n)
#    return n


# def add_out_snks(spec):
#    outs = spec['tmpl']['out']
#    all = spec['flw']
#    i = -1
#    for out in outs:
#        i += 1
#        n = None
#        for ws in out['wires']:
#            id = ws['id']
#            if id == spec['tmpl']['id']:
#                # wire from in to out -> op is the tmpl itself:
#                op = spec['tmpl']
#                all[id] = op
#                op['wires'] = []
#                op['z'] = id
#            else:
#                op = all[id]
#            n = n or new_snk(op, spec, i)
#            # we are relaxed here, from nr this is always [[]] when empty:
#            if op['wires'] == []:
#                op['wires'].append([])
#            op['wires'][ws['port']].append(n['id'])
#            app.debug('Wired virtual snk', frm=op, snk=n)
#            all[n['id']] = n


## ------------------------------------------------------------- build rx.pipe
## def built_rx_list_by_port(rxop, sf_out_port, axp):
##     sfid = rxop.op['type'].split('subflow:', 1)[1]
##     app.info('Unwrapping subflow instance', subflow=sfid, port=sf_out_port, **rxop.op)
##     spec = axp['subflows']['specs'][sfid]
##     T = spec['tmpl']
##     op_in = spec.get('op_in')
##     if not op_in:
##         breakpoint()  # FIXME BREAKPOINT
##     # we connect now rx_prev with the end of the list with ours in between:
##     try:
##         have = axp['subflows']['out_pipes']['virt_out:%s:%s' % (sf_out_port, sfid)]
##     except Exception as ex:
##         print('breakpoint set')
##         breakpoint()
##         keep_ctx = True
##         return

##     env = {}
##     for M in (T, rxop.op):
##         env.update({m['name']: m['value'] for m in M.get('env', ())})
##     if not env:
##         return have['rx_list']
##     env['@'] = sfid
##     l = list(have['rx_list'])
##     # FIXME: what about subflow containing (virt) sources?
##     l.insert(0, subflow_add_env(env, sfid))
##     return l


# def subflow_add_env(env, sfid):
#    def rxm(msg, env=env):
#        envs = msg.get('_env')
#        if not envs:
#            msg['_env'] = envs = []
#        msg['_env'].append(env)
#        return msg

#    return rx.map(rxm)


## breakpoint()  # FIXME BREAKPOINT
##     # in a subflow a non-snk op maybe wired to an out -> no error:
##     if sf_spec:
##         i = -1
##         j = -1
##         for o in sf_spec['tmpl']['out']:
##             i += 1
##             for w in o['wires']:
##                 j += 1
##                 if w['id'] == op['id']:
##                     # remember:
##                     op['sf_out'] = [i, j]
##                     return


## def with_inst_id(inst_id, id):
##     """Subflow instances are getting the instance id up front"""
##     return inst_id + ':' + id


## def fix_out_wires(s, S):
##     """
##     An outer subflow has an out wire to an (inner) subflow instance.
##     After the inner is exploded, that outwire must not any longer point to the subflow instance,
##     but to *its* nth out port wired back to a physical op, which was cloned into the outer subflow.

##     Example:

##           'name': 'Subflow 1',
##           'out': [{'wires': [{'id': '3cdb82f9.1014fe', 'port': 0}],
##                    'x': 480,
##                    'y': 40},
##                   {'wires': [{'id': '3cdb82f9.1014fe', 'port': 0},
##                              {'id': 'd79b0b01.2ef608', 'port': 1}], <- subflow instance|
##                    'x': 460,
##                    'y': 280}],
##     with:

##         {'_': 'Subflow 1',
##          'flw': {'3cdb82f9.1014fe': {'ax.hello',
##                                       (..)
##                                      'z': '9c35acae.d67d8'},
##                  'd79b0b01.2ef608': {'env': [],
##                                      'id': 'd79b0b01.2ef608',  <-----------------------
##                                      'type': 'subflow:fe2f1eee.cfe4f',
##                                      'wires': [['d79b0b01.2ef608:c0134d11.4b822']] <- clone of inner
##                                      'x': 180,
##                                      'y': 240,

##     => We find subflow fe2f1eee.cfe4f, check it's port 1 and replace its ops, with correct
##     clone ids into our wires, and get sth like:

##                   {'wires': [{'id': '3cdb82f9.1014fe', 'port': 0},
##                              {'id': 'd79b0b01.2ef608:d225937c.8355f', 'port': 0}],

##     """
##     for outs in s['tmpl']['out']:
##         replaced = []
##         for id_port in outs['wires']:
##             op = s['flw'][id_port['id']]
##             t = op['type'].split('subflow:')
##             if len(t) != 2:
##                 replaced.append(id_port)
##                 continue
##             tmpl = S[t[1]]['tmpl']
##             inner_out = tmpl['out'][id_port['port']]
##             for iws in inner_out['wires']:
##                 replaced.append(
##                     {'id': with_inst_id(op['id'], iws['id']), 'port': iws['port']}
##                 )
##         outs['wires'] = replaced


## def subflow_op_clone(op, inst_id, z):
##     d = dict(op)
##     d['id'] = with_inst_id(inst_id, d['id'])
##     # all internal wires also get the the inst id:
##     try:
##         d['wires'] = [[with_inst_id(inst_id, i) for i in ws] for ws in op['wires']]
##     except Exception as ex:
##         print('breakpoint set')
##         breakpoint()
##         keep_ctx = True
##     d['z'] = z
##     return (d['id'], d)


## def explode_subflow_instance(sf_instance, spec):
##     """op a subflow instance - might be in outer subflow"""
##     tmpl = spec['tmpl']
##     ops_flow = spec['flw']
##     inst_id = sf_instance['id']
##     inst_z = sf_instance['z']
##     app.info('Replacing with subflow', **sf_instance)
##     # remember the instance original out wires:
##     orig_wires = sf_instance['wires']
##     flow_clone = dict(
##         [subflow_op_clone(o, inst_id, z=inst_z) for o in ops_flow.values()]
##     )
##     # replacing them with the in-wiring of the template, which points into the subflow ops:
##     sf_in_op_id = tmpl['in'][0]['wires'][0]['id']
##     sf_instance['wires'] = [[with_inst_id(inst_id, sf_in_op_id)]]
##     # instance has as many wire groups as subflows has outs:
##     out = tmpl['out']
##     for i in range(len(out)):
##         out_wires = [
##             (with_inst_id(inst_id, m['id']), m['port']) for m in out[i]['wires']
##         ]
##         for id, port in out_wires:
##             wired_cloned_sf_op = flow_clone[id]
##             try:
##                 wired_cloned_sf_op['wires'][port].extend(orig_wires[i])
##             except Exception as ex:
##                 print('breakpoint set')
##                 breakpoint()
##                 keep_ctx = True
##     return flow_clone


## def explode_subflow_instances(id, spec):
##     return {op['id']: explode_subflow_instance(op, spec) for op in spec['instances']}


## def explode_subflows(flow):
##     """
##     We are unwrapping all subflows here, treat them as normal operator meshes"""
##     # TODO: Since subflows are restricted in wiring in possibilities (0/1) there would
##     # be pipelining advantages
##     S = find_all_subflows(flow)
##     have_exploded = set()  # all exploded subflow ids
##     cloned_originals = set()
##     while len(have_exploded) < len(S):
##         for id, spec in S.items():
##             if id in have_exploded:
##                 continue
##             if spec['inner_subflows'] - have_exploded:
##                 continue
##             new_ops = explode_subflow_instances(id, spec)
##             have_exploded.add(id)
##             [cloned_originals.add(id) for id in spec['flw'].keys()]
##             for op in spec['instances']:
##                 clones = new_ops[op['id']]
##                 z = op['z']
##                 if not z in S:
##                     flow.extend(clones.values())
##                 else:
##                     S[z]['flw'].update(clones)
##                     fix_out_wires(S[z], S)
##     r = []
##     return [op for op in flow if not op['id'] in cloned_originals]
