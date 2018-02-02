__author__ = 'akhanov'

import inspect
import pprint
import os
import os.path
import importlib
import random
import sys

from cafe.runner.utilities import get_test_suite_name
from cafe.runner.utilities import get_test_case_id
from cafe.runner.utilities import set_test_case_id
from cafe.runner.utilities import get_test_case_assignee
from cafe.runner.utilities import set_test_case_assignee
from cafe.runner.utilities import get_test_case_tags
from cafe.core.db import get_test_db, TestCase, TestSuite, TestDB

from cafe.core.utils import SingletonClass
from cafe.core.config import get_config


def get_last_tc_result():
    try:
        tc_id = get_test_db().get_previous_testcase_id()

        with get_test_db().get_session() as session:
            q = session.query(TestCase).filter(TestCase.test_case_id == tc_id).one()
            result = q.status
    except TestDB.CafeNoPreviousTestCase:
        result = "indeterminate"

    return result


def get_test_suite_config():
    ret = get_config().test_suite

    try:
        ts_id = get_test_db().get_current_testsuite_id()

        with get_test_db().get_session() as session:
            q = session.query(TestSuite).filter(TestSuite.test_suite_id == ts_id)
            results = q.all()
            name = str(results[0].name).split(".")[-1]
    except TestDB.CafeNoCurrentTestSuite:
        pass
    else:
        if name in get_config() and '__type__' in get_config()[name] and get_config()[name]['__type__'] == 'test_suite':
            ret = get_config()[name]

    return ret


@SingletonClass
class _TestSuiteState(object):
    """Singleton Class which contains the states of currently executing test suites
    """
    __data = {}

    def __init__(self):
        """Initializes the TestSuiteState structure
        """
        pass

    def add_ts(self, test_suite_name, topology_backup=None, param_backup=None):
        """Add a new test suite to TestSuiteState for tracking

        :param param_backup:
        Args:
            test_suite_name (str): The name of the test suite to add
            topology_backup (Optional[dict]): Defaults to None. The Topology snapshot saved before the execution of
                this test suite

        Raises:
            KeyError: If test suite with that name already exists in TestSuiteState

        """
        if test_suite_name in self.__data:
            raise KeyError("Test suite already running")
        else:
            self.__data[test_suite_name] = {'test_cases': [], 'topology_backup': topology_backup,
                                            'param_backup': param_backup}

    def close_ts(self, test_suite_name):
        """Removes the test suite from TestSuiteState - usually upon completion of the test suite

        Args:
            test_suite_name (str): The name of the test suite to close

        Raises:
            KeyError: If the test suite with that name does not exist in TestSuiteState

        """
        del(self.__data[test_suite_name])

    # def add_tc(self, test_suite_name, test_case_func, test_case_id, test_case_assignee, args, kwargs):
    def add_tc(self, test_suite_name, test_case_func, args, kwargs, **kwarguments):
        """Adds a test case under the specified test suite

        Args:
            test_suite_name (str): The name of the test suite to add the test case to
            test_case_func (function): The function pointer to the test case function
            test_case_id (str): The ID of the test case (specified either in PyDoc for the test case, or overridden by
                cafe.register_test_case()
            args (list): The list of arguments to pass to the test case
            kwargs (dict): The dictionary of keyword arguments to pass to the test case

        """
        assert("test_id" in kwarguments)
        assert("assignee" in kwarguments)

        # data = {"function": test_case_func,
        #         "id": kwarguments['test_case_id'],
        #         "assignee": kwarguments['test_case_assignee'],
        #         "args": args,
        #         "kwargs": kwargs}

        data = {"function": test_case_func,
                "args": args,
                "kwargs": kwargs,
                "tags": kwarguments.copy()
                }

        self.__data[test_suite_name]['test_cases'].append(data)

    def get_tc_list(self, test_suite_name):
        """Fetch the list of registered test cases in the specified test suite

        Args:
            test_suite_name (str): The name of the test suite

        Returns:
            list: List of function descriptors

            The format of a function descriptor is the following.

                {
                    "function": the test case function pointer,
                    "id": the test case id,
                    "args": the argument list for the test case,
                    "kwargs": the keyword argument dict for the test case,
                }

        """
        return self.__data[test_suite_name]['test_cases']

    def wipe(self):
        """Cleans the TestSuiteState data structure
        Removes all test suites and associated test cases - a fresh start.

        """
        self.__data = {}

    def dump(self):
        """Fetches the entire data structure
        Meant for debugging purposes

        Returns:
            dict: The dictionary describing the contents of the TestSuiteState

        """
        return self.__data

