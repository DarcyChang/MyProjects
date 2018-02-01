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


def initial_setting(self):
    android.welcome.slide_welcome_frame(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    sleep(30)  #  For zenfone6
    android.android_btn.android_cancel_btn(self)  # For zenfone6
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)


def all_button(self):
    android.welcome.slide_welcome_frame(self)
    android.create_new_account.create_account(self)
    android.login.forgot_password(self)
    android.login.sign_in(self, "jerry.sqa5", "55555555")
    android.main_screen.my_account(self)
    android.login.sign_out(self)
    android.login.sign_in(self, "changdarcy", "changdarcy")
    android.main_screen.add_device(self)
    android.wifi_binding.cloud_control(self)
    android.wifi_binding.reset_guide_link(self)
    android.common_btn.slide_right2left(self)
    android.common_btn.left_on_top_bar(self)
    android.wifi_binding.cloud_control(self)
    android.common_btn.slide_right2left(self)
    android.wifi_binding.open_wifi_setting(self)
    android.wifi_binding.wifi_connect_sprinkler(self, "BUZZISPR_1FB5AC")
    android.android_btn.android_back(self)
    android.wifi_binding.next_to_set_up_network_connection(self)
    android.wifi_binding.wireless_setup(self)
    android.wifi_binding.wifi_connect_ap(self, "BKwifi_Darcy_2.4G", "88888888")
    android.wifi_binding.next_to_continue_setting(self)


def main():
    print("initial_setting")


if __name__ == '__main__':
    main()
    print("test_binding_flow.py")
