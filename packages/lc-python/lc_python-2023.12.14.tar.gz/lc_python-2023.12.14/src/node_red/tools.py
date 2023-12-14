#!/usr/bin/env python

import ujson
# import orjson


def to_str(obj):
    try:
        return obj.decode('utf-8')
    except Exception:
        return str(obj)


# js is superdangerous - will block hanging if there are objects like 'ws' inside!!
def js(struct, ensure_ascii=False, reject_bytes=False):
    # fails when objects are in, e.g. connection sockets:
    return ujson.dumps(
        struct, ensure_ascii=ensure_ascii, reject_bytes=reject_bytes, default=str
    )


def jp(s1):
    return ujson.loads(s1)


def to_list(s, sep=','):
    return (
        s
        if isinstance(s, list)
        else list(s)
        if isinstance(s, tuple)
        else [str(i).strip() for i in s.split(sep)]
    )
