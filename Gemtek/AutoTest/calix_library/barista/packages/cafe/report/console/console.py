__author__ = 'akhanov'

from cafe.report.report import Report
from cafe.core.db import TestSuite
from cafe.core.config import get_config

import sys

class ConsoleReport(Report):
    def __init__(self, db, config):
        self.__db = db
        self._config = config

    def generate(self):
        fstream = sys.stdout
        # self.__db._update_all_testsuite_result()

        with self.__db.get_session() as s:
            ts = s.query(TestSuite).all()

            ts_total = len(ts)

            tc_total = 0
            tc_pass = 0
            tc_fail = 0
            tc_inde = 0

            for t in ts:
                fstream.write("*** test suite report (%s) ***\n" % t.name)
                report = "\n".join(self.__db.get_testsuite_report_text(t.test_suite_id).split('\n')[1:])

                fstream.write("%s\n" % report)

                tc_total += len(t.test_cases)
                tc_pass += len([i for i in t.test_cases if i.status == "pass"])
                tc_fail += len([i for i in t.test_cases if i.status == "fail"])
                tc_inde += len([i for i in t.test_cases if i.status == "indeterminate"])

        fstream.write("\nResult Path: %s\n" % get_config().cafe_runner.test_result_path)
        fstream.write("Log Path: %s\n\n" % get_config().cafe_runner.log_path)
        fstream.write("Total: %s test cases in %s test suites.\n" % (tc_total, ts_total))
        fstream.write("%s passed, %s failed, %s indeterminate.\n" % (tc_pass, tc_fail, tc_inde))



