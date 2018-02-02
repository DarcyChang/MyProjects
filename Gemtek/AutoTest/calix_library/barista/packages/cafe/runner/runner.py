__author__ = 'akhanov'

import glob
import imp
import os
import re
import pprint
import sys
import inspect
import warnings
import traceback
import signal
from cafe.core.config import get_config
from cafe.runner.utilities import change_pwd
from cafe.core.shutdown import Shutdown
from cafe.runner.test_suite_detect import has_test_suite
from cafe.util.version import get_version_info

from cafe.runner.tctools import TestSuiteState


def find_files(path):
    """An iterator that finds Python files in the specified path to execute test suites from

    Args:
        path (str): The root path to search

    Yields:
        str: The path of the next file found inside the path

    """
    for wlk in os.walk(path):
        subdir = wlk[0]
        for tc_file in glob.glob(subdir + os.path.sep + "*.py"):
            if has_test_suite(tc_file):
                yield tc_file


def run(fname, logger, pass_exceptions=True):
    """Imports the specified python file as a module, and executes Cafe Test Suites found within
    Handles any errors while importing and executing test suites, so that the next python file is not affected

    Args:
        fname (str): The path and name of the python file to import
        logger (cafe.core.logger.CLogger): The logger object to log to

    """
    logger.debug("Cafe Runner - found file '%s'" % fname)

    module_name = "".join(fname.split(".."))
    module_path = module_name.split(os.path.sep)

    if len(module_path) > 1:
        module_name = ".".join(module_path[1:])
    else:
        module_name = module_path[0]

    module_name = (module_name.strip("."))[0:-(len(".py"))]

    modpath = module_name.split(".")

    for i in range(1, len(modpath)):
        key = ".".join(modpath[0:i])
        sys.modules[key] = __file__

    load_successful = False

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            module = imp.load_source(module_name, fname)
            load_successful = True
        except Exception as e:
            if pass_exceptions:
                tb = traceback.format_exc()
                print(tb)
                logger.debug(tb)

                msg = "Errors found while importing %s, try executing the script directly before using Cafe Runner" % fname
                print(msg)
                logger.debug(msg)
            else:
                raise e

    if load_successful:
        objects = inspect.getmembers(sys.modules[module_name])

        path = os.path.dirname(os.path.realpath(fname))

        with change_pwd(path):
            for i in objects:
                try:
                    if '_cafe_test_suite' in dir(i[1]) and i[1]._cafe_test_suite:
                        (i[1])()
                except Exception as e:
                    print(traceback.format_exc())


def main(pass_exceptions=True):
    """Main procedure for execution of the Cafe Test Runner. Initializes the logging and configuration subsystems.
    """
    if '--version' in sys.argv:
        print(get_version_info())
        return

    from cafe.outputmanager.outputs import register_streams
    from cafe.runner.parameters.options import options

    register_streams()

    options.load_command_line_args()
    options.apply()


    # Logging Paths & Files
    # runner_state.logger.enable_file_logging("test_log.log")

    config = get_config()

    rs = config.runner_state

    rs.executing_in_runner = True

    """
    logfile = os.path.realpath(config.cafe_runner.log_path) + os.path.sep + config.cafe_runner.runner_log_name
    rs.logger.enable_file_logging(logfile)
    rs.logger.set_console(config.logger.console)
    rs.logger.set_level(config.logger.level)
    """

    path = os.path.realpath(os.path.expanduser(config.cafe_runner.path))

    rs.logger.debug("Cafe Runner - Parameter Loading Complete")
    rs.logger.debug("Cafe Runner - Execution Started")

    sys.path.append(".")
    parent_dir = os.path.dirname(os.path.realpath(os.curdir))

    if re.match("^.*\.py$", path):
        sys.path.append(os.path.dirname(path))
        run(path, rs.logger, pass_exceptions)
        sys.path.remove(os.path.dirname(path))
    else:
        for i in find_files(path):
            temp_path = os.path.dirname(i)
            sys.path.append(temp_path)
            run(i, rs.logger, pass_exceptions)
            sys.path.remove(temp_path)

    rs.logger.debug("Cafe Runner - Execution Finished")

    """
    from cafe.report.console.console import ConsoleReport
    from cafe.core.db import get_test_db
    db = get_test_db()

    #c = ConsoleReport(db)
    c = config.cafe_runner.report_type(db)
    c.generate()
    """

if __name__ == "__main__":
    main()
