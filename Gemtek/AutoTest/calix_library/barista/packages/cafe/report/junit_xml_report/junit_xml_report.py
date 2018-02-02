__author__ = 'akhanov'

from cafe.report.report import Report
from cafe.core.db import FAIL, PASS, INDETERMINATE, ERROR
from cafe.core.db import TestSuite as CafeTestSuite

from cafe.core.utils import create_folder
from junit_xml import TestSuite, TestCase
import os


class JUnitReport(Report):
    """Module for generating a JUnit XML Report
    """
    def generate(self):
        """Generate the JUnit XML Report based on results in the DB
        Creates JUnit XML files in path specified by runner settings
        """
        test_suites = []
        conf = self._config
        filename = conf.path + os.path.sep + conf.xml_name
        create_folder(filename)

        with self._db.get_session() as s:
            cafe_test_suites = s.query(CafeTestSuite)

            for ts in cafe_test_suites:
                test_cases = []
                ts_name = ts.name

                for tc in ts.test_cases:
                    tc_name = tc.global_id
                    tc_classname = tc.name
                    # tc_classname = ts.name
                    tc_duration = tc.elapsed_time
                    tc_stdout = ""
                    tc_stderr = ""

                    failed_steps = []
                    error_steps = []

                    for tc_step in tc.test_steps:
                        output = "%s:%s :\n\t%s\n" % (tc_step.filename, tc_step.line, tc_step.msg)
                        output += "Command:\n%s\n" % tc_step.cmd
                        output += "Response:\n%s\n" % tc_step.response

                        tc_stdout = output

                        msg = {
                            "message": "%s:%s : %s" % (tc_step.filename, tc_step.line, tc_step.msg),
                            "output": tc_step.response
                        }

                        if tc_step.status == FAIL:
                            failed_steps.append(msg)
                        elif tc_step.status == ERROR:
                            error_steps.append(msg)

                    junit_tc = TestCase(tc_name, tc_classname, tc_duration, tc_stdout, tc_stderr)

                    for step in failed_steps:
                        junit_tc.add_failure_info(**step)

                    for step in error_steps:
                        junit_tc.add_error_info(**step)

                    test_cases.append(junit_tc)

                test_suites.append(TestSuite(ts_name, test_cases))

        with open(filename, 'w') as f:
            TestSuite.to_file(f, test_suites, prettyprint=True)

if __name__ == "__main__":
    from cafe import get_test_db
    from cafe import get_config
    from cafe.runner.parameters.options import options
    from pprint import pprint

    # Set up report
    options.set("cafe_runner.reports", "junit_test")
    options.set("junit_test:junit_xml_report.path", "${cafe_runner.test_result_path}/junit/")
    options.apply()
    pprint(get_config())

    # r = JUnitReport(get_test_db(), get_config())
    # r.generate()

