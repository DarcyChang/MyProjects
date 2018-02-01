from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn


def zip_code(self): 
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zipCodeText")
#    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zipCodeSetting")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    # TODO : There are four point can touch that trigger ZIP Code function.
    #       One is recourse-id, another are class.


def enter_zip_code(self, zip_code):
    zip_code_text = self.driver.find_element_by_id("com.blackloud.wetti:id/autoCompleteView")
    print("[Gemtek] Keyin ZIP Code : "+str(zip_code))
    sleep(1)
    zip_code_text.clear()
    sleep(1)
    zip_code_text.send_keys(str(zip_code))
    sleep(1)
    android.android_btn.android_hide_keyboard(self) 
    sleep(1)


def choose_zip_code(self, num):
    el = self.driver.find_elements_by_id("com.blackloud.wetti:id/tvResult")
    self.assertIsNotNone(el)
    for i in range(len(el)):
        print("[Gemtek] zip code " + str(i) + " = " + el[i].text)
        if(str(num) == el[i].text[0:5]):
            print("[Gemtek] click zip code " + str(i) + " = " + el[i].text[0:5])
            el[i].click()
            sleep(1)
            return
    # TODO : Choose another zip code on slide to bottom
    #       Maybe we can do it by random.


def cancel(self):
    android.common_btn.cancel_on_top_bar(self, "tvCancel")
