"""ccplus session APIs

Methods:
    ccplusHelper.create_device_group():
    ccplusHelper.delete_device_group():
"""

__author__ = 'xizhang'

import json
import uuid
import urllib
import requests
import os
import datetime
import time

from cafe.core.logger import CLogger as Logger

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info

status_ok = 200

SOFTWARE_IMAGE_INFO = "Robot Framework Test Software Image"
CONFIG_FILE_INFO = "Robot Framework Test Config File"
DEVICE_GROUP_INFO = "Robot Framework Test Device Group"
WORKFLOW_INFO = "Robot Framework Test Workflow"


class CCPlusApiType:
    GROUP = "/cc/group"
    FILE = "/cc/file"
    WORKFLOW = "/cc/workflow"
    DEVICE = "/cc/device"
    DEVICE_OP = "/cc/device-op"
    SUBSCRIBER = "/cc/subscriber"
    EVENT = "/cc/event"
    CWMP = "/cc/device-cwmp-logs"


class CCPlusFileType:
    IMAGE_FILE = "SW/FW Image"
    CONFIG_FILE = "Configuration File"
    LOG_FILE = "Log File"
    SIP_CONFIG_FILE = "SIP Configuration File"


class WorkFlowState:
    SCHEDULED = "scheduled"
    ABORTED = "aborted"
    INPROGRESS = "In Progress"
    COMLETED = "Completed"
    SUSPEND = "Suspended"


class WorkFlowType:
    ON_DISCOVERY = {
        "initialTrigger": {
                        "type": "CPE Event",
                        "cpeEvent": "CC EVENT - New CPE Discovered"
                    },
    }

    TIME_WINDOW = {
        "initialTrigger": {
                        "type": "Maintenance Window"
                    },
    }