TestSuiteState = _TestSuiteState()
"""_TestSuiteState: The initialized singleton TestSuiteState object
"""


def get_test_cases(module=None, **kwargs):
    """Fetches a list of test case function objects based on specified criteria. Useful for dynamic addition of
    test cases to a test suite.

    Args:
        module (module): Defaults to None. The module to search for test cases. If None, the module that called
            get_test_cases() will be searched
        kwargs (dict): Keyword arguments which specify the filter to apply to the search. The search is done on test
            case tags specified in the pydoc for the test case.

    Returns:
        list: a list of test case function objects. These functions can then be added to a test suite using
        register_test_case().
    """
    ret = []

    if module is None:
        # pprint.pprint(inspect.stack())
        module_name = inspect.stack()[1][1]
        try:
            mod_ref = sys.modules[inspect.getmodulename(module_name)]
        except KeyError:
            mod_ref = sys.modules['__main__']
    else:
        mod_ref = module

    for i in mod_ref.__dict__:
        func = None
        try:
            if mod_ref.__dict__[i]._cafe_test_case is True:
                func = mod_ref.__dict__[i]
        except:
            pass

        if func is not None:
            tags = get_test_case_tags(func)

            match = True

            for key in kwargs:
                if (key in tags) and (kwargs[key] == tags[key]):
                    match &= True
                else:
                    match = False

            if match:
                ret.append(func)

    return ret


# def register_test_case(func, args=[], kwargs={}, test_id=None, assignee=None):
def register_test_case(func, args=[], kwargs={}, **kwarguments):
    """Registers the specified test case to its parent test suite and prepares it for execution.

    Args:
        func (function): The function pointer to the test case that is being registered
        args (list): The list of arguments which will be passed to the test case when it is executed
        kwargs (dict): The dictionary of keyword arguments which will be passed to the test case when it is executed
        test_id (Optional[str]): Defaults to None. If set, this ID will be used during execution of this test case
            instead of the one specified in the test case's pydoc
        assignee (Optional[str]): Defaults to None. If set, this assignee will be used during execution of this test case
            instead of the one specified in the test case's pydoc

    Example:
        ::

            # Define a test case which we will register in our suite
            @cafe.test_case()
            def tc(my_argument_1, my_argument_2):
                '''
                @test_id=123456GlobalID
                @assignee=someone
                '''
                pass

            # Define the suite
            @cafe.test_suite()
            def my_test_suite():
                # Pass the list of arguments to the test case
                cafe.register_test_case(tc, args=["Hello", "World"])

                # You can also use keyword arguments!
                cafe.register_test_case(tc, kwargs={"my_argument_1": "Hello", "my_argument_2": "World"})

                # You can even mix the two!
                cafe.register_test_case(tc, args=["Hello"], kwargs={"my_argument_2": "World"})

                # Overriding global ID's is also possible
                # Now, the ID won't be "123456GlobalID", it will be "I_AM_OVERRIDDEN"
                cafe.register_test_case(tc, test_id="I_AM_OVERRIDDEN")

                # Overriding assignee is also possible
                # Now, assignee won't be "someone", it will be "ASSIGNEE_WAS_OVERRIDDEN"
                cafe.register_test_case(tc, assignee="ASSIGNEE_WAS_OVERRIDDEN")

    """
    config = get_config()
    logger = config.runner_state.logger

    stack = inspect.stack()
    caller = stack[1][3]
    filepath = stack[1][1]

    if 'test_id' not in kwarguments:
        tc_id = get_test_case_id(func)
    else:
        tc_id = kwarguments['test_id']

    if 'assignee' not in kwarguments:
        tc_assignee = get_test_case_assignee(func)
    else:
        tc_assignee = kwarguments['assignee']

    if caller == '<module>':
        print("I GOT CALLED FROM A MODULE: BAD!!!")

    ts_name = get_test_suite_name(filepath + os.path.sep + caller)
    TestSuiteState.add_tc(ts_name, func, args, kwargs, test_id=tc_id, assignee=tc_assignee)

    logger.debug("Registered test case %s ('%s')" % (func.__name__, tc_id))


