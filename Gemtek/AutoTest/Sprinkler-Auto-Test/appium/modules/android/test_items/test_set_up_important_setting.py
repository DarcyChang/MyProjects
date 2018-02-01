# Copyright (C) 2017 Gemtek Technology Co., Ltd.
# Author: Darcy_Chang
# E-mail: darcy_chang@gemteks.com
#
# This python code for Gemtek's project "Sprinkler" that android APP auto test.
# Auto test from welcome frame start, till initial setting finish.
# About set up some important settings.


from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.welcome
import android.create_new_account
import android.login
import android.main_screen
import android.wifi_binding
import android.android_btn
import android.zip_code
import android.zone
import android.schedule


def initial_setting(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_device(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 22201)
    android.zip_code.choose_zip_code(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.zone.set_zone_all(self)
    android.zone.set_zone_num(self, 1)
    android.zone.set_zone_num(self, 2)
    android.zone.set_zone_num(self, 3)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.ok_btn_on_bottom(self)


def all_button(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.choose_deivce(self)
    android.zip_code.cancel(self)
    android.main_screen.choose_device(self)
    android.zip_code.zip_code(self)
    android.zip_code.enter_zip_code(self, 33301)
    android.zip_code.choose_zip_code(self)
    android.wifi_binding.weather_assistant(self)
    android.wifi_binding.ok(self)
    android.wifi_binding.weather_assistant(self)
    android.wifi_binding.next_btn_for_first_setting(self)
    android.common_btn.back_btn_on_bottom(self)
    android.wifi_binding.cancel(self)


def main():
    print("initial_setting")


if __name__ == '__main__':
    main()
    print("test_set_up_important_setting.py")
