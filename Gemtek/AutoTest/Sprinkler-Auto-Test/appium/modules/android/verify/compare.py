from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import unittest
import android.common_btn


# ===== Following function on main screen. =====
def verify_device_name(self, device_name):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvName")
    self.assertIsNotNone(el)
    print("[Gemtek] Device name : " + el.text)
    self.assertEqual(device_name, el.text) 
    sleep(1)


# ===== Following function on main screen's private account. =====
def verify_buy_blackloud_sprinkler(self):
    el = self.driver.find_element_by_id("com.android.chrome:id/url_bar")
    self.assertIsNotNone(el)
    self.assertEqual("www.blackloud.com/schmartsprinkler/", el.text) 
    sleep(1)


def verify_user_manual(self):
    el = self.driver.find_element_by_id("com.android.chrome:id/url_bar")
    self.assertIsNotNone(el)
    self.assertEqual("www.blackloud.com/content/SMART_SPRINKLER_QG.pdf", el.text) 
    sleep(1)


def verify_contact_us(self):
    el = self.driver.find_element_by_id("com.android.chrome:id/url_bar")
    self.assertIsNotNone(el)
    self.assertEqual("www.blackloud.com/contact-us/", el.text) 
    sleep(1)


def verify_about_blackloud(self):
    el = self.driver.find_element_by_id("com.android.chrome:id/url_bar")
    self.assertIsNotNone(el)
    self.assertEqual("www.blackloud.com/about-us/", el.text) 
    sleep(1)


def verify_legal_and_privacy_policy(self):
    el = self.driver.find_element_by_id("com.android.chrome:id/url_bar")
    self.assertIsNotNone(el)
    self.assertEqual("www.blackloud.com/privacy-policy/", el.text) 
    sleep(1)


def verify_app_version(self):
    ver = _get_file_name()
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvVersion")
    self.assertIsNotNone(el)
#    app_ver = el.text.split(" ")
    print("[Gemtek] APP Version is : " + el.text)
    self.assertEqual(ver, el.text)


# ===== Following function on dashboard page. =====
def verify_dashboard_title(self, sprinkler_name):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvTitle")
    self.assertIsNotNone(el)
    print("[Gemtek] Dashboard title name : " + el.text)
    self.assertEqual(sprinkler_name, el.text) 
    sleep(1)


def verify_auto_watering_status(self, status):
    sleep(2)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/auto_watering_status")
    self.assertIsNotNone(el)
    print("[Gemtek] Auto watering status is : " + el.text)
    self.assertEqual(str(status), el.text) 


def verify_weather_assistant_status(self, status):
    sleep(2)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/weather_assistant_status")
    self.assertIsNotNone(el)
    print("[Gemtek] Weather assistant status is : " + el.text)
    self.assertEqual(str(status), el.text) 


def verify_rain_delay_days_status(self, status):
    sleep(2)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/snoozeFinish")
    self.assertIsNotNone(el)
    print("[Gemtek] Rain delay days status is : " + el.text)
    self.assertEqual(str(status), el.text) 


def _get_zone_element_status(self, num):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_status").find_elements_by_class_name("android.widget.LinearLayout")
    self.assertIsNotNone(el)
#    print("[Gemtek] el length = " + str(len(el)))
    for i in range(1, len(el)):
        if i is 3 or i is 6 or i is 9:
            continue
#        print("[Gemtek] i = " + str(i))
        els = el[i].find_elements_by_class_name("android.widget.RelativeLayout")
        self.assertIsNotNone(els)
#        print("[Gemtek] els length = " + str(len(els)))
        els0 = els[0].find_element_by_class_name("android.widget.TextView")
        self.assertIsNotNone(els0)
        els1 = els[1].find_element_by_class_name("android.widget.TextView")
        self.assertIsNotNone(els1)
#        sprinkle = el[i].find_element_by_class_name("android.widget.ImageView")
        zone = els0.text.split("\n")
#        print("zone[0] = " + zone[0])
#        print("zone[1] = " + zone[1])
        if str(num) in zone[0]:
            print("[Gemtek] Found " + zone[0])
            return zone[0], zone[1], els1.text
    return None, None, None


def verify_zone_name(self, num, name):
    if num < 1 or num > 8:
        print("[Gemtek] You enter a wrong number.")
        return

    zone, zone_name, watering = _get_zone_element_status(self, str(num))

    if zone is None:
        print("[Gemtek] Not found Zone" + str(num))
        return
