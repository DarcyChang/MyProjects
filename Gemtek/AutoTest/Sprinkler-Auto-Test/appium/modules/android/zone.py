from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.android_btn


def set_zone_all(self): 
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/checkZoonAll")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def set_zone_num(self, zone_num): 
    recourseid = "com.blackloud.wetti:id/checkZoon"+str(zone_num)
    print("[Gemtek] zone recourse id "+recourseid)
    el = self.driver.find_element_by_id(recourseid)
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def name_your_zone(self, name):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/editText")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    edit_name = self.driver.find_element_by_class_name("android.widget.EditText")
    edit_name.clear()
    edit_name.send_keys(name)
    sleep(1)


def ok(self):
    android.android_btn.android_connect_wifi_btn(self)
    

def back(self):
    android.common_btn.left_on_top_bar(self)


def cancel(self):
    android.android_btn.android_cancel_btn(self)


def slide_right2left_in_zone(self):
    android.common_btn.slide_right2left(self)


def slide_left2right_in_zone(self):
    android.common_btn.slide_left2right(self, 180, 800, 690, 800)


def change_zone_photo(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/change_zone_photo")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def taking_photo(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/take_photo")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def choose_photo_from_gallery(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/select_photo")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def delete_photo(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/delete_photo")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def cancel_photo(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/cancel_photo")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def save(self):
    android.common_btn.right_on_top_bar(self)


def cancel(self):
    android.common_btn.left_on_top_bar(self)


if __name__ == '__main__':
    print("[Gemtek] zone.py")