class CCPlusHelper(object):
    def __init__(self, session=requests, url=None, org_id="51"):
        self.session = session
        self.base_url = url
        self.org_id = org_id

    def __delete_object(self, api_type, **kwargs):
        url = self.get_url(api_type)
        # print url
        _id = self.__get_id(url, **kwargs)
        params = {
            "orgId": self.org_id,
            "_id": _id,
        }
        url = url + "?" + urllib.urlencode(params)
        response = self.session.delete(url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text + " obj %s can not be deleted" % kwargs)
        return True

    def __get_id(self, url, **kwargs):
        # query group information by name, this is to get the _id information, it is used to delete
        # the group name

        url += "?%s" % urllib.urlencode(kwargs)

        group_data = self.session.get(url).json()
        if not group_data:
            raise Exception("the specify name '%s' not exists" % kwargs['name'])
        # print group_data
        if isinstance(group_data, dict):
            return group_data['_id']
        return group_data[0]['_id']

    def __get_upload_url(self, name, type):
        url = self.get_url(CCPlusApiType.FILE)
        url += "?%s" % urllib.urlencode({"name": name, "type": type, "orgId": self.org_id})

        # print url
        group_data = self.session.get(url).json()
        if not group_data:
            raise Exception("the specify url '%s' not exists" % url)
        return group_data[0]['uploadUrl']

    def __get_device_information(self, url, serial_number):
        url += "?%s" % urllib.urlencode({"serialNumber": serial_number})

        group_data = self.session.get(url).json()
        if not group_data:
            raise Exception("the specify serialNumber '%s' not exists" % name)
        return group_data

    def get_url(self, api_type):
        return self.base_url + api_type

    def __create_device_group(self, device_group_name, type="dynamic", **kwargs):
        name = device_group_name
        group_params = {
            "orgId": self.org_id,
            "name": device_group_name,
            "description": DEVICE_GROUP_INFO,
            "type": type,
            "cpeFilter": kwargs,
        }

        url = self.get_url(CCPlusApiType.GROUP)
        data = json.dumps(group_params)
        response = self.session.post(url=url, data=data)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        return name

    def create_device_group_by_sn(self, serial_number, device_group_name=None):
        name = "test_" + str(uuid.uuid1())
        if device_group_name:
            name = device_group_name
        return self.__create_device_group(device_group_name=name, type="dynamic", serialNumber=serial_number)

    def delete_device_group(self, name):
        return self.__delete_object(CCPlusApiType.GROUP, name=name)

    def delete_all_test_device_group(self):
        url = self.get_url(CCPlusApiType.GROUP)
        response = self.session.get(url=url)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        data = response.json()

        if not data:
            return
        else:
            id_array = []
            for group_item in data:
                if group_item["description"] == DEVICE_GROUP_INFO and\
                        group_item["name"].startswith("test_"):
                    id_array.append(group_item["name"])

            if id_array:
                for name in id_array:
                    self.__delete_object(CCPlusApiType.GROUP, name=name)

        return True

    def delete_all_test_upload_file(self):
        url = self.get_url(CCPlusApiType.FILE)
        response = self.session.get(url=url)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        data = response.json()

        if not data:
            return
        else:
            id_array = []
            for group_item in data:
                if group_item["description"] in[SOFTWARE_IMAGE_INFO, CONFIG_FILE_INFO]:
                    id_array.append(group_item["name"])

            if id_array:
                for name in id_array:
                    self.__delete_object(CCPlusApiType.FILE, name=name)
        return True

    def delete_all_test_workflow(self):
        url = self.get_url(CCPlusApiType.WORKFLOW)
        response = self.session.get(url=url)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        data = response.json()

        if not data:
            return
        else:
            id_array = []
            for group_item in data:
                if group_item["description"] in[WORKFLOW_INFO]:
                    id_array.append(group_item["name"])

            if id_array:
                for name in id_array:
                    self.delete_work_flow(name)
        return True

    def upload_sw_fw_image(self, path, upload_host=None, software_image_name=None):
        return self.__upload_file(path, upload_host, software_image_name, CCPlusFileType.IMAGE_FILE, SOFTWARE_IMAGE_INFO)

    def upload_config_file(self, path, upload_host=None, config_file_name=None):
        return self.__upload_file(path, upload_host, config_file_name, CCPlusFileType.CONFIG_FILE, CONFIG_FILE_INFO)

    def __upload_file(self, path, upload_host=None, file_name=None, file_type=None, file_description=None):

        # # To upload an file, the API client must send an HTTP POST request
        # to the designated URL path "/cc/file" with a valid "SW/FW Image Info" structure
        # as the request payload, then the API server will return an URL path for the actual upload.
        # The client will then upload the image to the returned URL path via HTTP POST.

        # get upload url
        url = self.get_url(CCPlusApiType.FILE)
        # print url
        name = path.split(os.sep)[-1]

        if not os.path.isfile(path):
            raise Exception("file path %s not exist, please check" % path)

        if file_name:
            name = file_name

        file_params = {
            "orgId": self.org_id,
            "name": name,
            "type": file_type,
            "description": file_description,
            "manufacturer": "Calix",
        }

        data = json.dumps(file_params)
        response = self.session.post(url, data=data)
        # print data
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        upload_params = response.json()
        # print upload_params

        # upload the image to the returned URL path via HTTP POST.
        try:
            upload_url = upload_params['uploadUrl']
        except:
            print "can not get upload url from response, try get url from RESTful API"
            upload_url = self.__get_upload_url(name, CCPlusFileType.CONFIG_FILE)
            # print upload_url

        # return

        if upload_host:
            upload_url = 'http://%s:8080/files/%s' % (upload_host, upload_params['_id'])

        path = os.path.abspath(path)
        with open(path, 'rb') as upload_file:
            response = requests.post(upload_url, data=upload_file,
                                         headers={'Content-Type': 'application/octet-stream'},
                                         auth=(upload_params['username'], upload_params['password']))

            if response.status_code != status_ok:
                raise Exception(response.status_code, response.text)

        return name

    def delete_sw_fw_image(self, name):
        return self.__delete_object(CCPlusApiType.FILE, name=name)

    def delete_config_file(self, name):
        return self.__delete_object(CCPlusApiType.FILE, name=name)

    def create_download_image_work_flow_on_discovery(self, group_name, image_name, work_flow_name=None):
        return self.__create_download_work_flow_on_discovery(group_name,image_name,work_flow_name,"Download SW/FW Image")

    def create_download_config_work_flow_on_discovery(self, group_name, config_file, work_flow_name=None):
        return self.__create_download_work_flow_on_discovery(group_name, config_file, work_flow_name, "Download Configuration File")

    def __create_download_work_flow_on_discovery(self, group_name, file_name, work_flow_name=None, file_type=None):
        name = "RF_Test_Flow_" + str(uuid.uuid1())
        if work_flow_name:
            name = work_flow_name
        # get image/group id
        file_id = self.__get_id(self.get_url(CCPlusApiType.FILE), name=file_name)
        group_id = self.__get_id(self.get_url(CCPlusApiType.GROUP), name=group_name)

        url = self.get_url(CCPlusApiType.WORKFLOW)
        workflow_params = {
            "orgId": self.org_id,
            "name": name,
            "description": WORKFLOW_INFO,
            "execPolicy": {
                "initialTrigger":
                    {
                        "type": "CPE Event",
                        "cpeEvent": "CC EVENT - New CPE Discovered"
                    },
            },
            "groups": [group_id],
            "actions": [
                {
                    "actionType": file_type,
                    "fileId": file_id,  # only if action type is "Download Xxx"
                },
            ]
        }

        data = json.dumps(workflow_params)

        response = self.session.post(url=url, data=data)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        return name

    def create_download_image_work_flow_on_time_window(self, group_name, image_name, time_window, work_flow_name=None):
        return self.__create_download_work_flow_on_time_window(group_name,image_name,time_window,work_flow_name, "Download SW/FW Image")

    def create_download_config_work_flow_on_time_window(self, group_name, config_name, time_window, work_flow_name=None):
        return self.__create_download_work_flow_on_time_window(group_name, config_name, time_window, work_flow_name, "Download Configuration File")

    def __create_download_work_flow_on_time_window(self, group_name, file_name, time_window, work_flow_name=None, download_type=None):
        name = "RF_Test_Flow_" + str(uuid.uuid1())
        if work_flow_name:
            name = work_flow_name

        # get image/group id
        file_id = self.__get_id(self.get_url(CCPlusApiType.FILE), name=file_name)
        group_id = self.__get_id(self.get_url(CCPlusApiType.GROUP), name=group_name)

        url = self.get_url(CCPlusApiType.WORKFLOW)

        workflow_params = {
            "orgId": self.org_id,
            "name": name,
            "description": WORKFLOW_INFO,
            "execPolicy": {
                "window": {
                    "startDateTime": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "windowLength": int(time_window) * 60,
                },
                "initialTrigger":
                    {
                        "type": "Maintenance Window"
                    },
            },
            "groups": [group_id],
            "actions": [
                {
                    "actionType": download_type,
                    "fileId": file_id,  # only if action type is "Download Xxx"
                },
            ]
        }

        data = json.dumps(workflow_params)
        response = self.session.post(url=url, data=data)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        return name

    def get_work_flow_state(self, name):
        url = self.get_url(CCPlusApiType.WORKFLOW) + "?%s" % urllib.urlencode({"name": name})
        group_data = self.session.get(url).json()
        if not group_data:
            raise Exception("the specify name '%s' not exists" % name)
        return group_data[0]['state']
        pass

    def suspend_work_flow(self, name):
        id = self.__get_id(self.get_url(CCPlusApiType.WORKFLOW), name=name)
        url = self.get_url(CCPlusApiType.WORKFLOW) + "/" + id + "/suspend"
        response = self.session.put(url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        return True

    def resume_work_flow(self, name):
        id = self.__get_id(self.get_url(CCPlusApiType.WORKFLOW), name=name)
        url = self.get_url(CCPlusApiType.WORKFLOW) + "/" + id + "/resume"
        response = self.session.put(url)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        return True

    def delete_work_flow(self, name):
        return self.__delete_object(CCPlusApiType.WORKFLOW, name=name)

    def wait_until_work_flow_to_state(self, name, state, timeout=1, interval=10):
        """

        Args:
            name:
            state:
            timeout: timeout to failure, unit is minutes

        Returns:

        """
        starttime = datetime.datetime.now()
        while self.get_work_flow_state(name) != state:
            endtime = datetime.datetime.now()
            gap = endtime - starttime
            if gap.seconds > float(timeout) * 60:
                raise Exception("timeout occurred, workflow still not get to state %s" % state)
            else:
                # print "Sleep %d seconds then check again" % interval
                time.sleep(float(interval))
                continue
        return True

    def get_arg_value(self, raw_data, arg):
        value = raw_data.copy()

        arg_array = arg.split(".")

        for sub_arg in arg_array:
            value = value[sub_arg]

        return value

    def get_parameters_value(self, serial_number, *args):
        result = {}

        args_name_array = []

        for arg in args:
            if isinstance(arg, list):
                args_name_array.extend(arg)
            else:
                args_name_array.append(arg)

        query_params = {
            "orgId": self.org_id,
            "operation": "GetParameterValues",
            "cpeIdentifier": {
                "serialNumber": serial_number,
            },

            "getOptions": {
                "liveData": True
            },
            "parameterNames": args_name_array,
        }

        data = json.dumps(query_params)
        url = self.get_url(CCPlusApiType.DEVICE_OP)
        response = self.session.post(url=url, data=data)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        raw_result = response.json()

        for arg in args_name_array:
            result[arg] = self.get_arg_value(raw_result, arg)

        return result

    def update_parameters(self, para_dict, update_dict={}):
        for key, value in update_dict.items():
            if key in para_dict:
                para_dict[key] = self.update_parameters(para_dict[key], update_dict[key])
            else:
                para_dict.update(update_dict)
        return para_dict

    def parse_parameters(self, params):
        para_dict = None

        for param_name, param_value in params.items():
            params = param_value

            params_array = param_name.split(".")
            params_array.reverse()

            for param in params_array:
                params = {param: params}

            if para_dict:
                para_dict = self.update_parameters(para_dict, params)
            else:
                para_dict = params

        return para_dict

    def set_parameters_value(self, serial_number, param_dict):
        query_params = {
            "orgId": self.org_id,
            "operation": "SetParameterValues",
            "cpeIdentifier": {
                "serialNumber": serial_number,
            },
            "parameterValues": self.parse_parameters(param_dict)
        }

        data = json.dumps(query_params)
        url = self.get_url(CCPlusApiType.DEVICE_OP)
        response = self.session.post(url=url, data=data)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        return True

    def delete_device(self, serial_number):
        return self.__delete_object(CCPlusApiType.DEVICE, serialNumber=serial_number)

    def add_object_on_device(self, serial_number, object_path=""):
        query_params = {
            "orgId": self.org_id,
            "operation": "AddObject",
            "cpeIdentifier": {
                "serialNumber": serial_number,
            },
            "objectName": object_path
        }

        data = json.dumps(query_params)
        url = self.get_url(CCPlusApiType.DEVICE_OP)
        response = self.session.post(url=url, data=data)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        if object_path[-1] == '.':
            return object_path + str(response.json()["newObjectIndex"])
        else:
            return object_path + "." + str(response.json()["newObjectIndex"])

    def delete_object_on_device(self, serial_number, object_path):
        query_params = {
            "orgId": self.org_id,
            "operation": "DeleteObject",
            "cpeIdentifier": {
                "serialNumber": serial_number,
            },
            "objectName": object_path
        }

        data = json.dumps(query_params)
        url = self.get_url(CCPlusApiType.DEVICE_OP)
        response = self.session.post(url=url, data=data)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)
        print response.text
        return True

    def get_event_log_on_device(self, serial_number):
        query_params = {
            "orgId": self.org_id,
            "deviceSn": serial_number
        }
        url = self.get_url(CCPlusApiType.EVENT) + "?%s" % urllib.urlencode(query_params)
        print url
        response = self.session.get(url)

        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        return response.json()

    def get_cwmp_log_on_device(self, serial_number, include_xml_text=False):
        query_params = {
            "orgId": self.org_id,
            "cpeIdentifier": {
                "serialNumber": serial_number,
            },
            "includeXmlText": include_xml_text
        }
        data = json.dumps(query_params)
        url = self.get_url(CCPlusApiType.CWMP)
        response = self.session.get(url=url, data=data)
        if response.status_code != status_ok:
            raise Exception(response.status_code, response.text)

        return response.json()


