from __future__ import print_function

__author__ = 'akhanov'

import sys
import io
import re

from callbacks import Renderer
from cafe.runner.utilities import get_test_suite_name
from cafe.core.db import get_test_db, PASS, FAIL, UNKNOWN

from cafe.outputmanager.outputmanager import output_manager
from cafe.outputmanager.outputs import TC_STDOUT

stdout = sys.stdout


class RedirectedStream(object):
    def __init__(self, base_stream=sys.stdout):
        self.__stream = base_stream

        self.closed = self.__stream.closed
        self.encoding = self.__stream.encoding
        self.errors = self.__stream.errors
        self.mode = self.__stream.mode
        self.name = self.__stream.name
        self.newlines = self.__stream.newlines
        self.softspace = self.__stream.softspace

    def close(self):
        self.__stream.close()

    def flush(self):
        self.__stream.flush()

    def fileno(self):
        return self.__stream.fileno()

    def isatty(self):
        return self.__stream.isatty()

    def next(self):
        return self.__stream.next()

    def read(self, size=-1):
        return self.__stream.read(size)

    def readline(self, size=-1):
        return self.__stream.readline(size)

    def readlines(self, sizehint=-1):
        return self.__stream.readlines(sizehint)

    def seek(self, offset, whence=io.SEEK_SET):
        self.__stream.seek(offset, whence)

    def tell(self):
        return self.__stream.tell()

    def truncate(self, size=None):
        self.__stream.truncate(size)

    def write(self, str):
        self.__stream.write(str)

    def writelines(self, sequence):
        for i in sequence:
            self.write(i)


