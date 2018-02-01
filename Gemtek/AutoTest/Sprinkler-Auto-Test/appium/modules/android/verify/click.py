from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.android_btn


# ===== Following function on dashboard page. =====
# If auto watering status is "OFF", then rain delay days can not be clickable(enabled = False).
def verify_rain_delay_days_click(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/rain_delay_layout")
    self.assertIsNotNone(el)
    print("[Gemtek] Rain delay days clickable : " + str(el.is_enabled()))
    self.assertTrue(el.is_enabled()) 
