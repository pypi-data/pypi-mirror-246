from operators.ops.tools import GS, Rx, as_msg, p, rx, send_secondary


class Src:
    """Creating data"""

    def parse_args(op, func):
        # f = find_func(op)
        f = func

        def produce(observer, scheduler, f, op):
            # import threading, time
            # tn = threading.currentThread().name
            # print('starting', tn)

            # function yields items:
            try:
                if f.get('wants_observer'):
                    f['func'](observer)
                else:
                    # yields:
                    for msg in f['func']():
                        # print('producing', tn, msg)
                        observer.on_next(msg)
                observer.on_completed()
            except Exception as ex:
                ex.msg = 'data production (ax-src)'
                ex.op = op
                observer.on_error(ex)

        def to_msg(msg, f=f, op=op, primary=op.get('primary')):
            """add headers"""
            try:
                msg = as_msg(msg, f, op)
                if primary:
                    # primary event source allows to ax-join later from other sources
                    msg['primary'] = True
            except Exception as ex:
                ex.msg = msg
                ex.op = op
                raise
            send_secondary(op, msg)
            return msg

        post_rx = [rx.map(to_msg), rx.subscribe_on(GS)]

        # if not f['name'] == build.nr_in_remote_src:
        # sends already full message format:
        # post_rx.insert(0, rx.map(to_msg))

        if f['is_rx_op']:
            return f['func'](), post_rx
        else:
            # pls see comment at builder function
            return Rx.create(p(produce, f=f, op=op)), post_rx


# class Src:
#     """Creating data"""

#     def parse_args(subj, op, src, next_ops=None, has_pipe_tail=False):

#         f = find_func(op)

#         def produce(observer, scheduler, f, op):

#             # import threading, time
#             # tn = threading.currentThread().name
#             # print('starting', tn)

#             # function yields items:
#             try:
#                 if f.get('wants_observer'):
#                     f['func'](observer)
#                 else:
#                     # yields:
#                     for msg in f['func']():
#                         # print('producing', tn, msg)
#                         observer.on_next(msg)
#                 observer.on_completed()
#             except Exception as ex:
#                 ex.msg = 'data production (ax-src)'
#                 ex.op = op
#                 observer.on_error(ex)

#         def to_msg(msg, f=f, op=op):
#             """add headers"""
#             try:
#                 msg = as_msg(msg, f, op)
#             except Exception as ex:
#                 ex.msg = msg
#                 ex.op = op
#                 raise
#             return msg

#         if f['is_rx_op']:
#             return f['func']().pipe(rx.map(to_msg))
#         else:
#             # pls see comment at builder function
#             return Rx.create(p(produce, f=f, op=op)).pipe(rx.map(to_msg))
