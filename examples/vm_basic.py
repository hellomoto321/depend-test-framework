from utils import enter_depend_test, run_cmd
enter_depend_test()

from depend_test_framework.core import Action, ParamsRequire, Provider, Consumer, TestObject


PARAM = {}
ENV = {}


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE_N)
@Consumer.decorator('$guest_name.config', Consumer.REQUIRE)
@Provider.decorator('$guest_name.active', Provider.SET)
def start_guest(params, env):
    guest = params.guest_name
    cmd = 'virsh start ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    run_cmd(cmd)


@Action.decorator(1)
@ParamsRequire.decorator(['guest_name'])
@Consumer.decorator('$guest_name.active', Consumer.REQUIRE)
@Provider.decorator('$guest_name.active', Provider.CLEAR)
def destroy_guest(params, env):
    guest = params.guest_name
    cmd = 'virsh destroy ' + guest
    if params.mock:
        params.logger.info("Mock: " + cmd)
        return
    run_cmd(cmd)


class define_guest(TestObject):
    """ define guest"""
    _test_entry = set([Action(1),
                       ParamsRequire(['guest_name', 'guest_xml'])])
    def __init__(self):
        self._test_entry.add(Provider('$guest_name.config', Provider.SET))

    def __call__(self, params, env):
        params.logger.info("define guest %s", params.guest_name)

class undefine_guest(TestObject):
    """undefine guest"""
    _test_entry = set([Action(1),
                       ParamsRequire(['guest_name'])])
    def __init__(self):
        self._test_entry.add(Consumer('$guest_name.config', Consumer.REQUIRE))
        self._test_entry.add(Provider('$guest_name.config', Provider.CLEAR))

    def __call__(self, params, env):
        params.logger.info("undefine guest %s", params.guest_name)