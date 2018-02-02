from cafe.sessions.ccplus import CCPlusHelper
from .proto.base import DriverBase

class CCPlusDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app
        self.params = self.app.topo_query.connection[self.name]
        self.url = self.params.url
        self.org_id = str(self.params.org_id)
        self.ccphelper = CCPlusHelper(self._session, self.url, self.org_id)

    def create_device_group_by_sn(self, serial_number, device_group_name=None):
        return self.ccphelper.create_device_group_by_sn(serial_number, device_group_name)

    def delete_device_group(self, name):
        return self.ccphelper.delete_device_group(name)

    def upload_sw_fw_image(self, path, upload_host=None, image_name=None):
        return self.ccphelper.upload_sw_fw_image(path, upload_host, image_name)

    def delete_sw_fw_image(self, name):
        return self.ccphelper.delete_sw_fw_image(name)

    def upload_config_file(self, path, upload_host=None, config_name=None):
        return self.ccphelper.upload_config_file(path, upload_host, config_name)

    def delete_config_file(self, name):
        return self.ccphelper.delete_config_file(name)

    def create_download_config_work_flow_on_discovery(self, group_name, config_name, work_flow_name=None):
        return self.ccphelper.create_download_config_work_flow_on_discovery(group_name, config_name, work_flow_name)

    def create_download_config_work_flow_on_time_window(self, group_name, config_name, time_window, work_flow_name=None):
        return self.ccphelper.create_download_config_work_flow_on_time_window(group_name, config_name, time_window, work_flow_name)

    def create_download_image_work_flow_on_discovery(self, group_name, image_name, work_flow_name=None):
        return self.ccphelper.create_download_image_work_flow_on_discovery(group_name, image_name, work_flow_name)

    def create_download_image_work_flow_on_time_window(self, group_name, image_name, time_window, work_flow_name=None):
        return self.ccphelper.create_download_image_work_flow_on_time_window(group_name, image_name, time_window, work_flow_name)

    def get_work_flow_state(self, work_flow_name):
        return self.ccphelper.get_work_flow_state(work_flow_name)

    def suspend_work_flow(self, work_flow_name):
        return self.ccphelper.suspend_work_flow(work_flow_name)

    def resume_work_flow(self, work_flow_name):
        return self.ccphelper.resume_work_flow(work_flow_name)

    def delete_work_flow(self, work_flow_name):
        return self.ccphelper.delete_work_flow(work_flow_name)

    def wait_until_work_flow_to_state(self, work_flow_name, state, timeout=60, interval=10):
        return self.ccphelper.wait_until_work_flow_to_state(work_flow_name, state, timeout, interval)

    def set_parameters_value(self, serial_number, param_dict):
        return self.ccphelper.set_parameters_value(serial_number, param_dict)

    def get_parameters_value(self, serial_number, *args):
        return self.ccphelper.get_parameters_value(serial_number, *args)

    def delete_all_test_device_group(self):
        return self.ccphelper.delete_all_test_device_group()

    def delete_all_test_upload_file(self):
        return self.ccphelper.delete_all_test_upload_file()

    def delete_device(self, serial_number):
        return self.ccphelper.delete_device(serial_number)

    def delete_all_test_workflow(self):
        return self.ccphelper.delete_all_test_workflow()

    def add_object_on_device(self, serial_number, object_path):
        return self.ccphelper.add_object_on_device(serial_number, object_path)

    def delete_object_on_device(self, serial_number, object_path):
        return self.ccphelper.delete_object_on_device(serial_number, object_path)

    def get_event_log_on_device(self, serial_number):
        return self.ccphelper.get_event_log_on_device(serial_number)

    def get_cwmp_log_on_device(self, serial_number, include_xml_text=False):
        return self.ccphelper.get_cwmp_log_on_device(serial_number, include_xml_text)