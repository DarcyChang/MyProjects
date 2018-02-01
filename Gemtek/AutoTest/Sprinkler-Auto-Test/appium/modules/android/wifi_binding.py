#coding=utf-8

import time
import os
from time import sleep
from appium import webdriver
import appium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import android.common_btn
from appium.webdriver.common.touch_action import TouchAction


def _select_wifi_button(self, ssid):
    if "BUZZI" in ssid:
        return self.driver.find_elements_by_id('android:id/title')
    else:
        return self.driver.find_elements_by_id('com.blackloud.wetti:id/tvWifiName')


def _enter_wifi_password(self, password):
    try:
        password_text = self.driver.find_element_by_id("com.blackloud.wetti:id/etPass")
        WebDriverWait(self.driver, 5, 1).until(lambda driver: password_text)
        print("[Gemtek] Keyin password : "+password)
        password_text.send_keys(password)
        sleep(3)
        android.common_btn.right_on_top_bar(self)
    except NoSuchElementException:
        print("[Gemtek] No passward")


def _check_connect(self):  #  TODO: Not finish.
#    connect_text = self.driver.find_elements_by_class_name("android.widget.RelativeLayout").find_element_by_id("android:id/title")
    connect = self.driver.find_element_by_class_name("android.widget.ListView")
    el = connect.find_elements_by_android_uiautomator('new UiSelector().text("dlink")')
    self.assertIsNotNone(el)
#    el.click()
 #   self.assertIsNotNone(connect_text)
 #   print("[Gemtek] "+connect_text.text)
 #   if "已連線" in connect_text.text or "Connected" in connect_text.text:
 #       print("[Gemtek] 已連線(Connected)")
 #       return True


def _try_again(self):
    i = 0
    while(i < 3):
        try:
            WebDriverWait(self.driver, 50, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/tvTryAgain"))
            print("[Gemtek] Retry connect wifi again.")
            self.driver.find_element_by_id("com.blackloud.wetti:id/tvTryAgain").click()
            i += 1
        except TimeoutException:
            print("[Gemtek] connected wifi.")
            break


def cloud_control(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/wifi_connect")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    i = 0
    while(i < 10):
        try:
            el = self.driver.find_element_by_id("com.blackloud.wetti:id/wifi_connect")
            self.assertIsNotNone(el)
            el.click()
            sleep(1)
            i += 1
            if(i == 10):
                break
        except:
            break
    sleep(1)


def no_flashing_red_light(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/reset_guide_link")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/reset_back")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def direct_control(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/direct_connect")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    i = 0
    while(i < 10):
        try:
            el = self.driver.find_element_by_id("com.blackloud.wetti:id/direct_connect")
            self.assertIsNotNone(el)
            el.click()
            sleep(1)
            i += 1
            if(i == 10):
                break
        except:
            break
    sleep(1)


def open_wifi_setting(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/system_wifi_setting")
    self.assertIsNotNone(el)
    action = TouchAction(self.driver)
    action.tap(el).perform()
#    el.click()
    sleep(3)
    while(1):  # TODO Here is a bug. Touch "open wifi setting" no response.
        try:
            el = self.driver.find_element_by_id("com.blackloud.wetti:id/system_wifi_setting")
            el.click()
            sleep(1)
        except:
            break
#    WebDriverWait(self.driver, 60, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/system_wifi_setting"))
#    self.driver.find_element_by_id("com.blackloud.wetti:id/system_wifi_setting").click()


def _search_ssid(ssid, ssid_list):
    for e in ssid_list:
        print("[Gemtek] search ssid : "+e.text)
        if e.text == ssid:
            print("[Gemtek] : Scan SSID " + ssid + " PASS!")
            return True, e
    return False, None


def wifi_connect_sprinkler(self, ssid):
    print("[Gemtek] WiFi scan sprinkler "+ssid+" start")
    scan_result = False
    ssid_elem = None
    for i in range(10):
#        elem = _select_wifi_button(self, ssid)
        elem = self.driver.find_elements_by_id('android:id/title')
        scan_result, ssid_elem = _search_ssid(ssid, elem)
        if scan_result:
            break
        else:
            sleep(6)  # TODO how to wifi scan?

    if not scan_result:
#        appium.raiseError("[Gemtek] : Scan SSID " + ssid + " FAIL!")
        print("[Gemtek] : Scan SSID " + ssid + " FAIL!")
    else:
        ssid_elem.click()
        sleep(1)
        try:
            android.android_btn.android_connect_wifi_btn(self)
            print("[Gemtek] connected SSID : "+ssid)
        except:
            android.android_btn.android_cancel_btn(self)


def wifi_connect_ap(self, ssid, password=""):
    print("[Gemtek] WiFi scan AP "+ssid+" start")
    scan_result = False
    ssid_elem = None
    for j in range(3):
        for i in range(6):
#            elem = _select_wifi_button(self, ssid)
            elem = self.driver.find_elements_by_id('com.blackloud.wetti:id/tvWifiName')
            scan_result, ssid_elem = _search_ssid(ssid, elem)
            if scan_result:
                break
            else:
                android.common_btn.slide_down2up(self, 400, 990, 400, 400)
        if scan_result:
            break
        else:
            _rescan(self)

    if not scan_result:
#        appium.raiseError("[Gemtek] : Scan SSID " + ssid + " FAIL!")
        print("[Gemtek] : Scan SSID " + ssid + " FAIL!")
    else:
        ssid_elem.click()
        sleep(1)

    _enter_wifi_password(self, password)
#    _try_again(self)


def wireless_setup(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/twWirelessButton")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def wired_setup(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/twWiredButton")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def _rescan(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnRescan")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def weather_assistant(self, switch):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/aeather_switch")
    self.assertIsNotNone(el)
    if switch == "ON" and str(el.get_attribute("checked")) == "false":
        el.click()
        ok(self)
    elif switch == "OFF" and str(el.get_attribute("checked")) == "true":
        el.click()
    sleep(1)


def schedule(self, num):
    if(int(num) < 1 or int(num) > 3):
        print("[Gemtek] Schedule number must be 1 to 3.")
        return    

    recourse_id = "com.blackloud.wetti:id/schedule"+str(num)+"Layout"
    el = self.driver.find_element_by_id(recourse_id)
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def next_wired(self):
    android.common_btn.right_on_top_bar(self)
    sleep(3)


def next_to_set_up_network_connection(self):
    android.common_btn.next_btn_on_bottom(self, "check_next")


def next_to_continue_setting(self):
#    path = "./screen_shot/" + str(time.strftime("%Y.%m.%d"))
#    if not os.path.exists(path):
#        os.makedirs(path)
#    name = path + "/" + "binging_finish" + str(time.strftime("-%Y.%m.%d_%H:%M:%S")) + ".png"
#    self.driver.get_screenshot_as_file(name)
    try:
        android.common_btn.next_btn_on_bottom(self, "tvOk")
    except:
        path = "./screen_shot/" + str(time.strftime("%Y.%m.%d"))
        if not os.path.exists(path):
            os.makedirs(path)
        name = path + "/" + "binging_finish" + str(time.strftime("-%Y.%m.%d_%H:%M:%S")) + ".png"
        self.driver.get_screenshot_as_file(name)
        _try_again(self)


def next_btn_for_first_setting(self):
    android.common_btn.next_btn_on_bottom(self, "setNextBtn")


def ok(self):
    android.android_btn.android_connect_wifi_btn(self)


def cancel(self):
    android.common_btn.cancel_on_top_bar(self, "settingCancel")


if __name__ == '__main__':
    print("[Gemtek] wifi_binding.py")
