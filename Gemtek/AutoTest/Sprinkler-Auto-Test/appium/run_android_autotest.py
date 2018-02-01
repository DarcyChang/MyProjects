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
import subprocess


# Returns abs path relative to this file and not cwd
# XXX What is this ? do not assign a lambda expression, use a def [E731]
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def get_device_name():
    result = subprocess.getoutput("adb devices")
    name = result.split()
#    print(name[4])
    return name[4]


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
        desired_caps['deviceName'] = get_device_name()
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

    def test_sanity001(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_001(self)
"""
    def test_sanity002(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_002(self)

    def test_sanity003(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_003(self)

    def test_sanity004(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_004(self)

    def test_sanity005(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_005(self)

    def test_sanity006(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_006(self)

    def test_sanity007(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_007(self)

    def test_sanity008(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_008(self)

    def test_sanity009(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_009(self)

    def test_sanity010(self):
        global func 
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_010(self)

    def test_sanity016(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_016(self)

    def test_sanity017(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_017(self)

    def test_sanity018(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_018(self)

    def test_sanity019(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_019(self)

    def test_sanity020(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_020(self)

    def test_sanity021(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_021(self)

    def test_sanity022(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_022(self)

    def test_sanity023(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_023(self)

    def test_sanity024(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_024(self)

    def test_sanity025(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_025(self)

    def test_sanity026(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_026(self)

    def test_sanity027(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_027(self)

    def test_sanity028_01(self):  # sanity 029
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_029(self)

    def test_sanity028_02(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_028(self)

    def test_sanity030_01(self):  # sanity 031
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_031(self)

    def test_sanity030_02(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_030(self)

    def test_sanity034(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_034(self)

    def test_sanity035(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_035(self)

    def test_sanity036(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_036(self)

    def test_sanity037(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_037(self)

    def test_sanity038(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_038(self)

    def test_sanity039(self):
        global func
        func = sys._getframe().f_code.co_name
        android.test_items.test_sanity.sanity_039(self)

#    def test_aa_sanity011(self):
#        global func 
#        func = sys._getframe().f_code.co_name
#        android.test_items.test_sanity.sanity_011(self)

#    def test_aa_sanity012(self):
#        global func 
#        func = sys._getframe().f_code.co_name
#        android.test_items.test_sanity.sanity_012(self)

#    def test_aa_sanity013(self):
#        global func 
#        func = sys._getframe().f_code.co_name
#        android.test_items.test_sanity.sanity_013(self)

#    def test_aa_sanity014(self):
#        global func 
#        func = sys._getframe().f_code.co_name
#        android.test_items.test_sanity.sanity_014(self)

#    def test_aa_sanity015(self):
#        global func 
#        func = sys._getframe().f_code.co_name
#        android.test_items.test_sanity.sanity_015(self)

#    def test_real_run_1(self):
#        android.test_items.test_real.sanity_01(self)
#        android.test_items.test_real.sanity_02(self)
#        android.test_items.test_real.sanity_03(self)
#        android.test_items.test_real.sanity_04(self)
#        android.test_items.test_real.sanity_05(self)
#        android.test_items.test_real.sanity_06(self)
#        android.test_items.test_real.sanity_07(self)
#        android.test_items.test_real.sanity_08(self)

#    def test_script_run_1(self):
#        android.test_items.test_real.full_flow(self)
#        android.test_items.test_binding_flow.initial_setting(self)


#    def test_script_run_2(self):
#        android.test_items.test_set_up_important_setting.initial_setting(self)


#    def test_script_run_3(self):
#        android.test_items.test_set_up_important_setting.all_button(self)


#    def test_script_run_practice(self):
#        android.test_items.test_dashboard_setting.dashboard_zone_test(self)
#        android.test_items.test_dashboard_setting.watering_test(self)
#        android.test_items.test_dashboard_setting.zip_code_test(self)
#        android.test_items.test_dashboard_setting.zone_test(self)
#        android.test_items.test_dashboard_setting.initial_setting(self)
#        android.test_items.test_dashboard_setting.all_button(self)


#    Test script
#        def test_wakeup(self):
#        sleep(1)
#        self.driver.press_keycode(26) # press home
#        sleep(1)
"""

if __name__ == '__main__':
    print("\n[Gemtek] Sprinkler Auto Test Start!\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
#    unittest.TextTestRunner(verbosity=2).run(suite)
    runner = HtmlTestRunner.HTMLTestRunner(
            output="android", 
            report_title="Sprinkler Auto Test report"
    ).run(suite)
