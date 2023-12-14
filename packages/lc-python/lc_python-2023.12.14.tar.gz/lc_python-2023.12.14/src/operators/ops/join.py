"""
Normal Join: See class doc

IPC via: This assembles the join to work via remote, using a con obj, e.g. con.redis

The con obj must support:
    - .set (write full payload received by other process)
    - .snk (stream id of other payload)
    - .src (read id from stream)
    - .get (get full payload by that id)
All sig compatible to redis con cls.


Purpose: Keep ALL processing in the process where the primary event was received.

Features:
    - When a secondary msg arrives, its id is only THEN pushed to ipc redis and payload written,
      when the process does NOT have the primary event.
      Otherwise we simply join normally, in process, won't serialize and write anything to redis.
    - Only the process which has the primary for an id from the stream will load the payload from redis
    - Redis can be swapped with another streaming capable transport

Mechanics:
    - Primary event sources have that param in the flows.json, resulting in:
    - All Messages from primary sources have a 'primary' boolean in the header.

    1. When we build this join pipeline, then we merge also a listener for ids (simply the ids as bytes)
    2. Also we mark the end of group (group local) stream with an attr. for having seen the primary as first msg
    3. Via this we can check if a secondary msg or id byte is NOT in the process where the primary is
    4. This means, all secondaries will only have single msgs groups -> They won't call the reducer
    5. Therfore a wrapper around the reducer can load the payload from the id bytes
"""


from operators.con import con
from devapp.app import FLG, app
from operators.ops.exceptions import Err, OpArgParseError
from operators.ops.tools import Rx, rx, GS
from operators.ops.funcs import Funcs

#  raise OpArgParseError(Err.param_not_supported, mode=mode, id=id)

# secs until payload for id published on ipc is gone, when not picked by process having the primary message
ipc_expiry = 5

filter_falses = rx.filter(lambda x: bool(x))


def make_joiner(func_name):
    j = func_name.strip()
    if j and j in Funcs:
        msg_join_val = Funcs.get(j)['func']
    else:
        if '[' in j:
            j = '{%s}' % (j or 'm[_ids][msg]')

        def msg_join_val(msg, j=j):
            return j.format(m=msg)

    def joiner(msg, f=msg_join_val):
        """Wrapper to cope with id bytes for the ipc feature and errors"""
        if isinstance(msg, bytes):
            return msg.decode('utf-8')
        try:
            return f(msg)
        except Exception as ex:
            app.error('Cannot get group val', exc=ex, msg=msg)

    return joiner


class red:
    def update_payload(have, msg):
        """The default reducer - combines items of same group to one
        how to combine the messages:

        A reducer is run only if we have > 1 message.
        have is the first message, msg the second, third, ...
        """
        have['payload'].update(msg['payload'])

    def update_payload_l1(have, msg):
        h = have['payload']
        m = msg['payload']
        for k, v in m.items():
            try:
                h[k].update(v)
            except Exception:
                h[k] = v

    def add_list(have, msg):
        joined = have.setdefault('joined', [])
        joined.append(msg)


def make_reducer(func_name, ipc=None):
    r = func_name.strip()
    if r and r in Funcs:
        r = Funcs.get(r)['func']
    else:
        r = getattr(red, r, None)
        if not r:
            app.die('Reducer not defined', name=func_name)

    def reducer(have, msg, r=r, ipc=ipc):
        """Wrapper to cope with id bytes for the ipc feature and errors"""
        try:
            if ipc and isinstance(msg, bytes):
                redis, ipc_key = ipc
                id = msg.decode('utf-8')
                msg = redis.get(0, 0, key=f'{ipc_key}:{id}')
                if not msg:
                    raise Exception(f'No secondary msg in redis for {id}')

            h = r(have, msg)
            return have if h is None else h
        except Exception as ex:
            app.error('Cannot reduce', exc=ex, have=have)
            # None will not pass the final filter

    return reducer


is_compl = rx.filter(lambda x: isinstance(x, dict) and x.pop('complete', False))


class Join:
    """
    A Join node, turning n messages of the same group into one.

    Supports only data dicts right now, no buffers and such things.

    Defaults:

    * Grouping: same message id.
    * Data confict resolution:

        - Headers of first one win, but payload of second.
        - Rationale:
            - This operator is also our object cache.
            - Objects will be kept in headers - while data enrichment will take time:
                            ┌─────────> NR:DBlookup ──>┐
                        PySockSrc────────────────────>Join ─> PySockSink
    """

    def validate_supported_features(id, mode, **kw):
        # custom is manual in NR:
        if mode not in ('auto', 'manual', 'custom'):
            # TODO: Implement all these neat joining feats:
            raise OpArgParseError(Err.param_not_supported, mode=mode, id=id)

    def parse_args(name, id, timeout, count, mode='auto', **kw):
        """
        The op as normally > 1 inputs, i.e. is following a merge.
        """
        Join.validate_supported_features(**dict(locals()))
        join_val = make_joiner(kw['joiner'])

        # that always - never cache infinite times, mem will explode:
        rx_timeout = Rx.timer(float(timeout or FLG.op_join_default_timeout))
        count = int(count or 0)

        def end_of_group(s, count=count, timeout=rx_timeout):
            """when is a sequence complete, i.e. join.sends an item"""
            # 'NodeRed: After a message with the msg.complete property set':
            is_complete = s.pipe(is_compl)

            if not count:
                return Rx.merge(is_complete, timeout)
            else:
                # we got all, when we can skip count-1 and still produce:
                got_items = s.pipe(rx.skip(count - 1))
                return Rx.merge(got_items, is_complete, timeout)

        ipc_via = kw.get('ipc_via')
        if not ipc_via:
            reducer = make_reducer(kw['property'])
            combiner = rx.flat_map(
                lambda s, r=reducer: s.pipe(rx.reduce(r), filter_falses)
            )
            grouper = rx.group_by_until(join_val, None, end_of_group)

            # the greenlet switch is needed since the end_of_group, which is called for the first
            # item of groups, would not emit, when greenlet of first msg blocks for other reasons
            ops = [rx.delay(0), grouper, combiner]
        else:
            ops = configure_ipc_pipeline(ipc_via, id, join_val, kw, count, rx_timeout)
        return rx.pipe(*ops)


