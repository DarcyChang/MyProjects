# Copyright (C) 2017 Gemtek Technology Co., Ltd.
# Author: Darcy_Chang
# E-mail: darcy_chang@gemteks.com
#
# This python code for Gemtek's project "Sprinkler" that android APP auto test.
# Auto test from welcome frame start, till cloud agent binding finish.


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


def sanity_01(self):
    android.control_app.is_app_installed(self)
    android.control_app.remove_app(self)
    android.control_app.install_app(self)
    android.control_app.launch_app(self)
    android.welcome.slide_welcome_frame(self)
    android.control_app.close_app(self)


def sanity_02(self):
    android.login.sign_in(self, "jerry.sqa5", "55555555")
    android.main_screen.my_account(self)
    android.login.sign_out(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    

def sanity_03(self):
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.weather_assistant(self, "ON")
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 0)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 7)
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.gtk_event.wait_any_key("[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
#    android.gtk_event.wait_any_key("[Gemtek] Wait, please connect buzzi wifi and enter any key to continue.\n")


def sanity_04(self):
    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_home(self)
    android.control_app.launch_app(self)
    android.wifi_binding.cloud_control(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.weather_assistant(self, "ON")
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 2)
    android.schedule.hour(self, 7)
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.gtk_event.wait_any_key("[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
    sleep(10)


def sanity_05(self):
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
    android.wifi_binding.schedule(self, 0)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 7)
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.common_btn.left_on_top_bar(self)
    android.gtk_event.wait_any_key("[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
#    android.gtk_event.wait_any_key("[Gemtek] Wait, please connect buzzi wifi and enter any key to continue.\n")
    sleep(5)

    
def sanity_06(self):
    android.android_btn.android_change_wifi_network(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_home(self)
    android.control_app.launch_app(self)
    android.wifi_binding.direct_control(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.main_screen.choose_device(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 2)
    android.schedule.hour(self, 7)
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    android.gtk_event.wait_any_key("[Gemtek] Wait, please reset deivce until wifi red LED blink and enter any to continue.\n")
    sleep(10)


def sanity_07(self):
    android.main_screen.my_account(self)
    android.verify.compare.verify_app_version(self, "1.65.2")
    android.main_screen.buy_blackloud_sprinkler(self)
    android.android_btn.android_back(self)
    android.main_screen.user_manual(self)
    android.android_btn.android_back(self)
    android.main_screen.contact_us(self)
    android.android_btn.android_back(self)
    android.main_screen.about_blackloud(self)
    android.android_btn.android_back(self)
    android.main_screen.legal_and_privacy_policy(self)
    android.android_btn.android_back(self)
    android.main_screen.feature_introduction(self)
    android.welcome.slide_welcome_frame(self)


def sanity_08(self):
    android.main_screen.choose_device(self)
    android.verify.compare.verify_device_name(self, "BUZZI Sprinkler1")
    android.main_screen.choose_device(self)
    android.verify.compare.verify_dashboard_title(self, "BUZZI Sprinkler1")
    android.verify.compare.verify_auto_watering_status(self, "On")
    android.verify.compare.verify_weather_assistant_status(self, "ON")
    android.verify.compare.verify_rain_delay_days_status(self, "OFF")
    android.verify.click.verify_rain_delay_days_click(self)
    android.dashboard.settings(self)
    android.verify.compare.verify_zip_code(self, 10001)
    android.verify.compare.verify_wifi_ssid(self, "BKwifi_Darcy_2.4G")


def sanity_105(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wired_setup(self)
    android.wifi_binding.no_flashing_red_light(self)
    android.wifi_binding.next_wired(self)
    android.gtk_event.wait_any_key("[Gemtek] Wait, if device wifi blue LED light, enter any key.")
    android.wifi_binding.next_to_continue_setting(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 94536)
    android.zip_code.choose_zip_code(self, 94536)
    android.wifi_binding.weather_assistant(self, "ON")
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.schedule(self, 0)
    android.wifi_binding.schedule(self, 1)
    android.schedule.hour(self, 7)
    android.schedule.repeat_all(self)
    android.schedule.save(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)
    sleep(5)

 
def full_flow(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")

    #  binging
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)

    #  after binding and then first setting system
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 22201)
    android.zip_code.choose_zip_code(self, 22201)
    android.wifi_binding.weather_assistant(self, "ON")
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.zone.set_zone_num(self, 1)
    android.zone.set_zone_num(self, 2)
    android.zone.set_zone_num(self, 3)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)

    #  dashboard setting
    android.main_screen.choose_device(self)
    android.dashboard.return2main_screen(self)
    android.main_screen.choose_device(self)
    android.dashboard.weather_assistant(self)

    android.dashboard.settings(self)
    android.sys_info.back(self)
    android.dashboard.settings(self)
    android.sys_info.edit_device_name(self, "darcy123456789123456789")
    android.sys_info.change_zip_code(self)
    android.zip_code.enter_zip_code(self, 22201)
    android.zip_code.choose_zip_code(self)
    android.sys_info.change_wifi(self)
    android.sys_info.yes(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)
    android.main_screen.choose_device(self)

    android.dashboard.schedule(self, 3)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 10)
    android.schedule.minute(self, 59)
    android.schedule.time_system(self, "PM")
    android.schedule.repeat_all(self)
    android.schedule.repeat_m(self)
    android.schedule.repeat_su(self)
    android.schedule.repeat_tu(self)
    android.schedule.repeat_w(self)
    android.schedule.save(self)

    android.dashboard.schedule(self, 1)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 1)
    android.schedule.minute(self, 0)
    android.schedule.time_system(self, "AM")
    android.schedule.repeat_all(self)
    android.schedule.repeat_m(self)
    android.schedule.repeat_su(self)
    android.schedule.repeat_tu(self)
    android.schedule.repeat_w(self)
    android.schedule.save(self)

    android.dashboard.schedule(self, 2)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 11)
    android.schedule.minute(self, 10)
    android.schedule.time_system(self, "PM")
    android.schedule.repeat_all(self)
    android.schedule.repeat_m(self)
    android.schedule.repeat_su(self)
    android.schedule.repeat_tu(self)
    android.schedule.repeat_w(self)
    android.schedule.save(self)

    android.dashboard.weather_slide_rigth2left(self)
    android.dashboard.weather_slide_left2right(self)
    android.dashboard.auto_watering(self)
#    android.dashboard.weather_assistant(self)
    android.dashboard.rain_delay_days(self)
    android.android_btn.android_back(self)
    sleep(5)
