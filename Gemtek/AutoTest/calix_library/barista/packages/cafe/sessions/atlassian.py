import json
import os
import re
import urllib

import requests

from cafe.core.logger import CLogger as Logger

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

# const variable define
MAX_RESULT_LIMIT = 2000


class TMSCaseNotExistException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg)

class BambooBuildNotExistException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg)

class TMSCaseStatus:
    PASS = "Pass"
    FAIL = "Fail"
    BLOCK = "Block"
    UNTEST = "Untest"
    NOTEST = "Notest"


class AtlassianAPI:
    # JIRA and TMS
    SEARCH = "search"
    UPDATE = "issue"
    CREATE = ""

    # Bamboo
    PROJECT = "project"
    RESULT = "result"


class RequestType:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"

class BambooBuildState:
    SUCCESS = "Successful"
    FAIL = "Failed"
    UNKNOWN = "Unknown"

class _AtlassianHelper(object):
    def __init__(self, session=requests, base_url=None, api_version="2"):
        """
        Initialize Altassian product login information

        :param session: session used to execute restful request, default is request module
        :param user: Altalassian Product User ID
        :param password: Altalassian Product User Password
        :param data_type: data return type, json or XML
        :param base_url: link to call REST API
        :return: None
        """
        self.session = session
        self.base_url = base_url + "rest/api/%s/" % api_version

    def _update(self, issue_key, url=None, data=None, request_type=RequestType.PUT):
        """
        update issue status by given data
        :param issue_key: issue_key
        :param data: update fields
        :return:
        """
        if not url:
            url_update = self._get_api_url(AtlassianAPI.UPDATE) + "/" + issue_key
        else:
            url_update = url

        status = self._request(url=url_update,
                               data=data,
                               request_type=request_type
                               )
        return True if status else False

    def _create(self):
        pass

    def _get_api_url(self, api_type):
        """
        get REST api_url string

        :param api_type: support type ,eg. search, editMeta and etc., this will defined in enum class AtlassianAPI
        :return: api_url string, eg. http://jira.calix.local/
        """
        return self.base_url + api_type

    def _request(self, url, data=None, request_type=RequestType.POST):
        with AltaAPIRequest(session=self.session,
                            request_type=request_type,
                            url=url,
                            data=data) as f:
            return f.get_data()


class _BaseJIRA(_AtlassianHelper):
    def __init__(self, session, base_url, api_version="2"):
        _AtlassianHelper.__init__(self, session, base_url, api_version)

    def _search(self, jql_str=None, max_results=MAX_RESULT_LIMIT, request_type=RequestType.POST):
        """
        Search content by a jql string

        :param jql_str: the JIRA SQL string used to query test cases;
        :return: search result organized by json, if nothing got return a empty dict
        """
        url_search = self._get_api_url(AtlassianAPI.SEARCH)
        debug(url_search)

        jql_data = {
            "jql": jql_str,
            "maxResults": 1,
            "startAt": 0
        }

        data = self._request(url=url_search, data=jql_data, request_type=request_type)
        if not data:
            return None

        total = data.get('total', None)

        if total > max_results:
            fetched = 0
            result = []
            while fetched < total:
                jql_data.update({'maxResults': max_results, 'startAt': fetched})
                data = self._request(url=url_search, data=jql_data, request_type=request_type)
                result.extend(data['issues'])
                fetched = len(result)
                debug(fetched, total)
            return {'issues': result, 'total': total}
        else:
            jql_data.update({'maxResults': MAX_RESULT_LIMIT})
            return self._request(url=url_search, data=jql_data, request_type=request_type)

    def _get_editmeta(self, issue_key):
        """
        get all field that can be updated for the specific issue-key
        :param issue_key: the unique key that each case assigned, like CAFE-295
        :return: json data or {}
        """
        url_editmeta = self._get_api_url(AtlassianAPI.UPDATE) + "/%s/editmeta" % issue_key
        data = self._request(request_type=RequestType.GET, url=url_editmeta)
        return data

    def _get_case(self, issue_name, issue_key):
        """
        Get case information in a specific project
        :param issue_name: the project Name which case belong, like CAFE
        :param issue_key: the unique key that each case assigned, like CAFE-295
        :return: case information data organized by json,
                 {} if nothing get back
        """

        jql_string = "project = '%s' AND issuekey = '%s'" % (issue_name, issue_key)
        return self._search(jql_string)

    def _get_transition_status(self, issue_key):
        """
        Get a list of the transitions possible for this issue by the current user,
        along with fields that are required and their types.

        Fields will only be returned if expand=transitions.fields.

        The fields in the metadata correspond to the fields in the transition screen for that transition.
        Fields not in the screen will not be in the metadata.

        status_id are dynamic in each state, must get this table to know the status_id if need update status_id

        :param issue_key: TMS issue key
        :return:
        """
        url_get_transition_status_table = self._get_api_url(AtlassianAPI.UPDATE) + "/" + issue_key + "/transitions?transitionId"
        data = self._request(url=url_get_transition_status_table, request_type=RequestType.GET)
        if data:
            data = data["transitions"]
            status_table = {}
            for index, item in enumerate(data):
                status_table[item["name"]] = item["id"]
            return status_table
        else:
            return {}


