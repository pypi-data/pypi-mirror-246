# ---------------------------------------------------------- Building the python module
def t_py_mod():
    """
    Finite States Machine

    Autocreated initially from _STATEFILE_

    Note: If this is a singleton then delete the register methods

    """

    from devapp.app import app
    from operators.core import src
    from functools import partial

    class st:
        """All States"""

        _ID_BY_STATE_DICT_ASSIGNS_ = []

    class ev:
        """All Events"""

        _ID_BY_EVENT_DICT_ASSIGNS_ = []

    class act:
        """All Actions"""

        _ID_BY_ACTION_DICT_ASSIGNS_ = []

    # reverse lookup dicts (by id):
    _ = lambda d: {getattr(d, k): k for k in dir(d) if not k[0] == '_'}
    states, events, actions = _(st), _(ev), _(act)
    events[None] = 'None'  # startup

    all__OBJ_s = {}

    class _OBJ_:
        """One instance of a _OBJ_ - within each msg, added by the application"""

        # state and event currently processed:
        id = None
        state = st._START_STATE_
        event = None
        metrics = None
        actions = None

        def __init__(self, id):
            all__OBJ_s[id] = self
            self.id = id
            self.actions = []
            self.info = partial(app.info, peer=self)
            self.debug = partial(app.debug, peer=self)
            self.warn = partial(app.warn, peer=self)
            self.error = partial(app.error, peer=self)

        def __repr__(self):
            return '_OBJ_(%s) [%s[%s]]' % (
                self.id,
                states[self.state],
                events[self.event],
            )

        def on(self, evt, msg=None):
            self.event = evt if isinstance(evt, int) else getattr(ev, evt)
            self.actions.clear()
            msg = {'payload': {}} if msg is None else msg
            msg['_OBJ_'] = self
            src.on_demand('_OBJ__events').on_next(msg)

    def verify(msg, act_id, action):
        _OBJ_ = msg['_OBJ_']
        assert act_id in transitions[_OBJ_.state][_OBJ_.event]
        _OBJ_.actions.append(action)
        _OBJ_.debug(action)
        return _OBJ_

    class act:

        _ACTION_FUNCTIONS_

    class Functions:
        # inherit or reference _OBJ_ into your Functions tree
        class _OBJ_:
            """_OBJ_ Public Functions"""

            def events(is_rx=True):
                return src.on_demand('_OBJ__events')

            def set_state(data, msg, to_state):
                """Keeping the state in the message header"""
                _OBJ_ = msg['_OBJ_']
                was = _OBJ_.state
                if was == to_state:
                    return
                _OBJ_.state = to_state
                _OBJ_.debug('State changed', was=states[was], now=states[to_state])

            act = act

    # ------------------------------------------------------------------- verifications
    transitions = _TRANSITIONS_

    # ------------------------------------------------------------------- parsing infos

    # Date      : _CTIME_
    # Template  : _MOD_TEMPLATE_
    # Parser rev: _PARSER_REV_
    # CLI cmd   :
    """
    _CLI_
    """

    Statefile = '''
    _STATEFILE_CONTENT_
    '''

    Flow = lambda: _FLOW_


def t_action():
    def _ACTION_FUNC_(data, msg, v=verify):
        """
        _ACTION_TABLE_
        """
        _OBJ_ = v(msg, _ACTION_ID_, '_ACTION_')


# ------------------------------------------------------------------------- Test Module
def t_py_test_mod():
    """
    Testing the Finite States Machine
    """
    from _FN_PY_MOD_ import Functions, _OBJ_, Flow
    from operators import build
    from devapp.app import run_app, app
    from operators.ops.funcs import funcs_from_package
    from operators.testing import tools
    from functools import partial
    from time import sleep

    def pre():
        funcs_from_package(Functions)

    def build_flow(flow, have=[0]):
        if have[0]:
            return
        have[0] = True
        return tools.build_flow(flow, pre=pre, build_force_rebuild=True)

    def run(state_id, evt, assrt):
        inst = _OBJ_('test')
        inst.state = state_id
        inst.on(evt)
        sleep(0.01)
        assert inst.state == assrt

    _TEST_FUNCTIONS_


def t_test():
    def test__STATE____EVENT_():
        """
        """
        build_flow(Flow())
        run(state_id=_STATE_ID_, evt='_EVENT_', assrt=_STATE_ID_NEXT_)  # _STATE_NEXT_
