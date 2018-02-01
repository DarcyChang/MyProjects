import unittest
from time import sleep
from appium import webdriver


def create_account(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgBarRight")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBarLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvCreateAccount")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBarRight")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("android:id/button1")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
#   self.driver.press_keycode(4) # press return
#    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnRegister")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("android:id/button1")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBarLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)




#def main():

if __name__ == '__main__':
    main()
