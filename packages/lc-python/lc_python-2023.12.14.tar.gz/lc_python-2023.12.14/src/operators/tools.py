from fnmatch import fnmatch


def oplog(op, *add):
    m = {'id': op['id'], 'n': op.get('name', 'n.a.'), 't': op['type']}
    for a in add:
        m[a] = op.get(a, 'n.a.')

    return m


# internal build caches:
# _multi_sources = {}
# _shared = {}

# oid: op or id:
class by:
    def id(oid):
        """placeholder - whenever we have a new ax_pipelines dict, we'll set it"""

    def _id(oid, frm):
        """oid is a dict with {'id'} or an op id already. We deliver the op
        frm is ax_pipelines after build. Before a temporary AP dict.
        """

        id = oid.get('id') if isinstance(oid, dict) else oid
        r = frm['ops'].get(id)
        if not r:
            raise Exception('Id %s unknown' % id)
        return r


err = lambda op_or_id: by.id(op_or_id).get('err')

# for direct flow to py import this is handy:
false, true = False, True


def msg_env(msg):
    # todo: cacheable, should be read only
    r = {}
    envs = msg.get('_env')
    if not envs:
        return r
    [r.update(e) for e in envs]
    return r


def wires(op):
    return [i for ws in op.get('wires', ()) for i in ws]


def is_py(op):
    # set in advance for subflows, at add_in_source
    h = op.get('_is_py')
    if h is not None:
        return h
    return op['type'].startswith('ax-') and not op['type'] == 'ax-hub'


lnk_func_prefix = 'rx:'


def is_func_link(op, typ):
    return (
        op['type'] == typ
        and op['name'].startswith(lnk_func_prefix)
        and op['mode'] == 'link'
    )


def func_links_to_subj_push(flow):
    """replace in-process 'rx:...' links with on_next -> subject(s)"""

    outs = [op for op in flow if is_func_link(op, 'link out')]

    def subj(op_in_link):
        return f'{op_in_link["name"]}-{op_in_link["id"]}'

    all_ins = []
    for o in outs:
        # all outs to ax.push_to:
        o['type'] = 'ax-snk'
        o['name'] = 'ax.push_to'
        links = o['links']
        ins = [op for op in flow if op['id'] in links]
        o['kw'] = {'subj': [subj(op) for op in ins]}
        links = set(links)
        for il in ins:
            # all connected ins to ax.src.on_demand subjects:
            il['type'] = 'ax-src'
            il['kw'] = {'name': subj(il)}
            all_ins.append(il)
    for il in all_ins:
        il['name'] = 'ax.src.on_demand'


def get_share_by_selector(id, op, sbv, fail=False):
    """
    The share_by feature (see test_share.py)

    This finds our selector match: name match or exact name/pos when sbv is simply True.

    2 posibilities:
    sbv be [d1, d3]
    single) wires = [[d1, d2, d3]] then the match is exact, e.g. d1 gets only data[d1]
    mult) wires = [[d1, d2], [d3]] then d1 AND d2 get data[d1]
    """

    def find_match(i, s):
        op = by.id(i)
        n = op['name']
        if fnmatch(n, '*%s*' % s):
            return i
        # if this is the next one we take the one after it:
        # TODO: fix and document that in test_share.py
        if 'rx.buffer' in n:
            if op.get('_orig_wires'):
                return find_match(op['_orig_wires'][0][0], s)

    if isinstance(sbv, str):
        sbv = [s.strip() for s in sbv.split(',')]
    ow = op['_orig_wires']
    n = by.id(id)['name'].rsplit(':', 1)[-1]
    if len(ow) < 2:
        # single situation
        if sbv == True:
            return [ow[0].index(id), n]
        ws = ow[0]
    else:
        # group where id is within:
        wiregroup = [i for i in ow if id in i]
        if not wiregroup:
            if fail:
                raise Exception('wire not found for name match', op=op, id=id)
            # is id of a virtual operator
            return get_share_by_selector(by.id(id)['ws'][0], op, sbv, fail=True)
        ws = wiregroup[0]
        if sbv == True:
            return [ow.index(ws), n]

    for s in sbv:
        for i in ws:
            m = find_match(i, s)
            if m:
                return [s]
    if sbv != True:
        op = by.id(id)
        if op['ws'] and op['type'] == 'ax-op':
            return get_share_by_selector(op['ws'][0], op, sbv, fail=True)
    return ['x']


def check_wiring(op):
    """
    Returns: [
        list: wires
        bool: deep_copy required
        bool: is_split
        list: wires w/o err in first op (wires we can push data to)
        ]
    """
    built = ws = op.get('ws')
    if built is None:
        ws = wires(op)
    if not ws:
        return ws, 0, 0, []
    if len(ws) == 1:
        return ws, 0, 0, built and [w for w in ws if not err(w)]
    dc = op.get('deep_copy')
    if dc is None:
        # The default for deep copy is to do it when we have > 1 output
        # When we have 2 wires connected to one output we don't deep copy
        # match_any: check *any* condiition, not just the first matching!
        dc = [ws] != op['wires']
    is_split = op.get('is_split')
    if is_split and not op.get('match_any'):
        dc = False  # deep_copy
    return ws, dc, is_split, built and [w for w in ws if not err(w)]
