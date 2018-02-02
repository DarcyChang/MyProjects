from robotide import publish
from robotide.pluginapi import Plugin

class TestCaseMovingPulgin(Plugin):
    """This plugin used for moving test case order by shortcut."""
    def __init__(self, ride_app_ref):
        Plugin.__init__(self, ride_app_ref, initially_enabled=False)

    def enable(self):
        self.log('TestCase Moving Plugin enabled')
        self.register_shortcut('CtrlCmd-PAGEUP', self.testcase_move_up)
        self.register_shortcut('CtrlCmd-PAGEDOWN', self.testcase_move_down)

    def disable(self):
        self.unregister_actions()
        self.log('TestCase Moving Plugin disabled')

    def testcase_move_up(self, event):
        handler = self.tree._controller.get_handler()
        if handler.is_draggable:
            handler.OnMoveUp(event)

    def testcase_move_down(self, event):
        handler = self.tree._controller.get_handler()
        if handler.is_draggable:
            handler.OnMoveDown(event)

    # RIDE log
    def log(self, data):
        publish.RideLogMessage(data).publish()

