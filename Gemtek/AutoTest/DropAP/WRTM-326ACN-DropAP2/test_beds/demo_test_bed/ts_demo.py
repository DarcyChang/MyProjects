__author__ = 'gliverm'

import cafe
from cafe.core.logger import init_logging
from stp.test_cases import tc_demo

if not cafe.executing_in_runner():
    # Get runner config file
    cafe.load_config_file("config/config.ini")

@cafe.test_suite()
def my_test_suite():

    # Test cases must be registered with Cafe prior to execution
    cafe.register_test_case(tc_demo.tc_123_sample_test_case)
    cafe.register_test_case(tc_demo.tc_777_test_case_with_arg, args=["Cafe"])
    cafe.register_test_case(tc_demo.tc_45679RGGUI_test_case_1, test_id="OVERRIDEN_1")
    cafe.register_test_case(tc_demo.tc_45679RGGUI_test_case_1, test_id="OVERRIDEN_2")
    cafe.register_test_case(tc_demo.tc_45679RGGUI_test_case_1)
    cafe.register_test_case(tc_demo.tc_45679RGGUI_test_case_1, test_id="OVERRIDEN_3", assignee="hubert")
    cafe.register_test_case(tc_demo.tc_888RGGUI_test_case_2)

    # Execute all registered test cases
    cafe.run_test_cases()

if not cafe.executing_in_runner():
    my_test_suite()