class TextRenderer(Renderer):
    """A renderer which outputs results to the console
    """
    def __init__(self, logger):
        super(TextRenderer, self).__init__(logger)

        self.tc_name_size = 0
        self.tc_has_output = False

    def skip_test_suite(self, func):
        """Callback of when a test suite is skipped.
        Prints "SKIP" to console

        Args:
            func (function): The test suite function in question

        """
        name = get_test_suite_name(func)
        print("%s: SKIP" % name, file=stdout)
        super(TextRenderer, self).skip_test_suite(func)

    def skip_test_case(self, func):
        """Callback of when a test case is skipped.
        Prints "SKIP" to console

        Args:
            func (function): The test case function in question

        """
        super(TextRenderer, self).skip_test_case(func)

    def start_test_suite(self, func):
        """Callback of when a test suite is started.
        Prints a header to console

        Args:
            func (function): The test suite function in question

        """
        name = get_test_suite_name(func)
        # print("\n----- %s -----" % name, file=stdout)
        # print("\n----- %s -----" % name, file=output_manager['raw_stdout'])
        print("\n\033[1m[ %s ]\033[0m" % name, file=output_manager['raw_stdout'])
        super(TextRenderer, self).start_test_suite(func)

    def end_test_suite(self, func):
        """Callback of when a test suite is done executing.
        Prints an empty space to console

        Args:
            func (function): The test suite function in question

        """
        print()
        super(TextRenderer, self).end_test_suite(func)

    def start_test_case(self, func):
        """Callback of when a test case starts.
        Hides all printout of the testcase

        Args:
            func (function): The test case function in question

        """
        # str = "%s: " % func.__name__
        # str = "\t[ %s ]" % func.__name__
        str = "    [ %s ]" % func.__name__

        self.tc_name_size = len(str)

        print(str, file=output_manager.raw_stdout, end="")
        # sys.stdout = open(os.devnull, "w")
        super(TextRenderer, self).start_test_case(func)
        output_manager.tc_stdout.new_section()
        output_manager.tc_stderr.new_section()

    def end_test_case(self, func):
        """Callback of when a test case is done executing
        Resumes printout

        Args:
            func (function): The test suite function in question

        """
        # sys.stdout = stdout
        #print()
        # self.tc_has_output = False
        return super(TextRenderer, self).end_test_case(func)

    def start_test_step(self, title):
        # output_manager.tc_stdout.new_section()
        # output_manager.tc_stderr.new_section()
        # output_manager.raw_stdout.new_section()
        # comment it by David, because it appear in robot framework and make it difficult to check
        # print("\n        %s" % title, end="", file=output_manager.raw_stdout)
        # output_manager.tc_stdout.new_section()
        # output_manager.tc_stderr.new_section()
        # output_manager.raw_stdout.new_section()
        pass

        return super(TextRenderer, self).start_test_step(title)

    def end_test_step(self, title, tc_obj):
        ret = super(TextRenderer, self).end_test_step(title, tc_obj)
        
        # If tc_obj is None, means we are not in a test case
        if tc_obj is not None:
            output_manager.tc_stdout.new_section()
            output_manager.step_stdout.new_section()

            print(tc_obj.title, file=output_manager.step_stdout)
            # output_manager.step_stdout.new_section()

            if tc_obj.status == PASS:
                ss = '\033[0;32mPASS\033[0m'
            elif tc_obj.status == FAIL:
                ss = '\033[0;31mFAIL\033[0m'
            else:
                ss = '\033[0;33mUNKNOWN\033[0m'

            print(ss, file=output_manager.step_stdout, end=": ")
            print(tc_obj.msg, file=output_manager.step_stdout)

        return ret

    def process_test_case_results(self, func, tcinfo):
        """Callback of when a test case's results are known
        Prints the result to console

        Args:
            func (function): The test suite function in question
            tcinfo: The tcinfo object which contains the status of the test case

        """
        if tcinfo.status == "pass":
            # print("\t%s: PASS" % func.__name__)
            string = '\033[0;32mPASS\033[0m'
            pass
        elif tcinfo.status == "fail":
            # print("\t%s: FAIL" % func.__name__)
            string = '\033[0;31mFAIL\033[0m'
            pass
        elif tcinfo.status == "indeterminate":
            # print("\t%s: INDETERMINATE" % func.__name__)
            string = "\033[0;33mINDETERMINATE\033[0m"
            pass

        # print("\n\t\t%s\n" % string, file=output_manager.raw_stdout)
        print("\n        %s\n" % string, file=output_manager.raw_stdout)
        # self.tc_name_size = 0
        # self.tc_has_output = False

    # def get_stdout_destination(self):
    #     outer = self
    #
    #     class TCPrinter(RedirectedStream):
    #         def __init__(self):
    #             super(TCPrinter, self).__init__()
    #             self.__initialized = False
    #             self.__sep = "\t| "
    #
    #         def write(self, str):
    #             # super(TCPrinter, self).write("[[[ WRITING: [%s] ]]]" % str)
    #             if not self.__initialized:
    #                 super(TCPrinter, self).write(self.__sep)
    #                 self.__initialized = True
    #                 outer.tc_has_output = True
    #
    #             for i in str:
    #                 if i == '\n':
    #                     super(TCPrinter, self).write("\n" + (" " * outer.tc_name_size) + self.__sep)
    #                 else:
    #                     super(TCPrinter, self).write(i)
    #
    #     ret = TCPrinter()
    #     # ret.write('\n')
    #
    #     return ret

    def get_stdout_destination(self):
        return output_manager[TC_STDOUT]

    def test_case_exception(self, func, e, tb):
        """Callback for when an exception is encountered inside a test case
        Logs the error.

        Args:
            func (function): The test case function in question
            e (Exception): The exception object
            tb (str): The traceback
        """
        # self.logger.error("EXCEPTION test suite '%s': %s\n\n%s" % (func.__name__, e.message, tb))

        split = tb.strip().split('\n')

        for i in split:
            # if self.tc_has_output:
            #     prefix = "\n" + (" " * self.tc_name_size)
            # else:
            #     prefix = ""
            #
            # print(prefix + "        ! %s" % i, file=sys.__stdout__, end="")
            # self.tc_has_output = True
            # print("\033[0;31m%s\033[0m" % i, file=output_manager.tc_stderr)
            print(i, file=output_manager.tc_stderr)

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

        # db.create_teststep(ts_id, tc_id, "Unhandled Exception", response=tb, status="error",
        #                    filename=filename, line=line, cmd=command)
        get_test_db().create_teststep("Unhandled Exception", response=tb, status="error",
                           filename=filename, line=line, cmd=command)

    def checkpoint_message(self, exp, title, msg, status):
        # print(msg, file=output_manager.tc_stdout)
        pass

