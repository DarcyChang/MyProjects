from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# next
def right_on_top_bar(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBarRight")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


# back
def left_on_top_bar(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/tvBarLeft")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def cancel_on_top_bar(self, btn_name):
    if btn_name in "tvCancel":
        _check_next(self)
    elif btn_name in "settingCancel":
        _settingcancel(self)


def _tvcancel(self):
    WebDriverWait(self.driver, 5, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/tvCancel"))
    self.driver.find_element_by_id("com.blackloud.wetti:id/tvCancel").click()
    sleep(1)


def _settingcancel(self):
    WebDriverWait(self.driver, 5, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/settingCancel"))
    self.driver.find_element_by_id("com.blackloud.wetti:id/settingCancel").click()
    sleep(1)


def slide_left2right(self, start_x=50, start_y=800, end_x=600, end_y=800, duration=500):
#    self.driver.swipe(50, 800, 600, 800, 500)
    self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    sleep(1)


def slide_right2left(self, start_x=600, start_y=800, end_x=50, end_y=800, duration=500):
#    self.driver.swipe(600, 800, 50, 800, 500)
    self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    sleep(1)


def slide_up2down(self, start_x=400, start_y=400, end_x=400, end_y=800, duration=500):
#    self.driver.swipe(400, 400, 400, 800, 500)
    self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    sleep(1)


def slide_down2up(self, start_x=400, start_y=800, end_x=400, end_y=400, duration=500):
#    self.driver.swipe(400, 800, 400, 400, 500)
    self.driver.swipe(start_x, start_y, end_x, end_y, duration)
    sleep(1)


def _check_next(self):
    WebDriverWait(self.driver, 60, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/check_next"))
    self.assertIsNotNone(self.driver.find_element_by_id("com.blackloud.wetti:id/check_next")) 
    self.driver.find_element_by_id("com.blackloud.wetti:id/check_next").click()
    sleep(1)


def _tvok(self):
    WebDriverWait(self.driver, 60, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/tvOk"))
    self.assertIsNotNone(self.driver.find_element_by_id("com.blackloud.wetti:id/tvOk")) 
    self.driver.find_element_by_id("com.blackloud.wetti:id/tvOk").click()
    sleep(1)


def _setnextbtn(self):
    WebDriverWait(self.driver, 60, 1).until(lambda driver: self.driver.find_element_by_id("com.blackloud.wetti:id/setNextBtn"))
    self.assertIsNotNone(self.driver.find_element_by_id("com.blackloud.wetti:id/setNextBtn")) 
    self.driver.find_element_by_id("com.blackloud.wetti:id/setNextBtn").click()
    sleep(1)


def next_btn_on_bottom(self, btn_name):
    if btn_name in "check_next":
        _check_next(self)
    elif btn_name in "tvOk":
        _tvok(self)
    elif btn_name in "setNextBtn":
        _setnextbtn(self)


def ok_btn_on_bottom(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/completeBtn")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def back_btn_on_bottom(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/setBackBtn")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


def Rescan(self):
    el = self.driver.find_element_by_id("com.blackloud.wetti:id/btnRescan")
    self.assertIsNotNone(el)
    el.click()
    sleep(1)


if __name__ == '__main__':
    print("common_btn.py")
