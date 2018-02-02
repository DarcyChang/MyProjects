from cafe.sessions.CDRouter import CDRouter
from .proto.base import DriverBase

class CDRouterDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        self.params = self.app.topo_query.connection[self.name]
        self.url = self.params.url
        self.cdrouter = CDRouter(self._session, self.url)

    def cdr_rerun_fail_case_by_package(self, test_package_name, result_id, unpause=False):
        return self.cdrouter.cdr_rerun_fail_case_by_package(test_package_name, result_id, unpause)

    def cdr_run_package(self, package_name, unpause=False):
        return self.cdrouter.cdr_run_package(package_name, unpause)

    def cdr_get_test_result(self, package_id):
        return self.cdrouter.cdr_get_test_result(package_id)

    def cdr_check_status(self, job_id):
        return self.cdrouter.cdr_check_status(job_id)

    def cdr_check_if_fail_in_test_package(self, result_id):
        return self.cdrouter.cdr_check_if_fail_in_test_package(result_id)

    def cdr_get_result_id(self, job_id):
        return self.cdrouter.cdr_get_result_id(job_id)

    def cdr_make_report(self, assignee, result_id, user_interface, EUT, cdrouter_parameters, remove_start_and_final=True):
        return self.cdrouter.cdr_make_report(assignee, result_id, user_interface, EUT, cdrouter_parameters, remove_start_and_final)