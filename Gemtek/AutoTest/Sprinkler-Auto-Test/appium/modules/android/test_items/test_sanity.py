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
import android.verify.next_page


def sanity_001(self):
    android.control_app.is_app_installed(self)
    android.control_app.remove_app(self)
    android.control_app.install_app(self, "1.65.3")
    android.control_app.launch_app(self)
    android.welcome.slide_welcome_frame(self)
    android.control_app.close_app(self)


def sanity_002(self):
    android.login.sign_in(self, "jerry.sqa5", "55555555")
    android.main_screen.my_account(self)
    android.login.sign_out(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")


def sanity_003(self):
    android.main_screen.my_account(self)
    android.main_screen.buy_blackloud_sprinkler(self)
    android.verify.compare.verify_buy_blackloud_sprinkler(self)
    android.android_btn.android_back(self)


def sanity_004(self):
    android.main_screen.my_account(self)
    android.main_screen.user_manual(self)
    android.verify.compare.verify_user_manual(self)
    android.android_btn.android_back(self)


def sanity_005(self):
    android.main_screen.my_account(self)
    android.main_screen.feature_introduction(self)
    android.welcome.slide_welcome_frame(self)


def sanity_006(self):
    android.main_screen.my_account(self)
    android.main_screen.contact_us(self)
    android.verify.compare.verify_contact_us(self)
    android.android_btn.android_back(self)


def sanity_007(self):
    android.main_screen.my_account(self)
    android.main_screen.about_blackloud(self)
    android.verify.compare.verify_about_blackloud(self)
    android.android_btn.android_back(self)


def sanity_008(self):
    android.main_screen.my_account(self)
    android.main_screen.legal_and_privacy_policy(self)
    android.verify.compare.verify_legal_and_privacy_policy(self)
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
        sleep(3)
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


def sanity_011(self):
    android.gtk_event.wait_any_key("\n[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.gtk_event.wait_any_key("\n[Gemtek] Please connect ethernet to device and enter any key.\n")
    android.wifi_binding.wired_setup(self)
    android.wifi_binding.no_flashing_red_light(self)
    android.wifi_binding.next_wired(self)
    android.gtk_event.wait_any_key("\n[Gemtek] Wait, if device wifi blue LED light, please enter any key.\n")
    android.wifi_binding.next_to_continue_setting(self)
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
    

def sanity_012(self):
    android.main_screen.add_device(self)
    android.wifi_binding.direct_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
#    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB840")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 1)
    android.schedule.repeat_su(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.common_btn.left_on_top_bar(self)
    android.main_screen.choose_device(self)
    android.verify.next_page.verify_binging_success_without_network(self)


def sanity_013(self):
#    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB840")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_home(self)
    android.control_app.launch_app(self)
    android.wifi_binding.cloud_control(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
#    android.wifi_binding.wifi_connect_ap(self, "Do", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
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


def sanity_014(self):
    android.gtk_event.wait_any_key("\n[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_home(self)
    android.control_app.launch_app(self)
    android.wifi_binding.cloud_control(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.gtk_event.wait_any_key("\n[Gemtek] Please connect ethernet to device and enter any key.\n")
    android.wifi_binding.wired_setup(self)
    android.wifi_binding.no_flashing_red_light(self)
    android.wifi_binding.next_wired(self)
    android.gtk_event.wait_any_key("\n[Gemtek] Wait, if device wifi blue LED light, please enter any key.")
    android.wifi_binding.next_to_continue_setting(self)
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


def sanity_015(self):
#    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB840")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_home(self)
    android.control_app.launch_app(self)
    android.wifi_binding.direct_control(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
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
    android.verify.next_page.verify_binging_success_without_network(self)
    

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


def sanity_018(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_zone(self)
    android.zone.set_zone_num(self, 5)
    android.zone.set_zone_num(self, 6)
    android.zone.save(self)
    # TODO verify it in dashboard


def sanity_019(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_system_date_and_time(self)


def sanity_020(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_wifi(self)
    android.sys_info.yes(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
#    android.wifi_binding.wifi_connect_ap(self, "Do", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_wifi_ssid(self, "BKwifi_Darcy_2.4G")
#    android.verify.compare.verify_wifi_ssid(self, "Do")


def sanity_021(self):
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_fw_version(self, "0.00.82")


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
    android.schedule.hour(self, 8)
    android.schedule.minute(self, 0)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)


def sanity_024(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 3)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 9)
    android.schedule.minute(self, 59)
    android.schedule.time_system(self, "PM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)


def sanity_025(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 3)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)


def sanity_026(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 2)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)


def sanity_027(self):
    android.main_screen.choose_device(self)
    android.dashboard.schedule(self, 1)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)


def sanity_028(self):
    android.main_screen.choose_device(self)
    android.dashboard.auto_watering(self, "On")
    android.verify.compare.verify_auto_watering_status(self, "On")
    android.dashboard.return2main_screen(self)


def sanity_029(self):
    android.main_screen.choose_device(self)
    android.dashboard.auto_watering(self, "OFF")
    android.verify.compare.verify_auto_watering_status(self, "OFF")
    android.dashboard.return2main_screen(self)
    android.verify.exist.verify_device_auto_watering(self, "OFF")


def sanity_030(self):
    android.main_screen.choose_device(self)
    android.dashboard.weather_assistant(self, "ON")
    android.verify.compare.verify_weather_assistant_status(self, "ON")
    android.dashboard.return2main_screen(self)


def sanity_031(self):
    android.main_screen.choose_device(self)
    android.dashboard.weather_assistant(self, "OFF")
    android.verify.compare.verify_weather_assistant_status(self, "OFF")
    android.dashboard.return2main_screen(self)


def sanity_034(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.launch_watering(self, 1)
    android.verify.exist.verify_watering_zone(self, 1)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)


def sanity_035(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.launch_watering(self, 1)
    android.manual_watering.stop(self)
    android.verify.exist.verify_manual_watering_page(self)


def sanity_036(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.water_multiple_zones(self)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)


def sanity_037(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.water_multiple_zones(self)
    android.manual_watering.skip(self)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)


def sanity_038(self):
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.water_multiple_zones(self)
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


def sanity_012_base(self):
    # sanity_001
    android.control_app.is_app_installed(self)
    android.control_app.remove_app(self)
    android.control_app.install_app(self, "1.65.3")
    android.control_app.launch_app(self)
    android.welcome.slide_welcome_frame(self)
    android.control_app.close_app(self)
    # sanity_002
    android.control_app.launch_app(self)
    android.login.sign_in(self, "jerry.sqa5", "55555555")
    android.main_screen.my_account(self)
    android.login.sign_out(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    # sanity_003
    android.main_screen.my_account(self)
    android.main_screen.buy_blackloud_sprinkler(self)
    android.verify.compare.verify_buy_blackloud_sprinkler(self)
    android.android_btn.android_back(self)
    # sanity_004
    android.main_screen.user_manual(self)
    android.verify.compare.verify_user_manual(self)
    android.android_btn.android_back(self)
    # sanity_005
    android.main_screen.feature_introduction(self)
    android.welcome.slide_welcome_frame(self)
    # sanity_006
    android.main_screen.my_account(self)
    android.main_screen.contact_us(self)
    android.verify.compare.verify_contact_us(self)
    android.android_btn.android_back(self)
    # sanity_007
    android.main_screen.about_blackloud(self)
    android.verify.compare.verify_about_blackloud(self)
    android.android_btn.android_back(self)
    # sanity_008
    android.main_screen.legal_and_privacy_policy(self)
    android.verify.compare.verify_legal_and_privacy_policy(self)
    android.android_btn.android_back(self)
    # sanity_009
    android.verify.compare.verify_app_version(self)
    android.android_btn.android_back(self)
    # sanity_012
    android.main_screen.add_device(self)
    android.wifi_binding.direct_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 1)
    android.schedule.repeat_su(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.common_btn.left_on_top_bar(self)
    android.main_screen.choose_device(self)
    android.verify.next_page.verify_binging_success_without_network(self)
    # sanity_016
    android.dashboard.settings(self)
    android.sys_info.edit_device_name(self, "BUZZI Sprinkler1")
    android.sys_info.back(self)
    android.verify.compare.verify_dashboard_title(self, "BUZZI Sprinkler1")
    android.dashboard.return2main_screen(self)
    android.verify.compare.verify_device_name(self, "BUZZI Sprinkler1")
    # sanity_017
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_zip_code(self)
    android.zip_code.enter_zip_code(self, 22201)
    android.zip_code.choose_zip_code(self, 22201)
    android.verify.compare.verify_zip_code(self, 22201)
    # sanity_018
    android.sys_info.change_zone(self)
    android.zone.set_zone_num(self, 6)
    android.zone.save(self)
    # TODO verify it in dashboard
    # sanity_019
    android.verify.compare.verify_system_date_and_time(self)
    # sanity_020
    android.sys_info.change_wifi(self)
    android.sys_info.yes(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_wifi_ssid(self, "BKwifi_Darcy_2.4G")
    # sanity_021
    android.verify.compare.verify_fw_version(self, "0.00.81")
    # sanity_022
    android.sys_info.back(self)
    android.dashboard.schedule(self, 1)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 1)
    android.schedule.minute(self, 0)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_sa(self)
    android.schedule.save(self)
    # sanity_023
    android.dashboard.schedule(self, 2)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 11)
    android.schedule.minute(self, 10)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    # sanity_024
    android.dashboard.schedule(self, 3)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 7)
    android.schedule.minute(self, 59)
    android.schedule.time_system(self, "PM")
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    # sanity_025
    android.dashboard.schedule(self, 3)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)
    # sanity_026
    android.dashboard.schedule(self, 2)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)
    # sanity_027
    android.dashboard.schedule(self, 1)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.delete_schedule(self)
    android.schedule.yes(self)
    android.schedule.back(self)
    # sanity_029
    android.dashboard.auto_watering(self, "OFF")
    android.verify.compare.verify_auto_watering_status(self, "OFF")
    android.dashboard.return2main_screen(self)
    android.verify.exist.verify_device_auto_watering(self, "OFF")
    android.main_screen.choose_device(self)
    # sanity_028
    android.dashboard.auto_watering(self, "On")
    android.verify.compare.verify_auto_watering_status(self, "On")
    android.dashboard.return2main_screen(self)
    android.verify.exist.verify_device_auto_watering(self, "On")
    android.main_screen.choose_device(self)
    # sanity_030
    android.dashboard.weather_assistant(self, "ON")
    android.verify.compare.verify_weather_assistant_status(self, "ON")
    android.dashboard.return2main_screen(self)
    android.verify.exist.verify_device_weather_assistant(self, "ON")
    android.main_screen.choose_device(self)
    # sanity_031
    android.dashboard.weather_assistant(self, "OFF")
    android.verify.compare.verify_weather_assistant_status(self, "OFF")
    android.dashboard.return2main_screen(self)
    android.verify.exist.verify_device_weather_assistant(self, "OFF")
    # sanity_034
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.launch_watering(self, 1)
    android.verify.exist.verify_watering_zone(self, 1)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)
    android.manual_watering.stop(self)
    # sanity_035
    android.manual_watering.launch_watering(self, 1)
    android.manual_watering.stop(self)
    android.verify.exist.verify_manual_watering_page(self)
    # sanity_037
    android.manual_watering.water_multiple_zones(self)
    android.manual_watering.skip(self)
    android.verify.exist.verify_watering_image(self)
    android.verify.exist.verify_countdown(self)
    android.manual_watering.stop(self)
    android.verify.exist.verify_manual_watering_page(self)
    android.manual_watering.back(self)
    # sanity_039(self):
    android.dashboard.zone_slide_down2up(self)
    android.dashboard.zone(self, 1)
    android.zone.name_your_zone(self, "darcy")
    android.zone.ok(self)
    android.zone.save(self)
    android.verify.compare.verify_zone_name(self, 1, "darcy")
