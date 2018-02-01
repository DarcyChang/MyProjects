from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn
import android.android_btn


def _get_zone_element_index(self, num):
    zone_num = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonName")
    for i in range(len(zone_num)):
#        print("[Gemtek] round : " + str(i))
#        print("[Gemtek] " + zone_num[i].text)
        if(num in zone_num[i].text):
#            print("[Gemtek] round : " + str(i))
            return i  
    print("[Gemtek] Not found Zone" + num)
    print(zone_num.index(zone_num))


def zone_time(self, num):
    index = _get_zone_element_index(self, str(num))
    zone_time = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonTime")
    print("[Gemtek] Zone" + str(num) + " time = " + zone_time[index].text)
    sleep(1)


def launch_watering(self, num):
    index = _get_zone_element_index(self, str(num))
    launch = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonIcon")
    self.assertIsNotNone(launch)
    launch[index].click()
    sleep(1)


def watering_time(self, num, set_time):
    if(set_time < 0 or set_time > 30):
        print("[Gemtek] Your set time must durning 0 to 30.")
        return

    index = _get_zone_element_index(self, str(num))
    now_time = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonCountText")

    if(set_time >= int(now_time[index].text[0:1])):
        diff = set_time - int(now_time[index].text[0:1])
        print("[Gemtek] Click plus " + str(diff) + " times")
        plus = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonCountPlus")
        for i in range(diff):
            plus[index].click()
    else:
        diff = int(now_time[index].text[0:1]) - set_time
        print("[Gemtek] Click sub " + str(diff) + " times")
        sub = self.driver.find_element_by_id("com.blackloud.wetti:id/zoneList").find_elements_by_id("com.blackloud.wetti:id/zoonCountLess")
        for i in range(diff):
            sub[index].click()


def slide_down2up(self):
    android.common_btn.slide_down2up(self, 360, 1250, 360, 180)


def slide_up2down(self):
    android.common_btn.slide_down2up(self, 360, 180, 360, 1250)


def watering_zone(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_zone")
    print("[Gemtek] " + el.text + " is watering now.")
    sleep(1)


def countdown(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_time")
    print("[Gemtek] countdown = " + el.text + " minutes.")
    sleep(1)


#def start_schedule(self):
def water_multiple_zones(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/run_schedule")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def stop(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_stop")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    

def skip(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/counting_skip")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def ok(self, time):
    WebDriverWait(self.driver, int(time), 1).until(lambda driver: self.driver.find_element_by_id("android:id/button1"))
    self.assertIsNotNone(self.driver.find_element_by_id("android:id/button1")) 
    self.driver.find_element_by_id("android:id/button1").click()
    sleep(1)


def back(self):
    android.common_btn.left_on_top_bar(self)