def run_test_cases(sort_method=None):
    """Execute the test cases registered to the parent test suite

    Args:
        sort_method (Optional[function]): Defaults to the value of the runtime parameter "cafe_runner.tc_exec_order".
            The key function used to determine the order of execution of test cases in the test suite.

    Example:
        ::

            @cafe.test_case()
            def tc1():
                pass

            @cafe.test_case()
            def tc2():
                pass

            @cafe.test_suite()
            def ts():
                cafe.register_test_case(tc1)
                cafe.register_test_case(tc2)

                cafe.run_test_cases()

                # You can also override the sort method
                cafe.run_test_cases(sort_method=cafe.runner.utilities.in_order)

                # Or make your own!

                def my_custom_sort(item):
                    return hash(item)

                cafe.run_test_cases(sort_method=my_custom_sort)

    """
    config = get_config()
    logger = config.runner_state.logger

    if sort_method is None:
        sort_method = get_config().cafe_runner.tc_exec_order

    stack = inspect.stack()
    caller = stack[1][3]
    filepath = stack[1][1]

    if caller == '<module>':
        print("I GOT CALLED FROM A MODULE: BAD!!!")

    ts_name = get_test_suite_name(filepath + os.path.sep + caller)
    tc_list = TestSuiteState.get_tc_list(ts_name)

    for i in sorted(tc_list, key=sort_method):
        func = i['function']
        # tc_id = i['id']
        tc_id = i['tags']['test_id']
        # assignee = i['assignee']
        assignee = i['tags']['assignee']
        args = i['args']
        kwargs = i['kwargs']

        include_list = config.cafe_runner.tc_include_list
        exclude_list = config.cafe_runner.tc_exclude_list

        in_include = (include_list is None) or (tc_id in include_list) or (func.__name__ in include_list)
        in_exclude = (exclude_list is not None) and ((tc_id in exclude_list) or (func.__name__ in exclude_list))

        if in_include and not in_exclude:
            # Set new test case id, in case of override
            original_id = get_test_case_id(func)
            original_assignee = get_test_case_assignee(func)
            set_test_case_id(func, tc_id)
            set_test_case_assignee(func, assignee)

            setattr(func, "_cafe_tc_id", tc_id)

            func(*args, **kwargs)
            # Restore the original test case id, for reuse
            # print ">>>>> %s <<<<<" % get_last_tc_result()
            set_test_case_id(func, original_id)
            set_test_case_assignee(func, original_assignee)
        else:
            logger.info("SKIPPING test case %s ('%s') due to include/exclude list contents" % (func.__name__, tc_id))


def get_test_cases_by_package(package, depth=3, **kwargs):
    """
    Fetches a list of test case function objects based on specified criteria in a package.

    Args:
        package (package): Package, which includes several modules.
        depth (int): The max depth for package, by default depth is 3.
        kwargs (dict): Keyword arguments which specify the filter to apply to the search. The search is done on test
            case tags specified in the pydoc for the test case.

    Returns:
        list: a list of test case function objects. These functions can then be added to a test suite using
        register_test_case().

    Example:
        ::

            # 1, get all test cases in user_access
            tcs = get_test_cases_by_package('dpu_mdu_automation.test_cases.security.user_access')

            # 2, get all test cases in user_access by tag:user_access
            tcs = get_test_cases_by_package('dpu_mdu_automation.test_cases.security.user_access', tag='user_access')

            # 3, get all test cases in user_access by test_id:875103CLIE3-16F
            tcs = get_test_cases_by_package('dpu_mdu_automation.test_cases.security.user_access', test_id='875103CLIE3-16F')

            # 4, get all test cases in security, depth=2, by assignee:rjin
            tcs = get_test_cases_by_package('dpu_mdu_automation.test_cases.security', depth=2, assignee='rjin')

    """

    ret = []

    # 1, get package absolute path
    packages = package.split('.')
    root = packages[0]

    package_path = None
    for p in sys.path:
        if root in p:
            package_path = os.path.join(p[:p.find(root)], os.path.sep.join(packages))
            break

    if package_path is None:
        return ret

    # 2, list all modules in the package and dynamically import module
    counts = package_path.count(os.path.sep)
    for dirpath, dirnames, filenames in os.walk(package_path):
        d = dirpath.count(os.path.sep) - counts + 1
        if d > depth:
            continue

        if filenames:
            module_base_name = dirpath[dirpath.find(root):].replace(os.path.sep, '.')
            for filename in filenames:
                if filename.startswith('tc_') and filename.endswith('.py'):
                    try:
                        m = importlib.import_module(module_base_name + '.' + filename[:-3])
                    except Exception as e:
                        logger = get_config().runner_state.logger
                        logger.warning('there is Exception[%s] when importing %s module' % (e, filename[:-3]))
                        continue

                    test_cases = get_test_cases(module=m, **kwargs)
                    if test_cases:
                        ret.extend(test_cases)

    return ret