# ----------------------------------------------------------------------------    IPC Join
def id_strm(ipc_key, redis):
    def from_ipc_src(o, GS, name=ipc_key, redis=redis):
        return redis.src(o, name, enc='raw')

    return Rx.create(from_ipc_src).pipe(rx.subscribe_on(GS))


def configure_ipc_pipeline(ipc_via, op_id, join_val, kw, count, rx_timeout):
    redis = getattr(con, ipc_via, 0)
    ipc_key = f'ipc:{op_id}'  # name of id stream (=join operator id)
    id_stream = id_strm(ipc_key, redis)

    if not redis:
        app.die('Connection for ipc streaming not configured', name=ipc_via)
    #
    # def handle_primary(s):
    #     def frm_id_strm(ipc_key=ipc_key, con=redis):
    #         def from_ipc_src(o, GS, name=ipc_key, con=con):
    #             return con.src(o, name, enc='raw')
    #
    #         return Rx.create(from_ipc_src).pipe(rx.subscribe_on(GS))
    #
    #     return Rx.merge(s, frm_id_strm())

    def end_of_group(s, count=count, timeout=rx_timeout, join_val=join_val, con=redis):
        """
        In s are all items of the same id within this process, until group ends.

        Some items are just bytes, from the id stream

        We end the group
        - at timeout
        - when we have no primary - then we store in redis and publish id
          That information we can attach to s itself
        - when count is reached
        - when complete is reached
        """

        # 'NodeRed: After a message with the msg.complete property set':

        def not_for_us(msg, s=s):
            """Returns True when its NOT for us, so group ends"""
            # this happens most often - be fast:

            # app.debug(
            #     'Checking if for us',
            #     id=s.key,
            #     k=[i for i in msg.keys()],
            #     tsmsg=ctime(msg['ts'] / 1000),
            #     ts=ctime(msg['payload']['ts']),
            #     sender=msg['payload']['sender'],
            # )

            if isinstance(msg, bytes):
                if not getattr(s, 'have_primary', None):
                    # the most common case in a system with many workers - they ALL get those Ids
                    # which could not be joined with a primary
                    # app.debug('not for us')
                    return True
                return

            if msg.get('primary'):
                app.debug('Is primary', id=s.key)
                s.have_primary = True
                return

            # we got a secondary.
            if hasattr(s, 'have_primary'):
                app.debug('Is secondary AND we have primary', id=s.key)

                # test id write / reads in single processes:
                # id = join_val(msg)
                # con.set(
                #     data=msg['payload'],
                #     msg=None,
                #     key=ipc_key + ':' + id,
                #     ex=ipc_expiry,
                # )
                # con.snk(id, msg=None, name=ipc_key, enc='plain')

                # perfect, we'll combine(reduce) with the primary
                return

            # we did not see the primary -> not for us:
            id = s.key
            app.debug('Secondary msg - not for us', id=id)
            # write payload to redis
            con.set(
                data=msg['payload'],
                msg=None,
                key=ipc_key + ':' + id,
                ex=ipc_expiry,
            )
            con.snk(id, msg=None, name=ipc_key, enc='plain')
            return True

        is_not_for_us = s.pipe(rx.map(not_for_us), rx.filter(lambda x: x is True))
        is_complete = s.pipe(is_compl)

        if not count:
            return Rx.merge(is_not_for_us, is_complete, timeout)
        else:
            # we got all, when we can skip count-1 and still produce:
            got_all_items = s.pipe(rx.skip(count - 1))
            return Rx.merge(is_not_for_us, got_all_items, is_complete, timeout)

    grouper = rx.group_by_until(join_val, None, end_of_group)
    reducer = make_reducer(kw['property'], ipc=(redis, ipc_key))
    combiner = rx.flat_map(lambda s, r=reducer: s.pipe(rx.reduce(r)))
    ops = [
        rx.delay(0),
        rx.merge(id_stream),
        grouper,
        combiner,
        # only let (combined) primaries through:
        rx.filter(lambda x: isinstance(x, dict) and x.get('primary')),
    ]
    return ops


# TODO:
# {'_is_py': True,
#  '_orig_wires': [['6d02057a.aee57c']],
#  'accumulate': True,
#  'build': 'object',
#  'count': '',
#  'id': '1e9d61a4.775c2e',
#  'joiner': '\\n',
#  'joinerType': 'str',
#  'ipc_via': 'redis',
#  'key': 'topic1',
#  'mode': 'auto',
#  'name': '',
#  'property': 'payload',
#  'propertyType': 'msg',
#  'reduceExp': '',
#  'reduceFixup': '',
#  'reduceInit': '',
#  'reduceInitType': '',
#  'reduceRight': False,
#  'src': ['srv', '253c721f.f5770e'],
#  'timeout': '',
#  'type': 'ax-join',
#  'wires': [['6d02057a.aee57c']],
#  'ws': ['6d02057a.aee57c'],
#  'x': 550,
#  'y': 360,
#  'z': 'tests'}
# (Pdb)