if __name__ == '__main__':
    ccpHelper = CCPlusHelper(url="http://10.245.250.98:8081")
    # ccpHelper.delete_all_test_workflow()
    # try:
    #     ccpHelper.delete_all_test_device_group()
    #     ccpHelper.delete_all_test_upload_file()
    # except:
    #     pass
    # group_name = ccpHelper.create_device_group_by_sn("CXNK001D8F8B")
    # print group_name
    # image_name = ccpHelper.upload_sw_fw_image("/home/xizhang/1.1.6.1.oneimage", upload_host="10.245.250.98", software_image_name="test_soft_ware_image.oneimage")
    # print image_name
    # ccpHelper.get_event_log_on_device("CXNK00205294")
    print ccpHelper.get_cwmp_log_on_device("CXNK00205294")
    # print config_name
    # work_flow_name = ccpHelper.create_download_image_work_flow_on_discovery(group_name, image_name)
    # work_flow_name = ccpHelper.create_download_image_work_flow_on_time_window(group_name, image_name, 10)
    # print group_name, image_name, work_flow_name
    # work_flow_name = "RF_test_flow_b0561d54-dab1-11e5-8e1a-0050569e5074"
    # ccpHelper.suspend_work_flow(work_flow_name)
    # ccpHelper.resume_work_flow(work_flow_name)
    # print ccpHelper.wait_until_work_flow_to_state(work_flow_name, workflowState.COMLETED, timeout=0.5)
    # print ccpHelper.get_valid_operation(serial_number="CXNK001D8E1B")

    # 1. by list, return dictionary, in one request
    # 2. return {name: value}

    # print ccpHelper.get_parameters_value("CXNK001D8F8B", ["InternetGatewayDevice.UserInterface.RemoteAccess.Enable"], "InternetGatewayDevice.DeviceInfo.UpTime")
    #
    # # 1.By dictionary, in one request, in one request
    # param_dict = {"InternetGatewayDevice.UserInterface.RemoteAccess.Enable": "false",
    #               "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.AutoChannelEnable": "false"}
    # # print ccpHelper.parse_parameters(param_dict)
    # print ccpHelper.set_parameters_value("CXNK001D8F8B", param_dict)
    #
    # print ccpHelper.add_object_on_device("CXNK001D8F7A", "InternetGatewayDevice.WANDevice.3.WANConnectionDevice.1.WANIPConnection.")
    # print ccpHelper.get_parameters_value("CXNK001D8F7A", ["InternetGatewayDevice.WANDevice.3.WANConnectionDevice.1.WANIPConnection"])
    #                                                       "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.AutoChannelEnable"])
    # print ccpHelper.delete_object_on_device("CXNK001D8F7A", "InternetGatewayDevice.WANDevice.3.WANConnectionDevice.1.WANIPConnection.27.")
    # print ccpHelper.delete_object_on_device("CXNK001D8F7A", "InternetGatewayDevice.WANDevice.3.WANConnectionDevice.1.WANIPConnection.26.")
    # print ccpHelper.delete_object_on_device("CXNK001D8F7A", "InternetGatewayDevice.WANDevice.3.WANConnectionDevice.1.WANIPConnection.25.")

    #
    # print ccpHelper.get_parameters_value("CXNK001D8F8B", ["InternetGatewayDevice.UserInterface.RemoteAccess.Enable",
    #                                                       "InternetGatewayDevice.LANDevice.1.WLANConfiguration.1.AutoChannelEnable"])
    #
    # ccpHelper.delete_all_test_device_group()
    # ccpHelper.delete_all_test_software_image()
    # ccpHelper.wait_until_work_flow_to_state("CXNK1C497B27D896_20160226133632", workflowState.INPROGRESS, 0.5)
    # ccpHelper.wait_until_work_flow_to_state("CXNK1C497B27D896_20160308104620", WorkFlowState.INPROGRESS, "0.5", "5")
    # config_name = ccpHelper.upload_config_file("/home/xizhang/1.1.6.config.conf", upload_host="10.245.250.98")
    # ccpHelper.delete_config_file(config_name)
    # print config_name, group_name
    # ccpHelper.create_download_config_work_flow_on_time_window("test_8caf0058-e986-11e5-93d7-0050569e5074", "1.1.6.config.conf", "10")
    # ccpHelper.create_download_config_work_flow_on_discovery(group_name, config_name)
    # ccpHelper.create_download_image_work_flow_on_time_window(group_name, config_name, 10)


    # ccpHelper.delete_device("CXNK001D8E7E")
    # ccpHelper.delete_sw_fw_image("Pre801F_1.1.9.1.oneimage")
    pass






