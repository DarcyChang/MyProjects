"""CDROuter session APIs
"""
import requests
import re
import csv
import json

from cafe.core.logger import CLogger as Logger

__author__ = 'xizhang'


_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

status_ok = 200

COLUMN_ROW = ["seq","test_id","iter","scount","status","retries","time","logfile","flag","note","id","name","description"]

# this is to convert CDRouter status to TMS status
STATUS_MAP = {
    'pending': 'Untest',
    'Skip': 'Pass',
    'skip': 'Pass',
    'PASS': 'Pass',
    'FAIL': 'Fail'
}

class CDRouterCaseStatus:
    SKIP = "skip"
    PASS = "PASS"
    PENDING = "pending"
    FAIL = "FAIL"
    FATAL = "FAIL"

class CDRouterRunningStatus:
    SCHEDULED = "scheduled"
    RUNNING = "running"
    FINISHED = "finished"


class CDRouterApiType:
    LAUNCH = "/jobs/launch.txt"
    JOBS = "/jobs/"


class CDRouter(object):
    def __init__(self, session=requests.session(), url=None):
        self.session = session
        self.base_url = url
        pass

    def cdr_run_package(self, package_name, unpause=False):
        url = "%s?name=%s&" % (self.get_api_url(CDRouterApiType.LAUNCH), package_name)
        # to start the test
        response = self.session.post(url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        job_id = self.get_job_id(response.text)
        if unpause:
            self.unpause_test()

        return job_id

    def cdr_get_test_result(self, result_id):
        url = self.base_url + "/results/" + result_id + ".csv"
        response = self.session.get(url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        return response.text

    def cdr_check_status(self, job_id):
        url = "%s%s.json" % (self.get_api_url(CDRouterApiType.JOBS), job_id)
        response = self.session.get(url=url)
        response.raise_for_status()
        result = response.json()
        return result["status"]

    def cdr_get_result_id(self, job_id):
        url = "%s/%s.json" % (self.get_api_url(CDRouterApiType.JOBS), job_id)
        response = self.session.get(url=url)
        response.raise_for_status()
        result = response.json()
        if result["status"] == CDRouterRunningStatus.FINISHED:
            return result["buddyid"]
        else:
            raise Exception("package(job id: %s) still in %s, can not get result ID" % (job_id, result["status"]))

    def cdr_check_if_fail_in_test_package(self, result_id):
        report = self.cdr_parse_test_result(result_id)

        if not CDRouterCaseStatus.FAIL in report.keys():
            return False

        return True

    def cdr_parse_test_result(self, result_id, remove_start_and_final=True):
        result = {}

        raw_test_result = self.cdr_get_test_result(result_id)
        try:
            reader = csv.reader(raw_test_result.splitlines())
        except:
            raise Exception("can not read as CSV format from data")

        index_name = -1
        index_status = -1
        column_length = -1
        for line in reader:
            # ignore the column row, column is like below:
            # ["seq","test_id","iter","scount","status","retries","time","logfile","flag","note","id","name","description"]

            if reader.line_num == 1:
                try:
                    index_status = line.index("status")
                    index_name = line.index("name")
                    column_length = len(line)
                except ValueError:
                    raise Exception("can not find column status and name, not a regular CDRouter result format")
                continue

            if len(line) != column_length:
                raise Exception("length of column is not match the first column, cur row is: %s" % line)

            if line[index_name] in ["start", "final"] and remove_start_and_final:
                continue

            if line[index_status] in result:
                result[line[index_status]].append(line[index_name])
            else:
                result[line[index_status]] = []
                result[line[index_status]].append(line[index_name])
        return result

    def cdr_make_report(self, assignee, result_id, user_interface, EUI, cdrouter_parameters, remove_start_and_final=True):
        if not cdrouter_parameters:
            raise Exception("case tms-GID map data can not be empty")

        report = []
        raw_test_result = self.cdr_get_test_result(result_id)
        try:
            reader = csv.reader(raw_test_result.splitlines())
        except:
            raise Exception("can not read as CSV format from data")

        index_name = -1
        index_test_id = -1
        index_status = -1
        index_time = -1
        column_length = -1
        index_seq = -1
        case = []
        for item in reader:
            # info(item)
            # ignore the column row, column is like below:
            # ["seq","test_id","iter","scount","status","retries","time","logfile","flag","note","id","name","description"]
            if reader.line_num == 1:
                try:
                    index_seq = item.index("seq")
                    index_test_id = item.index("test_id")
                    index_status = item.index("status")
                    index_name = item.index("name")
                    index_time = item.index("time")
                    column_length = len(item)
                except ValueError:
                    raise Exception("can not find column status and name, not a regular CDRouter result format")
                continue

            if len(item) != column_length:
                raise Exception("length of column is not match the first column, cur row is: %s" % item)

            if item[index_name] in ["start", "final"] and remove_start_and_final:
                continue
            try:
                case_name = item[index_name]
                global_id = cdrouter_parameters[case_name]
                global_id_tms = str(global_id) + user_interface + EUI
            except KeyError:
                info("case(%s) can not find tms global ID, skip this test case" % (case_name))
                continue
            if STATUS_MAP[item[index_status]] != STATUS_MAP[CDRouterCaseStatus.FAIL]:
                case.append([item[index_test_id],
                             STATUS_MAP[item[index_status]],
                             item[index_time],
                             case_name,
                             global_id_tms])
            else:
                fail_link = '%s/results/%s/log/%s' % (self.base_url, str(result_id), item[index_seq])
                case.append([item[index_test_id],
                             STATUS_MAP[item[index_status]],
                             item[index_time],
                             case_name,
                             global_id_tms,
                             fail_link])

        report.insert(0, case)
        report.insert(0, result_id)
        report.insert(0, assignee)
        # print report
        return report

    def cdr_push_test_result_to_tms(self, result={}):
        pass

    def cdr_rerun_fail_case_by_package(self, test_package_name, result_id, unpause=False):
        url = self.get_api_url(CDRouterApiType.LAUNCH)

        payload = {
            "skip_tests": "",
            "begin_at": "",
            "name": test_package_name,
            "extra_args": "",
            "tags": "",
            "end_at": "",
            "result_id": result_id,
            "skip_mode": "not-failed",
        }

        # to start the test
        response = requests.post(url, data=payload)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        # response text is like: state=starting:id=8627
        job_id = self.get_job_id(response.text)

        if unpause:
            self.unpause_test()
        return job_id

    def get_job_id(self, response_str):
        pat = "id=([0-9]+)"
        job_id = re.findall(pat, response_str)[0]
        return job_id

    def get_job_state(self, response_str):
        pat = "state=([a-z|A-Z]+)?:"
        state = re.findall(pat, response_str)[0]
        return state

    def unpause_test(self):
        # to unpause the test
        response = self.session.post("%s/live/unpause" % self.base_url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

    def get_api_url(self, api_type):
        url = self.base_url + api_type
        return url

if __name__ == '__main__':
    cdr_helper = CDRouter(url="http://10.245.10.205:8015")
    # print cdr_helper.cdr_get_test_result("20160318060322")
    # cdr_helper.cdr_run_package("TMPL_DHCPScale_XLZ", True)
    # job_id, job_state = cdr_helper.cdr_rerun_fail_case_by_package("TMPL_DHCPScale_XLZ", "20160331205233", True)
    print cdr_helper.cdr_check_status("866455")
    # print job_id, job_state
    # print cdr_helper.cdr_parse_test_result(raw_data)

