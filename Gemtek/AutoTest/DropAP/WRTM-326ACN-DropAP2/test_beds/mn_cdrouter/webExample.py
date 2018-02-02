__author__ = 'bmelhus'

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()

driver.set_window_size(1024, 768)
driver.get('http://min-cmdctr.calix.local/login')

time.sleep(5)
uname = driver.find_element_by_xpath('//input[@name="userName"]')
uname.send_keys('theWiz@ybr.com')
uname = driver.find_element_by_xpath('//input[@name="password"]')
uname.send_keys('T0t0too8791')
login_btn = driver.find_element_by_xpath('//input[@value="Login"]')
login_btn.send_keys(Keys.ENTER)

time.sleep(5)
driver.get('http://min-cmdctr.calix.local/netop-workflows/wizard')