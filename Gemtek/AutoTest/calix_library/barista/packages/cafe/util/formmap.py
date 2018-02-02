# coding=utf-8
__author__ = 'kelvin & James'

from cafe.sessions.session_manager import get_session_manager
from cafe.core.utils import Param, ParamAttributeError
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import selenium, sys
from string import Template
from cafe.core.signals import FORMMAP_SESSION_ERROR, FORMMAP_ELEMENT_ERROR
from cafe.core.logger import CLogger as Logger

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning

ERROR_NOT_VISIBLE = "Element is not present!"
ERROR_NO_ALERT_PRESENT = "No alert is present!"

class FormapSessionException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=FORMMAP_SESSION_ERROR)

class FormapElementException(Exception):
    def __init__(self, msg=""):
        _module_logger.exception(msg, signal=FORMMAP_ELEMENT_ERROR)

class _FormMap(Param):
    """
    the class is based on selenium and used for web test.
    """
    def __init__(self, d={}):
        """
        class init
        """
        super(FormMap, self).__init__(d)

    def set_gui_session(self, session):
        """
        set formmap gui session to the webgui session generated from session_mgr

        Args:
            session: webgui session
        return:
            None
        """
        print("#################Set session##################")
        self.session = session
        self.driver = session.driver

    def open_gui_session(self, session_name, host='localhost', port=15995):
        """
        open web gui session.

        Args:
            session_name: session name
            host: session server location, default value is 'localhost'.
            port: session server port, default value is 15995.

        return:
            None
        sample:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
        """
        print("#################Open session##################")
        try:
            self.session_mgr = get_session_manager(host, port)
            self.session = self.session_mgr.create_session(session_name, "webgui")
            self.driver = self.session.driver

            return 0
        except Exception as e:
            raise FormapSessionException("Failed to open session, reason:%s" % e)
    # def open_browser(self, browser="Firefox", chrome_driver_path=""):
    #     """
    #     Open browser for test
    #
    #     Args:
    #         browser: browser type, we are now support firefox only.
    #     return:
    #         None
    #
    #     sample:
    #         >>> t.FormMap
    #         >>> t.open_browser()
    #         or
    #         >>> t.open_browser(browser="Firefox")
    #     """
    #     if browser.lower() == "firefox":
    #         self.driver = webdriver.Firefox()
    #         self.driver.implicitly_wait(30)
    #         print "Browser title is :", self.driver.title
    #     elif browser.lower() == "chrome":
    #         print("Not support yet")
    #     elif browser.lower() == "ie":
    #         print("Not support yet")

    def get_url(self, browser_url):
        """
        get URL source

        Args:
            browser_url: URL which you want to access.
        return:
            None
        sample:
            >>> t.FormMap
            >>> t.open_browser()
            >>> t.get_url("http://www.python.org")
        """
        try:
            if isinstance(browser_url, str):
                self.url = browser_url
                print ">>> Opening url %s ......" % self.url
                self.driver.get(self.url)
                return 0
            else:
                raise Exception("'URL %s is invalid , URL should be a string!" % browser_url)
        except Exception as e:
            raise Exception("Failed to get: %s, Reason: %s" % (browser_url, e))

    def get_method(self, *args, **kwargs):
        """
        Get the method from loaded json file.

        Args:
            args: args should be list.
        return:
            method, it should be a string, i.g. xpath, element id...
        sample:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('main_page', 'search_field')
            >>> print "by = %s, content = %s" % (by, content)
                by = "xpath", content = "//*[@id=\"content\"]/ul/li[5]/a"
        """
        try:
            i = self["formmap"]
        except:
            raise Exception("key 'formmap' is not found")
        for name in args:
            if name in i:
                i = i[name]
            else:
                raise Exception("key cannot be find in form map object (%s)" % str(args))

        content = Template(i['content']).safe_substitute(kwargs)
        return i['by'], content

    def wait_element(self, xpath, secs):
        """
        Waiting for an element to display.

        Args:
            xpath: Xpath
            secs: Time(seconds)
        return:
            None
        """
        for i in range(secs):
            try:
                el = self.driver.find_element_by_xpath(xpath).is_displayed()
                if el:
                    return True
            except:
                pass
            sleep(1)
        raise Exception("Error: Time out, element is not displayed.")

    def _get_element(self, search_mode, method, wait_element=3):
        """
        Get the web element by provided method.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
        return:
            web element obj.
        """
        try:
            retry = 3
            while retry:
                if search_mode == "xpath":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_xpath(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue
                elif search_mode == "name":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_name(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "class_name":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_class_name(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "css_selector":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_css_selector(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "id":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_id(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "link_text":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_link_text(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "tag_name":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_tag_name(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue

                elif search_mode == "partial_link_text":
                    sleep(wait_element)
                    ele = self.driver.find_element_by_partial_link_text(method)
                    if ele.is_displayed():
                        return ele
                    else:
                        retry -= 1
                        continue
                else:
                    raise Exception(
                        "Invalid mode!, mode should be one of 'xpath, name, class_name, css_selector, id, link_text, tag_name, partial_link_text'")
            raise FormapElementException(ERROR_NOT_VISIBLE)
        except Exception as e:
            raise Exception("ERROR: %s" % e)

    get_element = _get_element

    def click(self, search_mode, method, wait_element=3):
        """
        Clicks the element. like button, drop down list, checkbox, radio and so on.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
        return:
            None
        example:
            >>> t.FormMap
            >>> t.open_browser()
            >>> t.get_url("http://www.python.org")
            >>> field = v.get_method("main_page", "text_field","search_field_xpath")
            >>> t.set_text("xpath",field,"selenium")
            >>> sleep(2)
            >>> buttons = v.get_method("main_page","button","go_xpath")
            >>> t.click("xpath",buttons)
            >>> sleep(3)
            >>> t.close_browser()
        """
        try:
            print(">>> Click element: [%s = {%s}]" % (search_mode, method))
            ele = self._get_element(search_mode, method, wait_element)
            ele.click()
        except Exception as err:
            raise FormapElementException("Failed to click element: [%s = {%s}], Reason: %s" % (search_mode, method, err))

    def set_text(self, search_mode, method, value, wait_element=3):
        """
        Simulates typing into the element.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
            value: The value which you want to type to element.
        return:
            None
        example:
            >>> t.FormMap
            >>> t.open_browser()
            >>> t.get_url("http://www.python.org")
            >>> x, y = v.get_method("main_page", "text_field","search_field_xpath")
            >>> t.set_text(x, y,"selenium")
            >>> sleep(2)
            >>> t.close_browser()
        """
        try:
            print (">>> Set text to element: [%s = %s]" % (search_mode, method))
            ele = self._get_element(search_mode, method, wait_element)
            ele.send_keys(value)
        except Exception as err:
            raise FormapElementException("Failed to set text to element: [%s = %s], Reason: %s" % (search_mode, method,err))

    def get_text(self, search_mode, method, wait_element=3):
        """
        Get the text of the element.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
        return:
            return the text from element.
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('main_page', 'search_field')
            >>> v.get_text(by, content)
        """
        print(">>> Get text from element: [%s = %s]" % (search_mode, method))
        ele = self._get_element(search_mode, method, wait_element)
        #print(ele)
        if ele.is_displayed():
            return ele.text
        else:
            raise FormapElementException(ERROR_NOT_VISIBLE)

    def get_attribute(self, search_mode, method, name, wait_element=3):
        """
        Gets the given attribute or property of the element.
        This method will first try to return the value of a property with the given name. If a property with that name
        doesn't exist, it returns the value of the attribute with the same name. If there’s no attribute with that name,
        None is returned.
        Values which are considered truthy, that is equals “true” or “false”, are returned as booleans. All other
        non-None values are returned as strings. For attributes or properties which do not exist, None is returned.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
            name: Name of the attribute/property to retrieve.
        return:
            None or Value of attribute/property.
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('main_page', 'search_field')
            >>> v.get_attribute(by, content, 'selenium')
        """
        try:
            print(">>> Get attrubute from element: [%s = %s]" % (search_mode, method))
            ele = self._get_element(search_mode, method, wait_element)
            return ele.get_attribute(name)
        except Exception as err:
            raise FormapElementException("Failed to get attrubute of element: [%s = %s]!, Reason: %s" % (search_mode, method, err))

    def clear_text(self, search_mode, method, wait_element=3):
        """
        Clears the text if it’s a text entry element.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('main_page', 'search_field')
            >>> v.clear_text(by, content, 'selenium')

        """
        try:
            print(">>> Clear text from element: [%s = %s]" % (search_mode, method))
            ele = self._get_element(search_mode, method, wait_element)
            ele.clear()
        except Exception as err:
            raise FormapElementException("Failed to clear text from element: [%s = %s]!, Reason: %s" % (search_mode, method, err))

    def submit_element(self, search_mode, method, wait_element=3):
        """
        Submits a form.

        Args:
            search_mode: a method name to find element, like id, xpath, name ...
            method: a method to find element, i.g. search_mode is xpath mode, then method should be a xpath. like "//*[@id='submit']".
        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('main_page', 'search_field')
            >>> v.submit_element(by, content, 'selenium')
        """
        try:
            print(">>> Submit element: [%s = %s]" % (search_mode, method))
            ele = self._get_element(search_mode, method, wait_element)
            ele.submit()
        except Exception as err:
            raise FormapElementException("Failed to submit element: [%s = %s]!, Reason: %s" % (search_mode, method, err))

    def back(self):
        """
        Goes one step backward in the browser history.

        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('page', 'link')
            >>> v.click(by, content)
            >>> v.back()

        """
        print ">>> Page back..."
        try:
            self.driver.back()
        except Exception as err:
            raise FormapElementException("Page back failed!, Reason: %s", err)

    def forward(self):
        """
        Goes one step forward in the browser history.

        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url('http://www.python.org')
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method('page', 'link')
            >>> v.click(by, content)
            >>> v.back()
            >>> v.forward()
        """
        print(">>> Page forward...")
        try:
            self.driver.forward()
        except Exception as err:
            raise FormapElementException("Failed to do page forward! Reason : %s" % err)

    def download(self):
        pass

    def upload(self):
        pass

    def switch_to_frame(self, frame):
        """
        Deprecated use driver.switch_to.frame

        Args:
            frame: specify the web frame which you want to switch to.
        return:
            None
        """
        self.driver.switch_to_frame(frame)

    def switch_to_frame_out(self):
        '''
        Returns the current form machine form at the next higher level.
        Corresponding relationship with switch_to_frame () method.

        return:
            None
        '''
        self.driver._switch_to.default_content()

    def swich_to_active_window(self):
        """
        Deprecated use driver.switch_to.window.

        return:
            None
        """
        self.driver.switch_to_alert()

    def _is_alert_present(self):
        """
        Internal methid, verify if alert is present.

        return:
            True or False

        """
        try:
            self.driver.switch_to_alert
        except:
            return False
        return True

    def accept_alert(self):
        '''
        accept warning box.

        return:
            Mone
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url("http://the-internet.herokuapp.com/")
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method("test_main_page", "java_script_alert")
            >>> v.click(by, content)
            >>> by, content = v.get_method("java_script_alert_page", "alert1")
            >>> v.click(by, content)  #check by xpath
            >>> print v.get_alert_text()
            >>> v.accept_alert()
        '''
        print(">>> Accept alert box.")
        try:
            self.driver.switch_to.alert.accept()
        except:
            raise FormapElementException("Failed to accept alert box!")

    def dismiss_alert(self):
        '''
        Dismisses the alert available.

        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url("http://the-internet.herokuapp.com/")
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method("test_main_page", "java_script_alert")
            >>> v.click(by, content)
            >>> by, content = v.get_method("java_script_alert_page", "alert1")
            >>> v.click(by, content)  #check by xpath
            >>> print v.get_alert_text()
            >>> v.dismiss_alert()
        '''
        try:
            print(">>> Dismiss alert box.")
            if self._is_alert_present():
                self.driver.switch_to.alert.dismiss()
        except Exception as err:
            raise FormapElementException("There is no alert box present! Reanson: %s" % err)

    def alert_authenticate(self, username, password):
        """
        Send the username / password to an Authenticated dialog (like with Basic HTTP Auth). Implicitly ‘clicks
ok.

        Args:
            username: username for authenticate
            password: password for authenticate
        return:
            None
        example:
            >>> v = FormMap()
            >>> v.open_gui_session("session1")
            >>> v.get_url("http://the-internet.herokuapp.com/")
            >>> v.load("~/repo/calix/src/demo/james_demo/Selenium_/formmap0.json")
            >>> by, content = v.get_method("test_main_page", "java_script_alert")
            >>> v.click(by, content)
            >>> by, content = v.get_method("java_script_alert_page", "alert1")
            >>> v.click(by, content)  #check by xpath
            >>> print v.get_alert_text()
            >>> v.alert_authenticate("admin", "password")
        """
        print(">>> Alert authenticating...")
        try:
            if self._is_alert_present():
                self.driver.switch_to.alert.authenticate(username, password)
        except Exception as err:
            raise FormapElementException("Alert box authenticate failed! Reanson: %s" % err)

    def set_alert_text(self, text):
        """
        Send Keys to the Alert.

        Args:
            text: text that you want to set to alert.
        return:
            None
        example:

        """
        print(">>> set %s to alert box." % text)
        try:
            if self._is_alert_present():
                self.driver.switch_to.alert.send_keys(text)
        except Exception as err:
            raise FormapElementException("Failed to set text to alert box! Reason: %s" % err)

    def get_alert_text(self):
        """
        Gets the text of the Alert.

        return:
            text content from a alert.
        """
        print(">>> Get alert box text.")
        try:
            if self._is_alert_present():
                return self.driver.switch_to.alert.text
        except Exception as err:
            raise Exception("Failed to get text from alert box! Reason: %s" % err)

    def exec_java_script(self, java_script):
        """
        Execute JavaScript scripts.

        Args:
            java_script:
        return:
            None
        example:
            >>> t.exec_java_script("window.scrollTo(200,1000);")
        """
        print(">>> Executing Java script %s." % java_script)
        try:
            self.driver.execute_script(java_script)
        except Exception as err:
            raise FormapElementException("Failed to execute Java script! Reason: %s" % err)

    def refresh(self):
        """
        refresh web page.

        return:
            None
        """
        print(">>> Page refresh.")
        try:
            self.driver.refresh()
        except Exception as err:
            raise FormapElementException("Failed to refresh page! Reason: %s" % err)

    def get_current_url(self):
        """
        Get the URL address of current page.

        return:
            crrent page URL.
        """
        print(">>> Get current URL.")
        try:
            return self.driver.current_url
        except Exception as err:
            raise FormapElementException("Failed to get current URL! Reason: %s" % err)

    def get_screenshot(self, file_name):
        """
        Get the current window screenshot.

        Args:
            file_name:
        return:
            None
        """
        print(">>> Get web page screenshot as file %s." % file_name)
        try:
            self.driver.get_screenshot_as_file(file_name)
        except Exception as err:
            raise FormapElementException("Failed to get screenshot! Reason: %s" % err)

    def close_browser(self):
        """
        Quits the driver and close every associated window.

        return:
            None
        """
        try:
            self.driver.quit()
        except Exception as err:
            raise FormapElementException("Failed to close browser! Reason: %s" % err)
        print("#################Browser Closed##################")

    def close_session(self, session_name):
        """
        close webgui session by session name.

        Args:
            session_name: session name.

        return:
            None
        """
        try:
            self.session_mgr.remove_session(session_name)
            print("#################session Closed##################")
            return 0
        except Exception as err:
            raise FormapSessionException("Failed to close session %s, Reason: %s" % (session_name, err))

FormMap = _FormMap

if __name__ == "__main__":
    v = FormMap()

    try:
        v.open_gui_session("session1", port=15556)
        v.get_url('http://www.python.org')
        v.load("~/repo/calix/src/demo/james_demo/selenium_/formmap0.json")

        by, content = v.get_method('main_page', 'search_field')
        v.set_text(by, content, 'selenium')

        by, content = v.get_method('main_page', 'search_button')
        v.click(by, content)

        sleep(3)
        v.back()
        sleep(3)
    finally:
        v.close_session('session1')
