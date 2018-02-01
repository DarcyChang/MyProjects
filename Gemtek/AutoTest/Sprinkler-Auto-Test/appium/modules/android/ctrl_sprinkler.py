from time import sleep
from appium import webdriver


def add_sprinkler(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/ivAddSprinkler") # add sprinkler
    self.assertIsNotNone(el)
    el.click()
    sleep(1) 


def account_setting(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imvAbLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(2)


def choose_sprinkler(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/ivThum")
    # "com.blackloud.wetti:id/tvName" is too.
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    # TODO : There are four point can touch that choose sprinkler function.
    #       two are recourse-id, another are class.
    #       Maybe we can do it by random.
