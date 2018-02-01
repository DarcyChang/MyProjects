from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.android_btn


def return2main_screen(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgBarLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def settings(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgBarRight")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def _is_weather_assistant_on(self):
    assistant_text = self.driver.find_element_by_id("com.blackloud.wetti:id/weather_assistant_status")
    self.assertIsNotNone(assistant_text)
    return assistant_text.text


def weather_assistant(self, status):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/weather_assistant_layout")
    self.assertIsNotNone(el)
    now_status = _is_weather_assistant_on(self)
    if status != now_status:
        el.click()
        sleep(3)
        if status == "ON":
            android.android_btn.android_connect_wifi_btn(self)
            sleep(3)


def auto_watering(self, status):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/auto_watering_layout")
    self.assertIsNotNone(el)
    now_status = _is_auto_watering_on(self)
    if status != now_status:
        el.click()
    sleep(3)


def _is_auto_watering_on(self):
    auto_text = self.driver.find_element_by_id("com.blackloud.wetti:id/auto_watering_status")
    self.assertIsNotNone(auto_text)
    return auto_text.text


def rain_delay_days(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/rain_delay_layout")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def ok(self):
    android.android_btn.android_connect_wifi_btn(self)


def manual(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/manuel_button")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def weather_slide_rigth2left(self):
    android.common_btn.slide_right2left(self)


def weather_slide_left2right(self):
    android.common_btn.slide_left2right(self)


def schedule_next(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_next")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def schedule_previous(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_previous")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def schedule(self, schedule_num):
    schedule = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_name")
    self.assertIsNotNone(schedule)
    for i in range(2):
        if str(schedule_num) not in schedule.text:
            schedule_next(self)
            sleep(1)


def schedule_edit(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_setting")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def schedule_pause(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/schedule_pause")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def zone_slide_down2up(self):
    android.common_btn.slide_down2up(self, 360, 1250, 360, 300)


def zone_slide_up2down(self):
    android.common_btn.slide_down2up(self, 360, 180, 360, 1250)


def _get_zone_element_index(self, num):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_status").find_elements_by_class_name("android.widget.TextView")
    for i in range(len(el)):
#        print("index = " + str(i))
#        print(el[i].text)
        if(num in el[i].text):
            print("[Gemtek] Choose Zone" + str(num) + " index = " + str(i))
            return i


def zone(self, num):
    index = _get_zone_element_index(self, str(num))
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/zone_status").find_elements_by_class_name("android.widget.TextView")
    el[index].click()


if __name__ == '__main__':
    print("dashboard.py")
