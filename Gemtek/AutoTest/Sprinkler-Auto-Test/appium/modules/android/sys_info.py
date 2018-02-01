from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.android_btn


def edit_device_name(self, device_name):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_name_edit")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    device_text = self.driver.find_element_by_class_name("android.widget.EditText")
    device_text.clear()
    device_text.send_keys(device_name)
    sleep(1)
    save(self)


def change_zip_code(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_zip_code")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def change_zone(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_zone")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def change_wifi(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_change_wifi")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def yes(self):
    android.android_btn.android_connect_wifi_btn(self)


def save(self):
    android.android_btn.android_connect_wifi_btn(self)


def cancel(self):
    android.android_btn.android_cancel_btn(self)


def back(self):
    android.common_btn.left_on_top_bar(self)


if __name__ == '__main__':
    print("sys_info.py")
