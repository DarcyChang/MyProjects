from time import sleep
from appium import webdriver
import appium
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn


def return2ctrl_sprinkler(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgBarLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def settings(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgBarRight")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
