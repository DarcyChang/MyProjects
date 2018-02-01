from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import android.common_btn


def set_schedule(self, schedule_num):
    recourseid = "com.blackloud.wetti:id/schedule"+str(schedule_num)+"Time"
    print("[Gemtek] schedule time recourse id "+recourseid)
    el = self.driver.find_element_by_id(recourseid)
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def hour(self, target):
    if target <= 0:
        print("[Gemtek] You enter a wrong number, number range must in 0 to 12")
        return

    print("[Gemtek] setting target hour = " + str(target))
    hour_text = self.driver.find_element_by_id("com.blackloud.wetti:id/leftWheelView").find_elements_by_id("com.blackloud.wetti:id/tv_label_item_wheel")
    self.assertIsNotNone(hour_text)
#    print("[Gemtek] set hour = " + hour_text[2].text)
    diff = abs(int(target) - int(hour_text[2].text))
    up_num = abs(int(target) - int(hour_text[1].text))
    down_num = abs(int(target) - int(hour_text[3].text))
#    print("[Gemtek] diff = " + str(diff) + " up_num = " + str(up_num) + " down_num = " + str(down_num))

    if(diff == 0):
        pass
    elif down_num <= up_num:
        for i in range(0, down_num+1):
            android.common_btn.slide_down2up(self, 120, 760, 120, 700)
            sleep(0.5)
    elif up_num < down_num:
        for i in range(0, up_num+1):
            android.common_btn.slide_up2down(self, 120, 630, 120, 700)
            sleep(0.5)


def minute(self, target):
    if target < 0 or target > 59:
        print("[Gemtek] You enter a wrong number, number range must in 0 to 59")
        return

    print("[Gemtek] setting target minute = " + str(target))
    minute_text = self.driver.find_element_by_id("com.blackloud.wetti:id/centerWheelView").find_elements_by_id("com.blackloud.wetti:id/tv_label_item_wheel")
    self.assertIsNotNone(minute_text)
#    print("[Gemtek] set minute = " + minute_text[2].text)
    diff = abs(int(target) - int(minute_text[2].text))
    up_num = abs(int(target) - int(minute_text[1].text))
    down_num = abs(int(target) - int(minute_text[3].text))
#    print("[Gemtek] diff = " + str(diff) + " up_num = " + str(up_num) + " down_num = " + str(down_num))

    if(diff == 0):
        pass
    elif down_num <= up_num:
        for i in range(0, down_num+1):
            android.common_btn.slide_down2up(self, 360, 760, 360, 700)
            sleep(0.5)
    elif up_num < down_num:
        for i in range(0, up_num+1):
            android.common_btn.slide_up2down(self, 360, 630, 360, 700)
            sleep(0.5)


def time_system(self, target):
    if target not in 'AM' and target not in 'PM':
        print("[Gemtek] You enter a wrong word, must be AM or PM.")
        return

    print("[Gemtek] setting time system = " + str(target))
    time_text = self.driver.find_element_by_id("com.blackloud.wetti:id/rightWheelView").find_elements_by_id("com.blackloud.wetti:id/tv_label_item_wheel")
    self.assertIsNotNone(time_text)
#    print("[Gemtek] set time system = " + time_text[2].text)

    if time_text[2].text != str(target):
        android.common_btn.slide_down2up(self, 600, 700, 600, 630)
        sleep(1)


def repeat_all(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgAll")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def repeat_su(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgSun")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def repeat_m(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgMon")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)

    
def repeat_tu(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgTue")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    
    
def repeat_w(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgWed")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
    
    
def repeat_th(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgThu")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def repeat_f(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgFri")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def repeat_sa(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/imgSat")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def _get_zone_element_index(self, num):
    zone_num = self.driver.find_element_by_id("com.blackloud.wetti:id/zoonLayout").find_elements_by_id("com.blackloud.wetti:id/zoneName")
    for i in range(len(zone_num)):
#        print("[Gemtek] round : " + str(i))
#        print("[Gemtek] " + zone_num[i].text)
        if(num in zone_num[i].text):
#            print("[Gemtek] round : " + str(i))
            return i  
    print("[Gemtek] Not found Zone" + num)
    print(zone_num.index(zone_num))


def _enter_zone_name(self, name):
    zone_text = self.driver.find_element_by_class_name("android.widget.EditText")
    self.assertIsNotNone(zone_text)
    zone_text.clear()
    zone_text.send_keys(name)
    sleep(1)


def name_your_zone(self, num, name):
    index = _get_zone_element_index(self, str(num))
    zone_name = self.driver.find_element_by_id("com.blackloud.wetti:id/zoonLayout").find_elements_by_id("com.blackloud.wetti:id/zoneSubName")
    self.assertIsNotNone(zone_name)
    zone_name[index].click()
    _enter_zone_name(self, name)
    ok(self)
    print("[Gemtek] " + zone_name[index].text)
    sleep(1)


def watering_time(self, num, set_time):
    if(set_time < 1 or set_time > 30):
        print("[Gemtek] Your set time must durning 1 to 30.")
        return

    index = _get_zone_element_index(self, str(num))
    now_time = self.driver.find_element_by_id("com.blackloud.wetti:id/zoonLayout").find_elements_by_id("com.blackloud.wetti:id/zoneCountText")

    if(set_time >= int(now_time[index].text[0:1])):
        diff = set_time - int(now_time[index].text[0:1])
        print("[Gemtek] Click plus " + str(diff) + " times")
        plus = self.driver.find_element_by_id("com.blackloud.wetti:id/zoonLayout").find_elements_by_id("com.blackloud.wetti:id/zoneCountPlus")
        for i in range(diff):
            plus[index].click()
    else:
        diff = int(now_time[index].text[0:1]) - set_time
        print("[Gemtek] Click sub " + str(diff) + " times")
        sub = self.driver.find_element_by_id("com.blackloud.wetti:id/zoonLayout").find_elements_by_id("com.blackloud.wetti:id/zoneCountLess")
        for i in range(diff):
            sub[index].click()


def slide_down2up(self):
    android.common_btn.slide_down2up(self, 360, 1250, 360, 180)


def slide_up2down(self):
    android.common_btn.slide_down2up(self, 360, 180, 360, 1250)


def ok(self):
    android.android_btn.android_connect_wifi_btn(self)


def yes(self):
    android.android_btn.android_connect_wifi_btn(self)


def cancel(self):
    android.common_btn.left_on_top_bar(self)


def back(self):
    android.common_btn.left_on_top_bar(self)


def save(self):
    android.common_btn.right_on_top_bar(self)
    sleep(2)


def delete_schedule(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/remove_schedule")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)