#    print("\n[Gemtek] " + zone + " " + zone_name + "\n")
    self.assertEqual(str(name), zone_name) 


def verify_zone_status(self, num, status):
    if num < 1 or num > 8:
        print("[Gemtek] You enter a wrong number.")
        return

    zone, zone_name, watering = _get_zone_element_status(self, str(num))

    if zone is None:
        print("[Gemtek] Not found Zone" + str(num))
        return
#    print("\n[Gemtek] " + zone + " " + watering + "\n")
    self.assertEqual(str(status), watering) 


def verify_zone_watering(self, num):  # TODO Not finish
    if num < 1 or num > 8:
        print("[Gemtek] You enter a wrong number.")
        return

    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_status").find_elements_by_class_name("android.widget.LinearLayout")
    self.assertIsNotNone(el)
    print("[Gemtek] el length = " + str(len(el)))
    
    for i in range(1, len(el)):
        if i is 3 or i is 6 or i is 9:
            continue
        print("[Gemtek] i = " + str(i))
        els = el[i].find_elements_by_class_name("android.widget.RelativeLayout")
        self.assertIsNotNone(els)
        print("[Gemtek] els length = " + str(len(els)))
        els0 = els[0].find_element_by_class_name("android.widget.TextView")
        self.assertIsNotNone(els0)
        zone = els0.text.split("\n")
        if str(num) in zone[0]:
            print("[Gemtek] Found " + zone[0])
            watering_img = els[1].find_elements_by_class_name("android.widget.ImageView")
            break
    self.assertIsNotNone(watering_img)
    self.assertTrue(watering_img.is_enabled())

#    print("[Gemtek] el length = " + str(len(el)))
#    for i in range(1, len(el)):
#        print("[Gemtek] i = " + str(i))
#        els = el[i].find_elements_by_class_name("android.widget.RelativeLayout")
#        print("[Gemtek] els01 length = " + str(len(els)))
#        els0 = els[0].find_elements_by_class_name("android.widget.TextView")
#        els1 = els[1].find_elements_by_class_name("android.widget.TextView")
#        print("[Gemtek] els0 = " + els0[0].text)
#        print("[Gemtek] els1 = " + els1[0].text)
#    els = el[1].find_elements_by_class_name("android.widget.TextView")
#    print("")
#    print(len(els))
#    print("")
#    print("[Gemtek] el 0 = " + els[0].text)
#    self.assertIsNotNone(els)


# ===== Following function on setting page. =====
def verify_zip_code(self, zip_code):
    sleep(2)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_zip_code_text")
    self.assertIsNotNone(el)
    print("[Gemtek] Zip Code is : " + el.text)
    self.assertEqual(str(zip_code), el.text) 


def verify_system_date_and_time(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_time")
    self.assertIsNotNone(el)
    print("[Gemtek] system time : " + el.text)
    time = self.driver.device_time
#    self.assertEqual(time, el.text) # TODO Not finish.
    sleep(1)


def verify_wifi_ssid(self, ssid):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_ssid")
    self.assertIsNotNone(el)
    tmp = el.text.split(":")
    print("[Gemtek] WiFi SSID is : " + el.text)
    self.assertEqual(str(ssid), tmp[1])


def _get_app_version(file):
    tmp = str(file).split("#")
    git_version = str(tmp[1]).split(".")
    tmp2 = str(tmp[0]).split("-")
    app_ver = str(tmp2[1])[1:]
    return int(git_version[0]), app_ver


def _get_file_name():
    git_version_max = 0
    apk_path = str(os.path.abspath("..")) + "/build/outputs/apk/"
    for subdir, dirs, files in os.walk(apk_path): 
        for file in files:
            git_version, app_ver = _get_app_version(file)
            if git_version > git_version_max:
                git_version_max = git_version
                app_ver_max = app_ver
    final_string = "Version " + str(app_ver_max) + " (" + str(git_version_max) + ")"
#    print("\n[Gemtek] file name = " + str(file) + " " + str(git_version_max) + " " + str(app_ver) + " " + final_string + "\n")
    return final_string


def verify_fw_version(self, fw_ver):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/fw_version")
    self.assertIsNotNone(el)
    print("[Gemtek] FW version is : " + el.text)
    self.assertEqual(str(fw_ver), el.text) 
