from devapp.app import app


def add_err(msg, details):
    e = str(details.get('err', ''))
    if e:
        e += ' -> '
    details['err'] = e + msg


class FuncNotFound(Exception):
    def __init__(self, msg, **details):
        # Call the base class constructor with the parameters it needs
        super(FuncNotFound, self).__init__(msg)
        add_err(msg, details)
        # this will be serialized to the server - usjon hangs on ws objects. go safe:
        self.details = dict([(k, str(v)) for k, v in details.items()])

    def __str__(self):
        app.error(self.args[0], **self.details)
        return self.args[0]


class OpArgParseError(Exception):
    def __init__(self, msg, **details):
        # Call the base class constructor with the parameters it needs
        super(OpArgParseError, self).__init__(msg)
        add_err(msg, details)
        # this will be serialized to the server
        self.details = dict([(k, str(v)) for k, v in details.items()])

    def __str__(self):
        app.error(self.args[0], **self.details)
        return self.args[0]


class TimeoutError(TimeoutError):
    def __init__(self, msg, op):
        self.msg = msg
        self.op = op
        try:
            # msg.payload changed to the exc tuple in op.py
            self.payload = msg['payload']
        except Exception:
            self.payload = 'n.a.'  # stay safe here


class Err:

    # we'll extend those with codes. for now only msg
    # fmt:off
    cond_not_deserializable               = ['Condition not deserializeable']                                [0]
    cond_require_list                     = ['Require condition list']                                       [0]
    cond_filter_not_parseable             = ['Filter condition not parseable']                               [0]
    cond_lookup_provider_not_found        = ['Lookup provider function not found']                           [0]

    func_no_sig                           = ['Could not derive func sig -> no pre run validation of params'] [0]
    func_not_found_or_importable          = ['Function not found or importable']                             [0]
    func_not_defined                      = ['Function not defined.']                                        [0]
    func_parametrize_error                = ['Func signature mapping problem.']                              [0]
    func_not_compilable                   = ['Function cannot be compiled.']                                 [0]
    func_processor_not_found              = ['Processor not found']                                          [0]
    func_type_mismatch                    = ['Function type mismatch.']                                      [0]

    op_validation_src_cannot_have_sources = ['Source cannot have sources']                                   [0]
    op_validation_snk_cannot_have_wires   = ['Sink cannot have wires']                                       [0]
    op_validation_no_sources              = ['No sources parsing error']                                     [0]
    op_subflow_error                      = ['Subflow Error']                                                [0]

    param_not_understood                  = ['Param not understood']                                         [0]
    param_not_supported                   = ['Param not supported']                                          [0]
    param_value_req                       = ['Requires param value']                                         [0]

    py_mod_not_importable                 = ['Python module not importable']                                 [0]