class JIRAHelper(_BaseJIRA):
    def __init__(self, session, base_url, api_version="2"):
        _BaseJIRA.__init__(self, session, base_url, api_version)


class TMSHelper(_BaseJIRA):
    def __init__(self, session, base_url, api_version="2"):
        _BaseJIRA.__init__(self, session, base_url, api_version)

    def get_regression_case(self, global_id, fix_version, build_tested):
        jql_str = "'Global ID' ~ '%s' and fixVersion ='%s'" % (global_id, fix_version)
        result = self._search(jql_str=jql_str)
        try:
            issue_name = self.session.get(result[u'issues'][0][u'fields'][u'project'][u'self']).json()["name"]
            issue_key = result[u'issues'][0][u'key']
        except (KeyError, IndexError):
            raise TMSCaseNotExistException("can not find specific cases, this case may not created")

        self.update_case_buildtested(issue_key, build_tested)
        return issue_name, issue_key

    def get_failed_jira_link_by_tms_id(self, tms_id):

        jql_str = "'id' = '%s' " % (tms_id)
        result = self._search(jql_str=jql_str)
        jira_link_list = []
        if result:
            self.session.get(result[u'issues'][0][u'fields'][u'project'][u'self']).json()["name"]
            # the issue_link_list which picked from customfield_10902 should have jira ticket with type "originates".
            issue_link_list =result[u'issues'][0][u'fields'][u'customfield_10902'].split(',')
            # print issue_link_list

            for l in issue_link_list:
                jira_link_list.append(re.search('http://jira.calix.local/\S*',l.strip('[').strip(']')).group(0))

            return jira_link_list
        else:
            return ''

    def update_tms_case_by_cdrouter_result(self, result, fix_version, build_tested):
        # result is like:
        #    assignee, result_id, case_detail
        # [u'blwang', '20160408005245', [[150, u'pending', 0, u'cdrouter_firewall_301', u'575020RGCLIGUIfam-800GE-AE'], [151, u'pending', 0, u'cdrouter_firewall_301', u'575020RGCLIGUIfam-800GE-AE'] ]]
        assignee = result[0]
        result_id = result[1]
        case_list = result[2]
        if case_list:
            info("case_ID    case_name    case_status    case_runtime    case GID")
            for case in case_list:
                case_status = case[1]
                case_runtime = case[2]
                case_name = case[3]
                case_gid = case[4]
                info("%s    %s    %s    %s    %s" % (case_gid, case_name, case_runtime, case_name, case_gid))
                try:
                    issue_name, issue_key = self.get_regression_case(case_gid, fix_version, build_tested)
                    # print issue_name, issue_key
                    self.update_case_assignee(issue_key, assignee)
                    self.transit_case_status(issue_name, issue_key, case_status)
                except TMSCaseNotExistException as e:
                    warn("TMS case not exist, skip this case, case name: %s" % (case_name))
                    pass
        return True

    def get_case_status(self, issue_name, issue_key):
        """
        Get TMS case test status, status include [passed, failed, blocked, untested, notest]
        :param issue_name:
        :param issue_key:
        :return:
        """
        data = self._get_case(issue_name, issue_key)
        status = None
        if data:
            status = data[u'issues'][0][u'fields'][u'status'][u'name']
        return status

    def update_case_assignee(self, issue_key, user_id):
        """
        This is to update TMS case assignee, the update process is refer the link below:
        https://developer.atlassian.com/jiradev/jira-apis/jira-rest-apis/jira-rest-api-tutorials/updating-an-issue-via-the-jira-rest-apis

        :param issue_name: TMS issue name
        :param issue_key: TMS issue key
        :param user_id: this should be your calix uesr_id, like xizhang, not mail or full name
        :return: True if update succeed, False if fail to update
        """
        update_data = {
            "update": {
                "assignee": [{"set": {"name": user_id}}],
            }
        }
        return self._update(issue_key, data=update_data)

    def update_case_buildtested(self, issue_key, build_tested):
        update_data = {
            "fields": {"customfield_10103": build_tested},
        }
        return self._update(issue_key, data=update_data)

    def transit_case_status(self, issue_name, issue_key, status):
        """
        This is to transit TMS case status, the update process is refer the link below:
        https://answers.atlassian.com/questions/165210/how-can-you-update-an-issues-workflow-status-through-the-rest-api

        :param issue_name: TMS issue name
        :param issue_key: TMS issue key
        :param status: status to update, status setting please refer enum class TMSCaseStatus
        :return: True if update succeed, False if fail to update
        :exception: raise exception if status not in transit-able list
        """
        current_status = self.get_case_status(issue_name, issue_key)

        transit_status_table = self._get_transition_status(issue_key)

        # if status already the target status return
        if not current_status:
            info("can not get current status")
            return False

        # print current_status, status
        if current_status.__contains__(status):
            return True

        if status not in transit_status_table.keys():
            raise Exception("status(%s) not in transit status table(%s), can not transit to the state" % (status, str(transit_status_table)))

        url_update = self._get_api_url(AtlassianAPI.UPDATE) + "/" + issue_key + "/transitions?expand=transitions.fields"
        update_data = {
            "transition": {
                "id": "%s" % transit_status_table[status]
            },
        }
        return self._update(issue_key=issue_key, url=url_update, data=update_data, request_type=RequestType.POST)

    def create_regression_case(self, creator_name, project, fix_version, JQL, timeout=3):

        url = "http://tools.calix.local/php/tms/tcScheduleDo.php?"
        host = urllib.splithost(urllib.splittype(self.base_url)[1])[0]
        params = {
            "filter": "%s" % JQL,
            "project": "%s" % project,
            "scheltype": "regression",
            "ttype": "regression",
            "hostname": host,
            "version": fix_version,
            "initiator": creator_name,
            "rapidViewId": "No selection yet",
            "sprint": "na",
            "gobackurl": "%sissues/?%s" % (self.base_url, urllib.urlencode({'jql': JQL}))
        }

        url = url + urllib.urlencode(params)

        response = self._request(url, request_type=RequestType.GET, data=timeout * 60)
        if 'Error:' in response.text:
            pattern = "Error:([\s\S]*?)\</div"
            error_str = re.findall(pattern, response.text)[0]
            raise Exception("Error: %s" % error_str)

        return True


