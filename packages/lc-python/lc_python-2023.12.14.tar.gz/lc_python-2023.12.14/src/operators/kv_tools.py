from devapp.tools import deep_update, get_deep


def schemadict(d):
    if isinstance(d, list):
        return [schemadict(i) for i in d]
    if not isinstance(d, dict):
        return d
    r = {}
    keys = list(d.keys())[:2]
    if len(keys) == 2:
        vals = [d[k] for k in keys]
        vals = [v for v in vals if isinstance(v, dict)]
        if len(vals) == 2 and sorted(list(vals[0])) == sorted(list(vals[1])):
            r['z...'] = f'({len(d)-1} more...)'
            r[keys[0]] = schemadict(vals[0])
            return r
    return {k: schemadict(v) for k, v in d.items()}


class kv:
    def get(data, pth, sep='.', create=True):
        """create: create a deep dict at the wanted position if not present"""
        res = get_deep(pth, data, sep=sep, create=create)
        return res

    def set(data, pth=None, deep=False, pth_sep='.', **kw):
        """
        Creating new data, possibly from existing data.
        """
        if pth is None:
            return kw
        m = get_deep(key=pth, data=data, sep=pth_sep, create=True)
        n = {}  # new data
        deep_update(n, m) if deep else n.update(m)
        deep_update(n, kw) if deep else n.update(kw)
        return n

    def update(
        data, msg, pth=None, deep=False, pth_sep='.', create=True, head=False, **kw
    ):
        """
        Enriching / modifying data

        pth: A list, tuple or dotted string, pointing possibly deep into the data or a string like a.b.c
        head: pth includes full message, payload must be explicit.

        create: Creates deep pths if not yet present, else fails

        deep: If set, we "overlay" any existing data with the new one.
        Example:
        {a:{b:1}} deep updated with {a:{c:1}} at pth None will result in {a:{b:1,c:1}}

        """
        m = data
        m = get_deep(key=pth, data=msg if head else data, sep=pth_sep, create=create)
        m.update(kw) if not deep else deep_update(m, kw)
