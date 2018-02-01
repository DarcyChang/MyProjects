from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.wifi_binding

def android_home(self):
    self.driver.press_keycode(3) # press home key
    sleep(3)


def android_back(self):
    self.driver.press_keycode(4) # press back(return)
    sleep(3)


def android_power(self):
    self.driver.press_keycode(26) # press power
    sleep(3)


def android_hide_keyboard(self): 
    self.driver.hide_keyboard()
    sleep(1)


def android_lock_screen(self):
    self.driver.lock(5)
    sleep(1)


#  connect, OK
def android_connect_wifi_btn(self):
    el = self.driver.find_element_by_id("android:id/button1")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def android_cancel_btn(self):
    try:
        WebDriverWait(self.driver, 60, 1).until(lambda driver: self.driver.find_element_by_id("android:id/button2"))
        self.driver.find_element_by_id("android:id/button2").click()
    except:
        pass
    sleep(1)


def android_clear_btn(self):
    el = self.driver.find_element_by_id("android:id/button3")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def android_change_wifi_btn(self):
    el = self.driver.find_element_by_id("com.android.settings:id/decision_dialog_wifi")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def android_change_wifi_network(self, ssid):
    self.driver.start_activity("com.android.settings", "com.android.settings.wifi.WifiSettings")
    activity = self.driver.current_activity
    if ".wifi.WifiSettings" in activity:
        android.wifi_binding.wifi_connect_sprinkler(self, ssid)
    else:
        print("[Gemtek] Can not locate com.android.settings.wifi.WifiSettings")


if __name__ == '__main__':
    print("android_btn.py")
