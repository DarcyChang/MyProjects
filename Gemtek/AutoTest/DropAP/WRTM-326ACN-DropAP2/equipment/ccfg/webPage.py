__author__ = 'bmelhus'

import selenium
from selenium import webdriver
from cafe.core.logger import CLogger as Logger
from cafe.core.utils import create_folder

_module_logger = Logger(__name__)
debug = _module_logger.debug
error = _module_logger.error

class WebSession(object):

    def __init__(self, sid=None, browser="", default_element_wait=10, logfile=None):
        self.sid = sid
        #print(sid)

        #disable selenium logger
        self.session_log = Logger("selenium.webdriver.remote.remote_connection")
        self.session_log.console = False
        self.default_element_wait = default_element_wait
        self.logfile = logfile
        self.driver = self._get_driver(browser)
        #self.driver.implicitly_wait(default_element_wait)

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, f):
        if f is None:
            self.session_log.disable_file_logging()
            return
        if create_folder(f):
            debug("create folder for %s successful" % f)
        else:
            debug("create folder for %s failed" % f)
            return
        self._logfile = f
        self.session_log.enable_file_logging(log_file=f)

    def _get_driver(self, browser):
        b = str(browser).upper()
        if b == "FIREFOX":
            d = webdriver.Firefox()
            d.implicitly_wait(self.default_element_wait)
            return d
        else:
            #return webdriver.Firefox()
            d = webdriver.Firefox()
            d.implicitly_wait(self.default_element_wait)
            return d

    def close(self):
        try:
            self.driver.quit()
        except:
            pass
        #self.driver.close()

# if __name__ == "__main__":
#     from selenium.webdriver.common.keys import Keys
#     from cafe.core.logger import init_logging
#
#     init_logging()
#
#     session = WebGuiSession(sid="123", logfile="web.log")
#     print(session.driver.capabilities)
#
#     session.driver.get("http://www.python.org")
#
#     assert "Python" in session.driver.title
#     elem = session.driver.find_element_by_name("q")
#     elem.send_keys("pycon")
#     elem.send_keys(Keys.RETURN)
#     assert "No results found." not in session.driver.page_source
#     import time
#     time.sleep(5)
#     session.close()