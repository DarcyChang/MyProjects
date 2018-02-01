import unittest
from time import sleep
from appium import webdriver
import android.common_btn


def slide_welcome_frame(self):
    sleep(1)
    android.common_btn.slide_right2left(self)
    android.common_btn.slide_right2left(self)
    android.common_btn.slide_right2left(self)
    android.common_btn.slide_right2left(self)
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnExitAppTour") 
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


#def main():

if __name__ == '__main__':
    print("[Gemtek] welcome.py")
#    main()
