#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from time import sleep
import time
from appium import webdriver
import android.common_btn
import android.welcome
import android.create_new_account
import android.login
import android.ctrl_sprinkler
import android.wifi_binding
import android.test_items.test_binding_flow
import android.test_items.test_set_up_important_setting
import android.test_items.test_dashboard_setting
import android.test_items.test_real
import android.test_items.test_sanity
import HtmlTestRunner


# Returns abs path relative to this file and not cwd
# XXX What is this ? do not assign a lambda expression, use a def [E731]
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class ContactsAndroidTests(unittest.TestCase):
    def screenshot(self, func):  #需要写这个方法才能实现截图
        path = "./screen_shot/" + str(time.strftime("%Y.%m.%d"))
        if not os.path.exists(path):
            os.makedirs(path)
        name = path + "/" + func + str(time.strftime("-%Y.%m.%d_%H:%M:%S")) + ".png"  #拼接截图文件名
        self.driver.get_screenshot_as_file(name)  #图片保存在定义路径中

    # initialize
    def setUp(self):
        print("==============================================================")
        print("[Gemtek] device setUp start")
        print("==============================================================")
        apk_name = "WETTI_APP_Production-V1.65.3-build#1615.apk"  # TODO auto setting
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['version'] = '4.4.2'  # tablet, Zenfone6
        desired_caps['deviceName'] = 'EAAZCY17F178'  # zenfone 6
        desired_caps['app'] = PATH(str(os.path.abspath("..")) + "/build/outputs/apk/" + apk_name)
        desired_caps['appPackage'] = 'com.blackloud.wetti'
        desired_caps['appActivity'] = 'com.blackloud.sprinkler.WelcomePageActivity'
        desired_caps['noReset'] = True
        desired_caps['fullReset'] = False
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)
        print("==============================================================")
        print("[Gemtek] device setUp finish")
        print("==============================================================")

    # Cleaning up
    def tearDown(self):
        print("==============================================================")
        print("[Gemtek] device tearDown")
        print("==============================================================")
        self.screenshot(func)
        self.driver.quit()

    def test_12(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_012_base(self)


if __name__ == '__main__':
    print("\n[Gemtek] Sprinkler Auto Test Start!\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    runner = HtmlTestRunner.HTMLTestRunner(
            output="android", 
            report_title="Sprinkler Auto Test report"
    ).run(suite)
