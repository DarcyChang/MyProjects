import os
from time import sleep
from appium import webdriver


def is_app_installed(self):
    print("[Gemtek] Check APP is installed or not?")
    el = self.driver.is_app_installed("com.blackloud.wetti")
    self.assertTrue(el)


def install_app(self, version):
    print("[Gemtek] Install APP")
    apk_path = str(os.path.abspath("..")) + "/build/outputs/apk/"
    for subdir, dirs, files in os.walk(apk_path): 
        for file in files:
            if version in file:
                apk_name = str(file)
    print("[Gemtek] current path = " + str(os.getcwd()))
    path = apk_path + apk_name
    print("[Gemtek] apk file path = " + path)
    self.driver.install_app(path)
 

def remove_app(self):
    print("[Gemtek] Remove APP")
    self.driver.remove_app("com.blackloud.wetti")


def launch_app(self):
    print("[Gemtek] Launch APP")
    self.driver.launch_app()


def close_app(self):
    print("[Gemtek] Close APP")
    self.driver.close_app()
