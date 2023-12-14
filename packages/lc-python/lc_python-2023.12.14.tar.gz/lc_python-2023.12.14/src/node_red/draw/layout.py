import json
from functools import partial

ls = '\\\\n'
len_ls = len(ls)


def strip_ls(r):
    while r.startswith(ls):
        r = r[len_ls:]
    while r.endswith(ls):
        r = r[:len_ls]
    return r


def p(op, k):
    return op['plot'][k]


class Ops:
    class dflt:
        """Defaults"""

        _border = 'solid'

        def get_dests(cls, op, ctx):
            return [w for w in ws for ws in op.get('wires', ())]

        def name(cls, op, ctx):
            n = op.get('name', '')
            i = p(op, 'sid')
            if not i:
                return n or p(op, 'id')
            if not n:
                return i or p(op, 'id')
            r = '%s-%s' % (n, i)
            w = ctx['max_label_width']
            if len(r) > w:
                r = r.replace('-', ls).replace(':', ls + ':')
            return r

        def typ(cls, op, ctx):
            return p(op, 'type')

        def node_layout(cls, op, ctx):
            return '{ border: %s; } ' % cls.border()

        def border(cls, op, ctx):
            if not op.get('wires'):
                return 'bold'
            return cls._border

        def box_title(cls, op, ctx):
            t = cls.typ()
            r = cls.name() + ls + t
            if op.get('err'):
                r = 'ERR: ' + r
            return strip_ls(r.strip())

        def draw(cls, op, ctx):
            r = cls.box_title()
            r = '[%s]' % r
            box = r + cls.node_layout()
            return box

        def __repr__(cls, op, ctx):
            t = cls.typ()

    class ax_hub(dflt):
        def box_title(cls, op, ctx):
            return 'AX-Hub'

    class ax_cond(dflt):
        _border = 'dashed'

        def typ(cls, op, ctx):
            t = op['condition']
            if not isinstance(t, str):
                t = json.dumps(t)
            t = t.replace('"and"', '&')
            t = t.replace('"or"', '|')
            t = t.replace('payload', 'pl')
            for k in ',', ' ', '[', ']', '"':
                t = t.replace(k, '')
            t = t[:10] + '..'
            return t

        def border(cls, op, ctx):
            # dashed when no filter?
            return cls._border

    class debug(dflt):
        pass

    class link(dflt):
        _border = 'solid'

        def box_title(cls, op, ctx):
            lks = [p(ctx['by_id'][i], 'layout').name() for i in op['links']]
            t = cls.name()
            if lks:
                lks.insert(0, '')
                t += ' link ' + cls._dir + ' ' + (ls.join(lks))
            return t

    class link_in(link):
        _dir = 'from'

    class link_out(link):
        _dir = 'to'

    class subflow:
        def box_title(cls, op, ctx):
            return cls.name()

    class io_in(dflt):
        pass

    class io_out(dflt):
        pass

    class secondary_nr_out(dflt):
        def border(cls, op, ctx):
            return 'dotted'

    class subflow_inst:
        def box_title(cls, op, ctx):
            r = cls.name() + ls + p(ctx['by_id'][p(op, 'subflow')], 'layout').name()
            return strip_ls(r)

    class tab:
        def box_title(cls, op, ctx):
            return 'Tab ' + op.get('label', '')

    class tabs:
        """virtual one, reprsenting all tabs"""

        def box_title():
            return 'All Tabs'

    class websocket(dflt):
        def name(cls, op, ctx):
            return ctx['by_id'].get(op['server'], {'path': '/n.a'})['path']

    class websocket_in(websocket):
        pass

    class websocket_out(dflt):
        pass


def short_id(op, ctx):
    """unique short id"""
    sid, chars = None, ctx['id_short']
    while not sid or sid in ctx['sids']:
        sid = _short_id(op, chars, sid, ctx['sids'])
        chars += 1
    ctx['sids'].add(sid)
    return sid


def _short_id(op, chars, oldsid, sids):
    if chars < 0:
        return ''
    id = op['id']
    if not chars or chars >= len(id):
        while id == oldsid or id in sids:
            id += '_'
        return id
    return id[:chars] + '..'


# all functions an op layout needs to provide:
meths = [
    k for k in dir(Ops.dflt) if not k.startswith('_') and callable(getattr(Ops.dflt, k))
]


def bases(cls, c={}):
    v = c.get(cls)
    if not v:
        b = cls.__bases__[:-1]
        b += (Ops.dflt, object)
        v = c[cls] = b
    return v


def layout(op, ctx):
    # creating partials for all layout functions, so op and ctx are present always:
    op['plot']['sid'] = short_id(op, ctx)
    t = op['type'].replace(' ', '_').replace('-', '_')
    if t.startswith('subflow:'):
        op['plot']['subflow'] = t.split(':', 1)[1]
        op['plot']['type'] = t = 'subflow_inst'
    cls = getattr(Ops, t, Ops.dflt)
    d = dict(cls.__dict__)
    for m in meths:
        f = getattr(cls, m, None) or getattr(Ops.dflt, m)
        d[m] = classmethod(partial(f, op=op, ctx=ctx))
    try:
        l = type(cls.__name__, bases(cls), d)
    except Exception as ex:
        print('breakpoint set')
        breakpoint()
        keep_ctx = True
    return l


# def conn_layout(frm, to, nr):
#     # http://bloodgate.com/perl/graph/manual/att_edges.html#Edges
#     typ = frm['type']
#     title, pre = '', ''
#     ws, deepc, is_split = check_wiring(frm)[:3]
#     if is_split:
#         pre += 's'
#     if pre:
#         title = pre + ' ' + title

#     if typ == 'link out':
#         c, styl, arrwstyl = '..', 'dotted', ''
#     elif typ == 'ax-cond':
#         if not is_filter(frm)[1]:
#             title = str(nr)
#         c, styl, arrwstyl = '..', 'dashed', ''
#     else:
#         c, styl, arrwstyl = '--', 'solid', 'arrowstyle: filled; '
#     sbs = frm.get('share_by')
#     if sbs:
#         l = get_share_by_selector(to['id'], frm, sbs)
#         l = ' %s' % '|'.join([str(i) for i in l])
#         title = l + title
#     if deepc:
#         symb = 'f' if nr == 0 else 'c'
#         title = symb + title
#         # styl = 'double'

#     if to.get('err'):
#         styl = 'dotted'
#         arrwstyl = 'arrowshape: x; '
#     c = '%s %s %s>' % (c, title, c) if title else '%s>' % c
#     return c + ' ' + '{ style: %s ; %s} ' % (styl, arrwstyl)


# is_src = lambda op, dests: not op['id'] in dests and not op['type'] == 'link in'
# is_lnk = lambda typ: 'link ' in typ
