import unittest
from time import sleep
from appium import webdriver


def forgot_password(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnFogotPass") # Forgot Password
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnSubmit") # Submit
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    el = self.driver.find_element_by_id("android:id/button1")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    email_text = self.driver.find_element_by_id("com.blackloud.wetti:id/etEmail") # E-mail
    self.assertIsNotNone(email_text)
    email_text.send_keys("freeman720916@yahoo.com.tw")
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnSubmit") # Submit
    self.assertIsNotNone(el)
    el.click()
    sleep(10)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvOk")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def sign_in(self, user, pswd):
    username_text = self.driver.find_element_by_id("com.blackloud.wetti:id/etUserName")
    self.assertIsNotNone(username_text)
    username_text.clear()
    username_text.send_keys(user)
    sleep(1)
    passward_text = self.driver.find_element_by_id("com.blackloud.wetti:id/etPass")
    self.assertIsNotNone(passward_text)
    passward_text.send_keys(pswd)
    sleep(1)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnSignin")
    self.assertTrue(el)
    self.assertIsNotNone(el)
    el.click()
    sleep(10)


def sign_out(self):	
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvLogout")
    self.assertIsNotNone(el)
    el.click()
    sleep(2)


if __name__ == '__main__':
    print("login.py")
