from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


# ===== Following function on binding page. =====
def verify_binging_network_success(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zipCodeSetting")
    self.assertIsNotNone(el)
    sleep(1)


# ===== Following function on dashboard page. =====
def verify_binging_success(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/activity_device_status")
    self.assertIsNotNone(el)
    print("[Gemtek] Binding success.")
    sleep(1)


def verify_binging_success_without_network(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/weather_info").find_element_by_class_name("android.widget.TextView")
    self.assertIsNotNone(el)
    self.assertEqual("No network", el.text)
    print("[Gemtek] Binding success without network.")
    sleep(1)
