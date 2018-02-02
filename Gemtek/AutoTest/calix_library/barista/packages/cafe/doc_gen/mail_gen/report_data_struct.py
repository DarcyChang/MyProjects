import cafe
import os

from cafe.util.version import get_version_info


class ReportSummary():



    def __init__(self, dictionary={}):
        #self.report_info = dictionary
        if not dictionary.has_key('report_title'):
            self.report_title = ''
        else:
            self.report_title = dictionary.get('report_title')

        self.release_number = ''
        if not (dictionary.has_key('image_version') and dictionary.has_key('build_number')):
            self.release_number = ''
        elif str(dictionary.get('image_version')).startswith('$') \
                and str(dictionary.get('build_number')).startswith('$') \
                and os.getenv(str(dictionary.get('image_version')).strip('$')) is not None \
                and os.getenv(str(dictionary.get('build_number')).strip('$')) is not None:

            self.release_number = os.getenv(str(dictionary.get('image_version')).strip('$')) + \
                                        '.'+ os.getenv(str(dictionary.get('build_number')).strip('$'))
        else:
            self.release_number = str(dictionary.get('image_version')) + '.' + str(dictionary.get('build_number'))

        if not dictionary.has_key('dut'):
            self.dut = ''
        else:
            self.dut = dictionary.get('dut')

        if not dictionary.has_key('build_id'):
            self.build_id = ''
        elif str(dictionary.get('build_id')).startswith('$') \
                and os.getenv(str(dictionary.get('build_id')).strip('$')) is not None:

            self.build_id = os.getenv(str(dictionary.get('build_id')).strip('$'))
        else:
            self.build_id = dictionary.get('build_id')

        if not dictionary.has_key('branch_id'):
            self.branch_id = ''
        elif str(dictionary.get('branch_id')).startswith('$') \
                and os.getenv(str(dictionary.get('branch_id')).strip('$')):

            self.branch_id = os.getenv(str(dictionary.get('branch_id')).strip('$'))
        else:
            self.branch_id = dictionary.get('branch_id')

        if not dictionary.has_key('result_url'):
            self.result_url = ''
        elif str(dictionary.get('result_url')).startswith('$') \
                and os.getenv(str(dictionary.get('result_url')).strip('$')) is not None:

            self.result_url = os.getenv(str(dictionary.get('result_url')).strip('$'))
        else:
            self.result_url = dictionary.get('result_url')

        if not dictionary.has_key('template_folder'):

            self.template_folder = dictionary.get('cfg_path')+'/templates'
        else:
            if os.path.isabs(dictionary.get('template_folder')):
                self.template_folder = dictionary.get('template_folder')
            else:
                self.template_folder = dictionary.get('cfg_path') + '/' + dictionary.get('template_folder')

        if not dictionary.has_key('template_file'):
            self.template_file = 'Report_Template_v2.htm'
        else:
            self.template_file = dictionary.get('template_file')

        self._get_machine_info()

        self.default_tag = 'UNDEFINED'

        self.result_summary = 'N/A'
        self.test_start_time = 'N/A'
        self.test_stop_time = 'N/A'
        self.test_execution_time = 'N/A'
        self.total_pass_rate = 'N/A'
        self.total_case_number = 'N/A'
        self.case_pass_number = 'N/A'
        self.case_fail_number = 'N/A'
        self.case_skip_number = 'N/A'
        self.case_average_time='N/A'

        # self.execution_ip = ''
        # self.cafe_version = ''
        # self.cafe_release_date =''
        # self.pip_version = {}
        # self.pypm_version = {}
        #
        # self.git_branch = ''
        # self.git_head = ''
        #self.version_info = get_version_info(lib_versions=False)
    def _get_machine_info(self, ip_addr=True, ip_route=True):
        self.local_info={}
        if ip_addr:
            self.local_info['ip'] = str(os.popen('/sbin/ip addr show').read())

        if ip_route:
            self.local_info['router'] = str(os.popen('/sbin/ip route show').read())


class ReportDetailPerCase():
    def __init__(self):
        self.machine_location = ''
        self.case_id = ''
        self.tag = {}
        self.duration = ''
        self.result = ''
        self.last_result = ''
        self.failed_by_ticket = ''


class ReportDetailPerTag():


    def __init__(self,tag='',tag_passed_number='',tag_failed_number='',tag_comments=''):
        self.tag_comments = tag_comments
        self.tag = tag
        self.tag_passed_number = tag_passed_number
        self.tag_failed_number = tag_failed_number
        self.tag_passed_rate = str(round(float(tag_passed_number) /
                                               (float(tag_passed_number) +
                                                float(tag_failed_number))*100,2))+'%'
        self.tag_skipped_number = 'N/A'

        # ret_dict.get(tag).append(self.__dict__)
        # return ret_dict