class BambooHelper(_AtlassianHelper):
    def __init__(self, session, base_url, api_version="latest"):
        _AtlassianHelper.__init__(self, session, base_url, api_version)

    def _project(self):
        """
        Lists all the projects set up on the Bamboo server.
        :return:
        """
        url_project = self._get_api_url(AtlassianAPI.PROJECT)
        data = self._request(url_project, request_type=RequestType.GET)
        return data

    def get_artifacts(self, project_key, plan_key, build_state=BambooBuildState.SUCCESS):
        url_get_artifact = self._get_api_url(AtlassianAPI.RESULT) + "/%s-%s.json?buildstate=%s" % \
                                                                    (project_key, plan_key, build_state)
        data = self._request(url_get_artifact, request_type=RequestType.GET)
        return data

    def get_latest_valid_artifact(self, project_key, plan_key, build_number="latest", path="", download=True):
        """
        get latest image file in bamboo
        :param project_key: project key like EXAA2267 it is represent the project "EXAA-2267-GFast-Product"
        :param plan_key: like CI and etc.
        :param path: download file path, default is current running folder
        :param download: download the image file to the set path if it is True or just return the image_file name
        :return: status, local file path
        """

        url_get_latest_artifact = self.get_valid_artifact_link(project_key, plan_key, build_number)

        result = self._request(url=url_get_latest_artifact, request_type=RequestType.GET)

        try:
            artifact_link = result["artifacts"]["artifact"][0]["link"]["href"]
        except KeyError:
            raise Exception("link not exists")

        if download:
            with DownloadRequest(session=self.session, url=artifact_link, path=path) as downloadHelper:
                path = downloadHelper.download()
                return True, path, artifact_link
        else:
            return True, "", artifact_link

    def get_valid_artifact_link(self, project_key, plan_key, build_number):
        url_get_latest_artifact = self._get_api_url(AtlassianAPI.RESULT) + "/%s-%s-%s.json?expand=artifacts" % \
                                                                    (project_key, plan_key, build_number)

        return url_get_latest_artifact

    def get_latest_patch_release_run(self, project_key, plan_key, build_number="latest", path="", download=True):
        """
        get lastest patchrelease.run file in bamboo
        :param project_key: project key like EXAA2267 it is represent the project "EXAA-2267-GFast-Product"
        :param plan_key: like CI and etc.
        :param path: download file path, default is current running folder
        :param download: dovnload the iamge file to the set path if it is True or just return the image_file name
        :return: status, local file path
        """

        url_get_latest_artifact = self.get_valid_artifact_link(project_key, plan_key, build_number)

        result = self._request(url=url_get_latest_artifact, request_type=RequestType.GET)

        try:
            artifact_link = result["artifacts"]["artifact"][0]["link"]["href"]
            artifact_link = artifact_link[0:artifact_link.find('/shared/')] + '/BLDDENALI/PatchRelease.run'
            match = re.findall(u"<A HREF=\"([\s\S]*)?\">", self.session.get(artifact_link).text)
            if match:
                artifact_link = artifact_link[0:artifact_link.find('/browse/')] + match[0]
            else:
                raise Exception("can not find patchRelease.run download link")
        except KeyError:
            raise Exception("link not exists")

        if download:
            with DownloadRequest(session=self.session, url=artifact_link, path=path) as downloadHelper:
                path = downloadHelper.download()
                return True, path, artifact_link
        else:
            return True, "", artifact_link

    def get_latest_gc_gh_package(self, project_key, plan_key, tag=None, path="", download=True):
        """
        get lastest patchrelease.run file in bamboo
        :param project_key: project key like EXAA2267 it is represent the project "EXAA-2267-GFast-Product"
        :param plan_key: like CI and etc.
        :param path: download file path, default is current running folder
        :param download: dovnload the iamge file to the set path if it is True or just return the image_file name
        :return: status, local file path
        """
        data = self.get_artifacts(project_key, plan_key, BambooBuildState.SUCCESS)
        artifact_link = None
        if not tag:
            try:
                url_get_latest_artifact = data["results"]["result"][0]["link"]["href"]
                url_get_latest_artifact += ".json?expand=artifacts"
            except KeyError:
                return False, "artifact not exists"

            result = self._request(url=url_get_latest_artifact, request_type=RequestType.GET)

            try:
                for artifact_detail in result["artifacts"]["artifact"]:
                    if artifact_detail['name'] == 'GC-GH-Package':
                        artifact_link = artifact_detail["link"]["href"]
                        break
            except KeyError:
                raise Exception("GC GG Package link not exists in this artifacts")
        else:
            tag = tag.split(",")
            for artifact in data["results"]["result"]:
                try:
                    url_get_latest_artifact = artifact["link"]["href"]
                    url_get_latest_artifact += ".json?expand=artifacts,labels"
                except KeyError:
                    return False, "artifact not exists"

                result = self._request(url=url_get_latest_artifact, request_type=RequestType.GET)

                try:
                    tags = []
                    for item in result['labels']['label']:
                        tags.append(item['name'])
                    # print tags

                    if set(tag).issubset(set(tags)):
                        for artifact_detail in result["artifacts"]["artifact"]:
                            if artifact_detail['name'] == 'GC-GH-Package':
                                artifact_link = artifact_detail["link"]["href"]
                                break

                        if artifact_link:
                            break
                    else:
                        continue
                except KeyError:
                    raise Exception("GC GG Package link not exists in this artifacts")

        if not artifact_link:
            raise Exception("can not find the specific artifact link")
        # print artifact_link
        if download:
            with DownloadRequest(session=self.session, url=artifact_link, path=path) as downloadHelper:
                path = downloadHelper.download()
                return True, path, artifact_link
        else:
            return True, "", artifact_link


