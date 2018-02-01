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
import android.zip_code
import android.manual_watering
import android.verify.click
import android.verify.compare


def initial_setting(self):
    print("initial_setting")
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.dashboard.return2main_screen(self)
    android.main_screen.choose_device(self)
    android.dashboard.schedule_edit(self)
    android.schedule.hour(self, 6)
    android.schedule.minute(self, 30)
    android.schedule.time_system(self, "PM")
    android.schedule.repeat_all(self)
    android.schedule.repeat_m(self)
    android.schedule.repeat_su(self)
    android.schedule.repeat_tu(self)
    android.schedule.repeat_w(self)
    android.schedule.save(self)
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


def all_button(self):
    print("all_button")
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
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
    android.dashboard.weather_assistant(self)
    android.dashboard.rain_delay_days(self)
    android.android_btn.android_back(self)
    sleep(5)


def watering_test(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.dashboard.manual(self)
    android.manual_watering.zone_time(self, 8)
    android.manual_watering.watering_time(self, 1, 30)
    android.manual_watering.watering_time(self, 2, 10)
    android.manual_watering.watering_time(self, 3, 1)
    android.manual_watering.watering_time(self, 4, 31)
    android.manual_watering.watering_time(self, 5, -1)
    android.manual_watering.watering_time(self, 8, 29)
    android.manual_watering.launch_watering(self, 1)
    android.manual_watering.watering_zone(self)
    android.manual_watering.countdown(self)
    android.manual_watering.stop(self)
    android.manual_watering.water_multiple_zones(self)
    sleep(10)


def zip_code_test(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.dashboard.settings(self)
    android.sys_info.change_zip_code(self)
    android.zip_code.enter_zip_code(self, 222)
    android.zip_code.choose_zip_code(self, 22210)


def zone_test(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.dashboard.schedule_edit(self)
    android.schedule.slide_down2up(self)
    android.schedule.name_your_zone(self, 3, "sunny! yesterday.")
    android.schedule.name_your_zone(self, 6, "trello TRELLO 12334546346536565")
    android.schedule.name_your_zone(self, 6, "love you oh~")
    android.schedule.watering_time(self, 1, 1)
    android.schedule.watering_time(self, 2, 3)
    android.schedule.watering_time(self, 3, 35)
    android.schedule.watering_time(self, 4, 0)
    android.schedule.watering_time(self, 5, 5)
    android.schedule.watering_time(self, 8, 10)
    android.schedule.save(self)
    sleep(10)
    android.schedule.slide_up2down(self)
    sleep(10)


def dashboard_zone_test(self):
#    android.welcome.slide_welcome_frame(self)
#    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.dashboard.zone_slide_down2up(self)
#    android.verify.compare.verify_zone_name(self, 1, "darcy")
#    android.verify.compare.verify_zone_name(self, 2, "123")
#    android.verify.compare.verify_zone_name(self, 3, "aaaaa")
#    android.verify.compare.verify_zone_name(self, 4, "abcdefghijklmnopqrst")
#    android.verify.compare.verify_zone_name(self, 5, "SKIP")
#    android.verify.compare.verify_zone_name(self, 6, "")
#    android.verify.compare.verify_zone_name(self, 7, "hr")
#    android.verify.compare.verify_zone_name(self, 8, "KING")
#    android.verify.compare.verify_zone_status(self, 1, "OFF")
#    android.verify.compare.verify_zone_status(self, 2, "SKIP")
#    android.verify.compare.verify_zone_status(self, 3, "OFF")
#    android.verify.compare.verify_zone_status(self, 4, "OFF")
#    android.verify.compare.verify_zone_status(self, 5, "SKIP")
#    android.verify.compare.verify_zone_status(self, 6, "OFF")
#    android.verify.compare.verify_zone_status(self, 7, "OFF")
#    android.verify.compare.verify_zone_status(self, 8, "SKIP")
#    android.verify.compare.verify_zone_watering(self, 1)
#    android.verify.compare.verify_zone_watering(self, 2)
#    android.verify.compare.verify_zone_watering(self, 3)
    android.verify.compare.verify_zone_watering(self, 4)
#    android.verify.compare.verify_zone_watering(self, 5)
#    android.verify.compare.verify_zone_watering(self, 6)
#    android.verify.compare.verify_zone_watering(self, 7)
#    android.verify.compare.verify_zone_watering(self, 8)
#    android.dashboard.zone(self, 1)
#    android.dashboard.zone(self, 2)
#    android.dashboard.zone(self, 3)
#    android.dashboard.zone(self, 4)
#    android.dashboard.zone(self, 5)
#    android.dashboard.zone(self, 6)
#    android.dashboard.zone(self, 7)
#    android.dashboard.zone(self, 8)


def main():
    print("dashboard_setting")


if __name__ == '__main__':
    main()
    print("test_dashboard_setting.py")
