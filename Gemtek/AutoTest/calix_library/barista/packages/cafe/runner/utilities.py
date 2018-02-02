from __future__ import print_function

import types
import random
import os
import sys
import re
import getpass
import inspect

from contextlib import contextmanager
from glob import glob
from cafe.core.config import get_config
from ConfigParser import ConfigParser

from cafe.core.db import PASS, FAIL, INDETERMINATE, INFO, WARN, ERROR
from cafe.core.db import get_test_db, TestDB

__author__ = 'akhanov'


def get_test_case_tag(func, tag):
    ret = func.__name__
    found = False
    tagname = "@%s=" % tag

    try:
        docstr = func.__doc__.split("\n")
    except:
        docstr = []

    for line in docstr:
        if tagname in line:
            if not found:
                try:
                    ret = line.split(tagname)[1]
                except IndexError as e:
                    raise ValueError("No valid ID found after '%s' directive, %s"
                                     % (tagname, e))

                found = True
            else:
                raise ValueError("%s already set to '%s'; You cannot set more than one %s per test case."
                                 % (tag, ret, tag))

    return ret


def set_test_case_tag(func, tag, value):
    """Sets (overrides existing) test case tag with the specified value

    Args:
        func (function): The test case function to set the ID for.
        tag (str): The tag name
        value (str): The value to assign to the tag
    """
    tagname = "@%s" % tag

    try:
        docs = func.__doc__.split("\n")
    except AttributeError as e:
        # since we append __doc__ in next
        # print("func docstring is none, !! %s" % e)
        docs = []

    for i in docs:
        m = re.match("^\s*@\s*(\S+)\s*=\s*\S+\s*$", i)
        if (m is not None) and (m.group(1) == tag):
            docs.remove(i)

    docs.append("%s=%s" % (tagname, value))
    func.__doc__ = '\n'.join(docs)


def get_test_case_tags(func):
    ret = {}

    try:
        docstr = func.__doc__.split("\n")
    except:
        docstr = []

    for line in docstr:
        m = re.match("^\s*@\s*(\S+)\s*=\s*(\S+)\s*$", line)
        if m is not None:
            ret[m.group(1)] = m.group(2)

    return ret


def get_test_suite_name(func):
    """Fetches the name of the test suite.
    The name consists of the file system path to the test suite and the
    declared name of the test suite.

    Args:
        func (function): The test suite function

    Returns:
        str: The full, unique name of the test suite

    """
    module_path = ""

    # if type(func) is types.FunctionType:
    if hasattr(func, '__call__'):
        module_path = sys.modules[func.__module__].__file__ + os.path.sep + func.__name__
    # elif type(func) is types.StringType:
    elif isinstance(func, basestring):
        module_path = func

    def pystrip(file_basename):
        m = re.search("^(?P<name>.*?)(\.pyc|\.py|\.pyo|)$", file_basename)
        return m.group('name')

    chain = ".".join(map(pystrip, module_path.split(os.path.sep))).strip(".")

    return chain


def get_test_case_id(func):
    """Fetches the ID specified in the pydoc of the test case function.
    If ID is missing from the pydoc, the name of the function is used instead.
    If more than one ID is found in the pydoc, an Exception is raised.

    Args:
        func (function): The test case function to retrieve the ID for.

    Returns:
        str: The ID of the specified test case.

    Raises:
        ValueError: If more than one ID is found in the test case's PyDoc or
    the ID is incorrectly formatted

    """
    ret = func.__name__
    found = False

    try:
        docstr = func.__doc__.split("\n")
    except AttributeError:
        # just return it
        # print("function docstring is none")
        return ret

    for line in docstr:
        if "@test_id=" in line:
            if not found:
                try:
                    ret = line.split("@test_id=")[1]
                except IndexError:
                    raise ValueError("No valid ID found after '@test_id=' directive")

                found = True
            else:
                raise ValueError("ID already set to '%s'; You cannot set more than one ID per test case." % ret)

    return ret


def get_test_case_assignee(func):
    """Fetches the assignee specified in the pydoc of the test case function.
    If the assignee is missing from the pydoc, the name of the current user is
    used instead. If more than one assignee is found in the pydoc, an Exception
    is raised.

    Args:
        func (function): The test case function to retrieve the assignee for.

    Returns:
        str: The assignee of the specified test case.

    Raises:
        ValueError: If more than one assignee is found in the test case's PyDoc
    or the ID is incorrectly formatted

    """
    ret = getpass.getuser()
    found = False

    try:
        docstr = func.__doc__.split("\n")
    except AttributeError:
        # just return it
        # print("function docstring is none")
        return ret

    for line in docstr:
        if "@assignee=" in line:
            if not found:
                try:
                    ret = line.split("@assignee=")[1]
                except IndexError:
                    raise ValueError("No valid assignee found after '@assignee=' directive")

                found = True
            else:
                raise ValueError("Assignee already set to '%s'; You cannot set more than one assignee per test case." %
                                 ret)

    return ret


def set_test_case_id(func, tc_id):
    """Sets (overrides existing) test case ID

    Args:
        func (function): The test case function to set the ID for.
        tc_id (str): The ID to set

    """
    try:
        docs = func.__doc__.split("\n")
    except AttributeError:
        # need docs in future
        # print("function docstring is none")
        docs = []

    for i in docs:
        if "@test_id" in i:
            docs.remove(i)

    docs.append("@test_id=%s" % tc_id)
    func.__doc__ = '\n'.join(docs)