class AltaAPIRequest(object):
    def __init__(self, session=requests, request_type=RequestType.POST, url="", data=None, retry=False):
        self.session = session
        self.url = url
        self.data = data
        self.retry = retry
        self.request_type = request_type
        self.response = None
        self.request_dict = {
            RequestType.POST: self.session.post,
            RequestType.GET: self.session.get,
            RequestType.PUT: self.session.put,
        }
        self.request_method = self.request_dict[request_type]

    def get_data(self):
        if self.response:
            try:
                return self.response.json()
            except ValueError:
                return self.response
        return None

    def __enter__(self):
        if self.data:
            self.data = json.dumps(self.data)

        for x in range(3):
            self.response = self.request_method(
                self.url,
                self.data,
            )
            if self.response.status_code not in [200, 204]:
                info("error response code: %d " % self.response.status_code)
                debug(self.response.content)
                if self.response.status_code in [401]:
                    raise Exception("authentication failed, please check your id and password")
                self.response = None

            if not self.retry:
                break

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.response:
            del self.response


class DownloadRequest(object):
    def __init__(self, session=requests, url="", path="\\"):
        self.session = session
        self.url = url
        self.path = path
        self.response = None

    def download(self):
        local_filename = self.url.split('/')[-1]
        local_file_path = os.path.join(self.path, local_filename)
        r = requests.session().get(self.url)
        with open(local_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        return os.path.abspath(local_file_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.response:
            del self.response


if __name__ == '__main__':
    from cafe.sessions.restapi import RestfulSession
    session = RestfulSession(user='soapuser', password="Soapuser")
    # tmsHelper = TMSHelper(session, "http://tms.calix.local/", '2')
    # print tmsHelper.transit_case_status("CAFE", "CAFE-1", "Pass")
    # bambooHelper = BambooHelper(session, "http://bamboo.calix.local/", 'latest')
    # bambooHelper.get_latest_valid_artifact("EXAA2267", "CI0", build_number="2554")
    # bambooHelper.get_latest_patch_release_run("EXAA2267", "CI0", build_number="2708")
