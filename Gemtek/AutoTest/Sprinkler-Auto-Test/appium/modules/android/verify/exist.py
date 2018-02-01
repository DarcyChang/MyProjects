from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


# ===== Following function on main screen. =====
def verify_device_auto_watering(self, status):
    sleep(5)
    if status == "OFF":
        el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_text")
        self.assertIsNotNone(el)
        print("[Gemtek] " + el.text)
        try:
            tmp = "Blackloud Sprinkler is OFF."
            self.assertEqual(tmp, el.text)
        except:
            tmp = "Based on State watering laws, the sprinkler will ban watering"
            self.assertIn(tmp, el.text)
    sleep(1)
    

def verify_device_weather_assistant(self, status):
    sleep(5)
    if status == "ON":
        el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_text")
        self.assertIsNotNone(el)
        print("[Gemtek] " + el.text)
        tmp = "Based on State watering laws, the sprinkler will ban watering"
        self.assertIn(tmp, el.text)
    else:
        try:
            el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_text")
            tmp = "Blackloud Sprinkler is OFF."
            self.assertEqual(tmp, el.text) 
        except NoSuchElementException:
            pass
    sleep(1)


# ===== Following function on setting page. =====
def verify_system_date_and_time(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/device_time")
    self.assertIsNotNone(el)
    print("[Gemtek] system time : " + el.text)
#    self.assertEqual(device_name, el.text) 
    sleep(1)


# ===== Following function on dashboard page. =====
def verify_schedule_without_pause(self):
    try:
        el = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_pause")
        self.assertIsNone(el)
    except:
        pass
    sleep(1)


# ===== Following function on manual watering page. =====
def verify_manual_watering_page(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/activity_manual_watering")
    self.assertIsNotNone(el)
    sleep(1)


def verify_watering_zone(self, zone):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_zone")
    print("[Gemtek] " + el.text + " is watering now.")
    self.assertIn(str(zone), el.text)
    sleep(1)


def verify_watering_image(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_image")
    self.assertIsNotNone(el)
    sleep(1)


def verify_countdown(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_time")
    self.assertIsNotNone(el)
    print("[Gemtek] countdown = " + el.text + " minutes.")
    sleep(1)


def verify_skip(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_skip")
    self.assertIsNotNone(el)
    sleep(1)
