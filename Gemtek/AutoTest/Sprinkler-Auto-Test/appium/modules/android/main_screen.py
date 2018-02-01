import unittest
from time import sleep
from appium import webdriver
import android.verify.exist
import android.verify.next_page
from appium.webdriver.common.touch_action import TouchAction


def add_device(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/ivAddSprinkler")
    self.assertIsNotNone(el)
    el.click()
    sleep(1) 


def choose_device(self):
    # TODO timeout 30 seconds
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/ivThum")
    # "com.blackloud.wetti:id/tvName" is too.
    self.assertIsNotNone(el)
    action = TouchAction(self.driver)
    i = 1
    while(1):
        try:
            action.tap(el).perform()
#            el.click()
            sleep(1)
            try:
                android.verify.next_page.verify_binging_success(self)
            except:
                android.verify.next_page.verify_binging_network_success(self)
            break
        except:
            sleep(1)
            i += 1
            if(i == 30):
                print("[Gemtek] choose device TIME OUT !")
                break
    sleep(1)
    # TODO : 1. There are four point can touch that choose sprinkler function.
    #       two are recourse-id, another are class.
    #       Maybe we can do it by random.
    #       2. Binging two or more devices.


def my_account(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imvAbLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(2)


def buy_blackloud_sprinkler(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBuyNetti")
    self.assertIsNotNone(el)
    el.click()
    sleep(5)


def user_manual(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvUserManual")
    self.assertIsNotNone(el)
    el.click()
    sleep(5)


def feature_introduction(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvTourGuide")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def contact_us(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvContactUs")
    self.assertIsNotNone(el)
    el.click()
    sleep(5)


def about_blackloud(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvAbout")
    self.assertIsNotNone(el)
    el.click()
    sleep(5)


def legal_and_privacy_policy(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvUnderText")
    self.assertIsNotNone(el)
    el.click()
    sleep(5)


if __name__ == '__main__':
    print("[Gemtek] main_screen.py")
