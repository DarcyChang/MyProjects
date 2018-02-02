import cafe
from cafe.sessions.atlassian import *
from .proto.base import DriverBase

class JiraDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        self.params = self.app.topo_query.connection[self.name]
        self.url = self.params.url
        self.api_version = self.params.api_version
        self.jira_helper = JIRAHelper(self._session, self.url, self.api_version)


class TMSDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        self.params = self.app.topo_query.connection[self.name]
        self.url = self.params.url
        self.api_version = self.params.api_version
        self.tms_helper = TMSHelper(self._session, self.url, self.api_version)

    def update_tms_case_by_cdrouter_result(self, result, fix_version, build_tested):
        return self.tms_helper.update_tms_case_by_cdrouter_result(result, fix_version, build_tested)

    def get_regression_case(self, global_id, fix_version, build_tested):
        return self.tms_helper.get_regression_case(global_id, fix_version, build_tested)

    def get_failed_jira_link_by_tms_id(self, global_id):
        return self.tms_helper.get_failed_jira_link_by_tms_id(global_id)

    def get_case_status(self, issue_name, issue_key):
        return self.tms_helper.get_case_status(issue_name, issue_key)

    def update_case_assignee(self, issue_key, user_id):
        return self.tms_helper.update_case_assignee(issue_key, user_id)

    def transit_case_status(self, issue_name, issue_key, status):
        return self.tms_helper.transit_case_status(issue_name, issue_key, status)

    def create_regression_case(self, creator_name, project, fix_version, JQL, timeout=3):
        return self.tms_helper.create_regression_case(creator_name, project, fix_version, JQL, timeout)

    def update_case_buildtested(self, issue_key, build_tested):
        return self.tms_helper.update_case_buildtested(issue_key, build_tested)


class BambooDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        self.params = self.app.topo_query.connection[self.name]
        self.url = self.params.url
        self.api_version = self.params.api_version
        self.bamboo_helper = BambooHelper(self._session, self.url, self.api_version)

    def get_latest_valid_artifact(self, project_key, plan_key, build_number="latest", path="", download=True):
        return self.bamboo_helper.get_latest_valid_artifact(project_key, plan_key, build_number, path, download)

    def get_latest_patch_release_run(self, project_key, plan_key, build_number="latest", path="", download=True):
        return self.bamboo_helper.get_latest_patch_release_run(project_key, plan_key, build_number, path, download)

    def get_latest_gc_gh_package(self, project_key, plan_key, tag=None, path="", download=True):
        return self.bamboo_helper.get_latest_gc_gh_package(project_key, plan_key, tag, path, download)
