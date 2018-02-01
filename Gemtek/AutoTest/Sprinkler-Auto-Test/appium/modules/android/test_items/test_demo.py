# Copyright (C) 2017 Gemtek Technology Co., Ltd.
# Author: Darcy_Chang
# E-mail: darcy_chang@gemteks.com
#
# This python code for Gemtek's project "Sprinkler" that android APP auto test.
# Auto test from welcome frame start, till cloud agent binding finish.
#
# About test case detail, please reference following URL:
# https://docs.google.com/spreadsheets/d/1l_t7J054HMrCXrOheT947wO5HIcxB3oh1Q5w6esRrkQ/edit?pli=1#gid=1268640127


from time import sleep
from appium import webdriver
import android.common_btn
import android.welcome
import android.create_new_account
import android.login
import android.main_screen
import android.wifi_binding
import android.android_btn
import android.dashboard
import android.schedule
import android.sys_info
import android.zone
import android.control_app
import android.gtk_event
import android.verify.click
import android.verify.compare
import android.verify.exist


def sanity_001(self):
    android.control_app.is_app_installed(self)
    android.control_app.remove_app(self)
    android.control_app.install_app(self, "1.65.3")
    android.control_app.launch_app(self)
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")


def sanity_002(self):
#    android.main_screen.my_account(self)
#    android.login.sign_out(self)
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")


def sanity_004(self):
    android.main_screen.my_account(self)
    android.main_screen.user_manual(self)
    android.verify.compare.verify_user_manual(self)
    android.android_btn.android_back(self)


def sanity_009(self):
    android.main_screen.my_account(self)
    android.verify.compare.verify_app_version(self)


def sanity_010(self):
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
#    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB840")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
#    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.wifi_connect_ap(self, "Do", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    try:
        self.driver.find_element_by_id("com.blackloud.wetti:id/rltAb")
        android.main_screen.choose_device(self)
    except:
        pass
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.weather_assistant(self, "ON")
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 1)
    android.schedule.repeat_su(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.main_screen.choose_device(self)
    android.verify.next_page.verify_binging_success(self)


def sanity_016(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.edit_device_name(self, "Gemtek")
    android.sys_info.back(self)
    android.verify.compare.verify_dashboard_title(self, "Gemtek")
    android.dashboard.return2main_screen(self)
    android.verify.compare.verify_device_name(self, "Gemtek")


def sanity_017(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_zip_code(self)
    android.zip_code.enter_zip_code(self, 22201)
    android.zip_code.choose_zip_code(self, 22201)
    android.verify.compare.verify_zip_code(self, 22201)


def sanity_018(self):  # non-sanity_018
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_zone(self)
    android.zone.set_zone_all(self)
    android.zone.set_zone_num(self, 1)
    android.zone.set_zone_num(self, 2)
    android.zone.set_zone_num(self, 3)
    android.zone.set_zone_num(self, 4)
    android.zone.save(self)


def sanity_021(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_fw_version(self, "0.00.81")


def sanity_022(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 1)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 4)
    android.schedule.minute(self, 0)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)


def sanity_023(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 2)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 6)
    android.schedule.minute(self, 0)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.verify.exist.verify_schedule_without_pause(self)


def sanity_034(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 1)
    android.dashboard.manual(self)
    android.manual_watering.launch_watering(self, 1)
    android.verify.exist.verify_watering_zone(self, 1)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)
    android.manual_watering.stop(self)
    android.verify.exist.verify_manual_watering_page(self)


def sanity_036(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.water_multiple_zones(self)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)
    android.manual_watering.skip(self)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)
    android.manual_watering.stop(self)
    android.verify.exist.verify_manual_watering_page(self)


def sanity_039(self):
    android.main_screen.choose_device(self)
    android.dashboard.zone_slide_down2up(self)
    android.dashboard.zone(self, 1)
    android.zone.name_your_zone(self, "darcy")
    android.zone.ok(self)
    android.zone.save(self)
    android.verify.compare.verify_zone_name(self, 1, "darcy")

