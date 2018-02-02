__author__ = 'akhanov'

import traceback
import sys
import pprint
from cafe.runner.parameters.options import options
from cafe.core.config import get_config
from cafe.runner.utilities import set_test_case_tag, get_test_case_id, get_test_case_assignee
from cafe.runner.tctools import get_last_tc_result, get_test_suite_config
from cafe.util.helper import get_cfs
from cafe.core.db import get_test_db, TestDB
import inspect

class test_case:
    """This is a decorator that marks the function as a Cafe Test Case

    Args:
        skip: If true, the execution of the test case will be skipped

    Returns:
        object: The object that wraps the decorated function with test case properties

        This function currently cannot be executed outside of a Test Suite.
        This function handles any exceptions which are raised in the test case's code, as well as trigger the callback
        functions defined in the currently used Renderer (see cafe.runner.renderers package for examples of those).
        These callbacks include test case start/stop events, exception event, etc. Output to stdout is also manipulated
        in accordance to the currently set parameters.

    Example:
        ::

            @cafe.test_case()
            def my_test_case(arg1, arg2):
                print("You passed in: %s and %s!" % (arg1, arg2))

            # This test case will be skipped
            @cafe.test_case(skip=True)
            def my_skip_case():
                print("I am being skipped :(")

            @cafe.test_suite()
            def test_suite():
                cafe.register_test_case(my_test_case, args=["Hello", "world"])

                # This one will be skipped, because skip=True above
                cafe.register_test_case(my_skip_case)

                # You can also call them directly!
                my_test_case("Hello", "Again")

                cafe.run_test_cases()

    """
    def __init__(self, skip=False):
        """Remembers the decorator parameters
        """
        self.skip = skip
        self.__rs = get_config().runner_state

    def __call__(self, func):
        """Invoked when the decorated function is called

        Args:
            func: The function being decorated. This is done automatically when using the decorator syntax

        Returns:
            The wrapper which will be executed in place of the decorated function

        """
        func._cafe_test_case = True

        def wrapper(*args, **kwargs):
            """The wrapper function which will be executed in place of the decorated function
            The "hidden" test case handling logic is implemented here
            The wrapper catches any exceptions that occur within the test case and log them.
            If we are already in a test case, the wrapper behaves like a normal python function
            instead, without test case related logging and such.

            Args:
                args: The list of arguments passed in externally
                kwargs: The dictionary of named arguments passed in externally

            """
            
            try:
                # Is there already a test case? Then just run the function
                get_test_db().get_current_testcase()
                return func(*args, **kwargs)
            except TestDB.CafeNoCurrentTestCase:
                # No current test case? Good, carry on!
                pass

            if self.skip:
                self.__rs.callbacks.skip_test_case(wrapper)
                return

            if get_test_suite_config().abort_on_failure:
                try:
                    if get_last_tc_result() == 'fail':
                        self.__rs.callbacks.skip_test_case(wrapper)
                        return
                except IndexError:
                    pass

            self.__rs.callbacks.start_test_case(wrapper)

            # try:
            #     test_id = func._cafe_tc_id
            # except:
            #     test_id = get_test_case_id(func)

            # print("")
            # print("*" * 10 + " test case running - %s " % func.__name__ + "*" * 10)
            # print("")

            tmp_stdout = sys.stdout
            sys.stdout = self.__rs.callbacks.get_stdout_destination()

            try:

                func(*args, **kwargs)
            except Exception as e:
                sys.stdout = tmp_stdout
                tb_text = traceback.format_exc().strip().split('\n')
                tb = '\n'.join(tb_text[0:1] + tb_text[3:]) + '\n'

                self.__rs.callbacks.test_case_exception(wrapper, e, tb)
            finally:
                sys.stdout = tmp_stdout
                tc_info = self.__rs.callbacks.end_test_case(wrapper)
                self.__rs.callbacks.process_test_case_results(wrapper, tc_info)

        set_test_case_tag(func, 'test_id', get_test_case_id(func))
        set_test_case_tag(func, 'assignee', get_test_case_assignee(func))
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper._cafe_test_case = True

        return wrapper


class test_suite:
    """This is a decorator that marks the function as a Cafe Test Suite

    Args:
        skip: If true, the execution of the test suite will be skipped

    Returns:
        function: The function with special test suite properties added to it

        The wrapper handles any exceptions that are raised inside the test suite function, and triggers any Callbacks
        in the currently set Renderer (see cafe.runner.renderers package for examples of those). These callbacks include
        when the test suite starts, stops, fails due to an exception, etc. Unlike test cases, test suites can be called
        standalone.

    Example:
        ::

            @cafe.test_suite()
            def my_test_suite():
                pass

            # Just like test cases, test suites can be skipped
            @cafe.test_suite(skip=True)
            def my_skip_suite():
                pass

            # Unlike test cases, we can call test suites from anywhere
            my_test_suite()
            my_skip_suite()

    """
    def __init__(self, skip=False):
        """Saves the decorator parameters
        """
        self.skip = skip
        self.__rs = get_config().runner_state

    def __call__(self, func):
        """Invoked when the decorated function is called

        Args:
            func: The function being decorated

        Returns:
            The wrapper which will be executed in place of the decorated function

        """
        func.cafe_test_suite = True

        def wrapper(*args, **kwargs):
            """The wrapper function which will be executed in place of the decorated function
            The "hidden" test suite handling logic is implemented here

            Args:
                args: The list of arguments passed in externally
                kwargs: The dictionary of named arguments passed in externally

            """
            options.apply()
            # get_cfs().create_cafe_paths()

            if self.skip:
                self.__rs.callbacks.skip_test_suite(func)
                return

            self.__rs.callbacks.start_test_suite(func)

            try:
                # print("")
                # print("*" * 10 + " test suite running - %s " % func.__name__ + "*" * 10)
                # print("")
                func(*args, **kwargs)
            except Exception as e:
                tb_text = traceback.format_exc().strip().split('\n')
                tb = '\n'.join(tb_text[0:1] + tb_text[3:]) + '\n'

                self.__rs.callbacks.test_suite_exception(func, e, tb)
            finally:
                self.__rs.callbacks.end_test_suite(func)

        wrapper.__name__ = func.__name__
        wrapper._cafe_test_suite = True

        return wrapper