def set_test_case_assignee(func, assignee):
    """Sets (overrides existing) test case ID

    Args:
        func (function): The test case function to set the ID for.
        tc_id (str): The ID to set

    """
    try:
        docs = func.__doc__.split("\n")
    except:
        docs = []

    for i in docs:
        if "@assignee" in i:
            docs.remove(i)

    docs.append("@assignee=%s" % assignee)
    func.__doc__ = '\n'.join(docs)


def in_order(item):
    """Function intended to be used as the key function for the Python built-in
    'sorted' function.
    Returns the weight of the item as 'zero', no matter what the item is, so
    the original order of the iterable is
    preserved.

    Args:
        item: The item to return the weight for.

    Returns:
        int: Constant (zero) weight for the item.

    """
    return 0


def randomized(item):
    """Function intended to be used as the key function for the Python built-in
    'sorted' function.
    Returns a random weight for the specified item, so that the iterable is
    sorted in a random order.

    Args:
        item: The item to return the weight for.

    Returns:
        int: Randomized weight for the item.

    """
    random.seed()
    return random.random()


@contextmanager
def change_pwd(path):
    """Context manager for changing the present working directory (pwd) for the
    block of code.

    Args:
        path: Directory to set as the new present working directory

    Yields:
        None. Yields to block of code after changing present working directory,
    then switches back after the block is
        complete

    Example:
        ::

            with change_pwd("/home/newcwd/"):
                # do_things() will be executed with working directory set to "/home/newcwd"
                do_things()

    """
    old_curdir = os.getcwd()
    os.chdir(path)

    yield

    os.chdir(old_curdir)


def executing_in_runner():
    """Detect if we are currently executing inside the Cafe Test Case Runner.

    Returns:
        True if the Cafe Test Case Runner is being used, False otherwise.

    """
    config = get_config()
    return config.runner_state.executing_in_runner


def print_console(message):
    """Prints a message to console output stream

    Args:
        message (str): The string you want to print
    """

    print(message, file=sys.__stdout__)


def print_log(message, level='INFO'):
    """Prints a message to the log

    Args:
        message (str): The string you want to print to the log
        level (Optional[str]): Defaults to INFO. The log level of the message.
    Can be TRACE, DEBUG, INFO, ERROR, or WARNING.
    """
    levels = ['TRACE', 'DEBUG', 'INFO', 'ERROR', 'WARNING']
    assert(level in levels)
    get_config().runner_state.logger.__getattribute__(level.lower())(message)


def print_report(message, status=INFO):
    """Adds a step with the specified message to the report

    Note:
        Depending on the report type, you may not be able to see this message.
    In particular, reports that do not show test steps (console_report, for
    example), will not show this message

    Args:
        message (str): the string you want to print to the report
        status (Optional[str]): Defaults to 'info'. The status of the step. Can
    be 'pass', 'fail', 'indeterminate', 'info', 'error', 'warn'.
    """
    levels = [PASS, FAIL, INDETERMINATE, INFO, ERROR, WARN]
    assert(status in levels)
    db = get_test_db()

    # try:
    #     ts_id = db.current_testsuite_id
    #     tc_id = db.current_testcase_id
    # except TestDB.CafeNoCurrentTestSuite:
    #     skip = True

    try:
        frame = inspect.stack()[1]
    except IndexError:
        raise Exception("%s must be called from another method" % print_report.__name__)

    fname = frame[1]
    line = frame[2]
    cmd = "\n".join(map(str.strip, frame[4]))

    db.create_teststep(message, msg=message, response=None, cmd=cmd, status=status, filename=fname, line=line)


def get_project_paths(options_struct, file_path, path_file_name="cafepath"):
    """
    Finds a project path file, sets the parent directory as project root, and
    loads any additionally defined path
    references from that file.

    Args:
        options_struct (cafe.runner.parameters.options._Options): The options structure
        file_path (str): The initial path where the procedure will look for the project path file. The procedure will
            descend down the tree path looking for the file.
        path_file_name (str): Defaults to 'cafepath'. The name of the project path file to look for.

    Returns:
        tuple: (filename, ret). filename is the name of the loaded project path file. ret is a dictionary of path
            reference -> real filesystem path key-value pairs.

    """
    dir_path = os.path.abspath(os.path.dirname(os.path.expandvars(os.path.expanduser(file_path))))
    chain = dir_path.split(os.path.sep)

    ret = {}
    found = False

    for i in range(len(chain), -1, -1):
        cur_path = os.path.sep.join(chain[0:i])
        assumed_filename = cur_path + os.path.sep + path_file_name

        if assumed_filename in glob(assumed_filename):
            options_struct.push_log_queue("Found Cafe Path File '%s'" % assumed_filename, "DEBUG")

            ret['project'] = os.path.dirname(assumed_filename)
            options_struct.push_log_queue("Setting Cafe Path 'project://' to '%s'" % ret['project'])

            with change_pwd(ret['project']):
                try:
                    cp = ConfigParser()
                    cp.read(assumed_filename)

                    for option in cp.options('paths'):
                        ret[option] = os.path.abspath(os.path.expanduser(os.path.expandvars(cp.get('paths', option))))
                        options_struct.push_log_queue("Setting Cafe Path '%s://' to '%s'" % (option, ret[option]))

                except IOError:
                    # just pass
                    pass

            found = True
            break

    if not found:
        options_struct.push_log_queue("File 'cafepath' not found in this project's directory tree. Cafe Path "
                                      " References (such as 'project://') will not function correctly.", "WARNING")

    return assumed_filename, ret

