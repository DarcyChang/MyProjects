__author__ = 'akhanov'

import os
import time
from datetime import datetime
from datetime import timedelta
import webbrowser

from tornado import template
from cafe.report.report import Report

from cafe.core.db import TestSuite
from cafe.core.db import TestCase


class HTMLReport(Report):
    def __init__(self, db, config):
        """Initialize the HTML Report generator

        Args:
            db: Database containing the results
            config: The configuration for this report instance

        """
        super(HTMLReport, self).__init__(db, config)
        self._report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.template = template.Loader(os.path.dirname(__file__)).load("template.tt")

    def generate(self):
        """Generate the HTML Report
        """
        # Replace variables
        html_file = open(self._config.filename, "w")
        params = {
            'title': 'Cafe Execution Report - %s' % self._report_timestamp,
            'test_suites': []
        }

        with self._db.get_session() as s:
            test_suites = s.query(TestSuite)

            for test_suite in test_suites:
                ts_params = {}

                status_class = "fail"

                if test_suite.status == "pass":
                    status_class = "pass"
                elif test_suite.status == "indeterminate":
                    status_class = "indeterminate"
                elif test_suite.status == "info":
                    status_class = "info"
                elif test_suite.status == "warn":
                    status_class = "warn"
                elif test_suite.status == "error":
                    status_class = "err "

                ts_params['name'] = test_suite.name
                ts_params['status'] = status_class
                ts_params['test_cases'] = []

                for test_case in test_suite.test_cases:
                    tc_params = {}

                    tc_status = "fail"

                    if test_case.status == "pass":
                        tc_status = "pass"
                    elif test_case.status == "indeterminate":
                        tc_status = "indt"
                    elif test_case.status == "info":
                        tc_status = "info"
                    elif test_case.status == "warn":
                        tc_status = "warn"
                    elif test_case.status == "error":
                        tc_status = "err "

                    start_time = time.localtime(test_case.start_time)
                    duration = timedelta(seconds=test_case.elapsed_time)
                    end_time = time.localtime(test_case.start_time + test_case.elapsed_time)

                    tc_params['global_id'] = test_case.global_id
                    tc_params['status'] = tc_status
                    tc_params['assignee'] = test_case.assignee
                    tc_params['start_time'] = time.strftime("%H:%M:%S", start_time)
                    tc_params['duration'] = str(duration)
                    tc_params['end_time'] = time.strftime("%H:%M:%S", end_time)
                    tc_params['test_steps'] = []

                    for test_step in test_case.test_steps:
                        step_params = {}
                        step_status = "fail"

                        if test_step.status == "pass":
                            step_status = "pass"
                        elif test_step.status == "indeterminate":
                            step_status = "indeterminate"
                        elif test_step.status == "info":
                            step_status = "info"
                        elif test_step.status == "warn":
                            step_status = "warn"
                        elif test_step.status == "error":
                            step_status = "err "

                        step_params['msg'] = test_step.msg
                        step_params['status'] = step_status
                        step_params['title'] = test_step.title
                        step_params['filename'] = test_step.filename
                        step_params['line'] = test_step.line
                        step_params['cmd'] = test_step.cmd
                        step_params['response'] = test_step.response

                        tc_params['test_steps'].append(step_params)

                    ts_params['test_cases'].append(tc_params)

                params['test_suites'].append(ts_params)

        html_file.write(self.template.generate(**params))

        if self._config.launch_browser:
            webbrowser.open(self._config.filename)


