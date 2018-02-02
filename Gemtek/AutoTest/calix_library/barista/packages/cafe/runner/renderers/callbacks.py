from __future__ import print_function

__author__ = 'akhanov'


from cafe.runner.utilities import get_test_suite_name
from cafe.runner.utilities import get_test_case_id
from cafe.runner.utilities import get_test_case_assignee
import cafe.topology.topo

import sys
import os
import pprint
import re

from cafe.runner.tctools import TestSuiteState
#from cafe.runner.parameters.runner_state import runner_state
# from cafe.core.db import create_test_db
from cafe.core.db import get_test_db
from cafe.core.config import get_config
#logger = runner_state.logger
from cafe.topology.topo import get_topology
from cafe.core.utils import get_test_param

from cafe.runner.signals import SignalManager, clear_signal, get_signals, on_signal, raise_signal


class Renderer(object):
    """Class which handles callbacks based on events occuring during the execution of test suites and test cases
    """
    logger = None
    """CLogger: The logger object to log to
    """

    def __init__(self, logger):
        """Initialization of the Object
        Creates a test database to log results to

        Args:
            logger (CLogger): The logger object to log to

        """
        from cafe.runner.parameters.options import options
        self.__options = options
        self.logger = logger

    def skip_test_suite(self, func):
        """Callback for when a test suite gets skipped during execution
        Logs that the test suite was skipped

        Args:
            func (function): The test suite function in question

        """
        name = get_test_suite_name(func)
        self.logger.debug("SKIP test suite '%s'" % name)

    def skip_test_case(self, func):
        """Callback for when a test case gets skipped during execution
        Logs that the test case was skipped

        Args:
            func (function): The test case function in question

        """
        self.logger.debug("SKIP test case '%s'" % func.__name__)

    def test_suite_exception(self, func, e, tb):
        """Callback for when an exception is encountered inside a test suite
        Logs the error.

        Args:
            func (function): The test suite function in question
            e (Exception): The exception object
            tb (str): The traceback

        """
        self.logger.error("EXCEPTION test case '%s': %s\n\n%s" % (get_test_suite_name(func), e.message, tb))

    def start_test_suite(self, func):
        """Callback for when a test suite execution starts
        Logs the start event and makes an entry in the database

        Args:
            func (function): The test suite function in question

        """
        db = get_test_db()
        db.create_testsuite(get_test_suite_name(func))

        name = get_test_suite_name(func)
        alt_name = func.__name__

        # See if any test suite options need to be applied

        ''' Topology File Handling '''

        topology_backup = None
        param_backup = None

        try:
            alt_name = func.__name__
            test_suites = self.__options.get_instances()['test_suite']
            key = None

            if name in test_suites:
                key = name
            elif alt_name in test_suites:
                key = alt_name

            fname = get_config()[key].topology_file
            topology_backup = get_topology().backup()

            if fname is not None:
                get_topology().load(fname)
            else:
                topology_backup = None

            self.logger.debug("Loaded topology file '%s' for test suite '%s'" % (fname, alt_name))

            param_file_list = get_config()[key].parameter_files

            if param_file_list is not None:
                param_backup = get_test_param().copy()
                get_test_param().reset()

                for fname in param_file_list:
                    p = cafe.Param()
                    p.load(fname)

                    cafe.param_merge(get_test_param(), p)

                    self.logger.debug("Loaded parameter file '%s' for test suite '%s'" % (fname, alt_name))
            else:
                param_backup = None

        except KeyError:
            pass
        except cafe.topology.topo.TopologyError:
            self.logger.error("Unable to load topology file '%s' for test suite '%s'" % (fname, alt_name))
        except cafe.core.utils.ParamFileError:
            self.logger.error("Unable to load parameter files '%s' for test suite '%s'" % (", ".join(param_file_list),
                                                                                           alt_name))

        ''' End Topology File Handling'''

        self.logger.debug("START test suite '%s'" % name)
        SignalManager.new_exec_level()
        TestSuiteState.add_ts(name, topology_backup, param_backup)

    def end_test_suite(self, func):
        """Callback for when a test suite execution ends
        Logs the end event and closes the entry in the database

        Args:
            func (function): The test suite function in question

        """
        name = get_test_suite_name(func)
        #db = get_test_db()
        #db.update_testsuite_result(name)
        #print(db._get_testsuite_report_text(get_test_suite_name(func)))
        self.logger.debug("FINISH test suite '%s'" % name)

        ''' Topology File Handling '''

        topology_backup = TestSuiteState.dump()[name]['topology_backup']
        param_backup = TestSuiteState.dump()[name]['param_backup']

        if topology_backup is not None:
            get_topology().restore(topology_backup)
            self.logger.debug("Unloaded topology file after test suite '%s'" % (name))

        if param_backup is not None:
            get_test_param().reset()
            cafe.param_merge(get_test_param(), param_backup)
            self.logger.debug("Unloaded parameter files after test suite '%s'" % (name))

        ''' End Topology File Handling '''

        SignalManager.finish_exec_level()
        TestSuiteState.close_ts(name)

        get_test_db().close_current_testsuite()


    def start_test_case(self, func):
        """Callback for when a test case execution starts
        Logs the start event and makes an entry in the database

        Args:
            func (function): The test case function in question

        """
        gid = get_test_case_id(func)
        assignee = get_test_case_assignee(func)
        db = get_test_db()
        SignalManager.new_exec_level()
        tcid = db.create_testcase(name=func.__name__, global_id=gid, assignee=assignee)
        self.logger.debug("START test case '%s'" % func.__name__)

    def end_test_case(self, func):
        """Callback for when a test case execution ends
        Logs the end event and closes the entry in the database

        Args:
            func (function): The test suite function in question

        """
        db = get_test_db()
        #print("*** %d " % db.current_testcase_id)
        # db.update_testcase_elapsed_time(db.current_testcase_id)
        # db.update_testsuite_result_by_id(db.current_testsuite_id)
        # tcinfo = db.get_testcase(func.__name__, get_test_case_id(func), db.current_testsuite_id)
        tcinfo = db.get_current_testcase()
        self.logger.debug("FINISH test case '%s'" % func.__name__)
        SignalManager.finish_exec_level()

        db.close_current_testcase()
        return tcinfo

    def start_test_step(self, title):
        self.logger.debug("Test Step '%s' started" % title)

    def end_test_step(self, title, tc_obj):
        self.logger.debug("Test Step '%s' ended" % title)

    def process_test_case_results(self, func, tcinfo):
        """Callback for when a test case execution is complete and the result is known

        Args:
            func (function): The test suite function in question
            tcinfo: The test case info object containing the status

        """
        if tcinfo.status == "pass":
            pass
        elif tcinfo.status == "fail":
            pass
        elif tcinfo.status == "indeterminate":
            pass

    def test_case_exception(self, func, e, tb):
        """Callback for when an exception is encountered inside a test case
        Logs the error.

        Args:
            func (function): The test case function in question
            e (Exception): The exception object
            tb (str): The traceback

        """
        self.logger.error("EXCEPTION test suite '%s': %s\n\n%s" % (func.__name__, e.message, tb))
        db = get_test_db()
        ts_id = db.current_testsuite_id
        tc_id = db.current_testcase_id

        m = re.search(r'File\s+"(?P<filename>.*)",\s+line\s+(?P<line>\S+),.*\n\s+(?P<command>.*)\n', tb)
        filename = "<NOT FOUND>"
        line = 0
        command = ""

        try:
            filename = m.group('filename')
            line = m.group('line')
            command = m.group('command')
        except:
            pass

        db.create_teststep(ts_id, tc_id, "Unhandled Exception", response=tb, status="error",
                           filename=filename, line=line, cmd=command)

    def get_stdout_destination(self):
        """Callback for retrieving the stream where all writes to stdout are redirected to

        Returns:
            The stream object which will be used in place of stdout

        """
        return sys.stdout

    def checkpoint_message(self, exp, title, msg, status):
        pass

