import robotide as _
import tempfile
import wx
from robotide.preferences.settings import Settings
from robotide.namespace import Namespace
from robotide.controller import Project
from robotide.spec.librarymanager import LibraryManager
from robotide.ui.actiontriggers import MenuBar, ToolBar, ShortcutRegistry
from robotide.ui.mainframe import ActionRegisterer
from robotide.robotapi import (TestDataDirectory, TestCaseFile, ResourceFile,
                               TestCase, UserKeyword)
from robotide.controller.filecontrollers import (TestDataDirectoryController,
                                                 ResourceFileController)
from robotide.ui.notebook import NoteBook
from robotide.ui.pluginmanager import PluginManager
from robotide.ui.tree import Tree


class FakeSettings(Settings):
    def __init__(self):
        settings_path = tempfile.NamedTemporaryFile(mode='w+t').name
        Settings.__init__(self, settings_path)
        self.add_section('Plugins')

class FakeFrame(wx.Frame):
    def __init__(self, application, controller):
        wx.Frame.__init__(self, parent=None, title='RIDE Plugin Unit Test')
        self._application = application
        self._controller = controller
        self.toolbar = ToolBar(self)
        self.actions = ActionRegisterer(MenuBar(self), self.toolbar,
                                        ShortcutRegistry(self))

        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.tree = Tree(splitter, self.actions, self._application.settings)
        # populate datafile_nodes[0]
        self._populate_tree()

        self.notebook = NoteBook(splitter, self._application)
        self._plugin_manager = PluginManager(self.notebook)

    def _populate_tree(self):
        self.tree.populate(self._controller)

MIN_TC_LEN = 0
MAX_TC_LEN = 2
MIN_UK_LEN = 3
MAX_UK_LEN = 5

class FakeApplication(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)
        self.settings = FakeSettings()
        self.namespace = Namespace(FakeSettings())
        self.frame = FakeFrame(self, self.model)
        # populate datafile_nodes[1:]
        self._expand_all()

    @property
    def model(self):
        return self._create_model()

    # Fake Test Cases Tree:
    #  - /top_suite    <model.data>
    #      = Top Suite Fake UK 0
    #      = Top Suite Fake UK 1
    #      = Top Suite Fake UK 2
    #      - sub_suite_0.txt    <model.data.children[0]>
    #          - Sub Suite 0 Fake Test 0    <model.data.children[0].tests[0]>
    #          - Sub Suite 0 Fake Test 1    <model.data.children[0].tests[1]>
    #          - Sub Suite 0 Fake Test 2    <model.data.children[0].tests[2]>
    #          = Sub Suite 0 Fake UK 0      <model.data.children[0].keywords[0]>
    #          = Sub Suite 0 Fake UK 1      <model.data.children[0].keywords[1]>
    #          = Sub Suite 0 Fake UK 2      <model.data.children[0].keywords[2]>
    #      + sub_suite_1.txt   <model.data.children[1]>
    #      + sub_suite_2.txt   <model.data.children[2]>
    #  * resource.txt      <model.resources[0]>
    #
    def _create_model(self):
        suite = self._create_directory_suite('/top_suite')
        suite.children = [self._create_file_suite('sub_suite_%d.txt' % i)
                          for i in range(3)]
        res = ResourceFile()
        res.source = 'resource.txt'
        res.keyword_table.keywords.append(UserKeyword(res, 'Resource Keyword'))
        library_manager = LibraryManager(':memory:')
        library_manager.create_database()
        model = Project(
            self.namespace, library_manager=library_manager)
        model._controller = TestDataDirectoryController(suite)
        rfc = ResourceFileController(res, project=model)
        model.resources.append(rfc)
        model.insert_into_suite_structure(rfc)
        return model

    def _create_directory_suite(self, source):
        return self._create_suite(TestDataDirectory, source, is_dir=True)

    def _create_file_suite(self, source):
        suite = self._create_suite(TestCaseFile, source)
        suite.testcase_table.tests = [TestCase(
            suite, '%s Fake Test %d' % (suite.name, i)) for i in range(3)]
        return suite

    def _create_suite(self, suite_class, source, is_dir=False):
        suite = suite_class()
        suite.source = source

        if is_dir:
            suite.directory = source

        suite.keyword_table.keywords = [UserKeyword(
            suite.keyword_table, '%s Fake UK %d' % (suite.name, i)) for i in range(3)]
        return suite

    def _expand_all(self):
        for node in self.frame.tree._datafile_nodes[1:]:
            self.frame.tree._expand_and_render_children(node)
