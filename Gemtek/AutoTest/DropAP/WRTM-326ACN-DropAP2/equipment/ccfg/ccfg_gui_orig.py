__author__ = 'bmelhus'

from cafe.core.logger import CLogger as Logger
# from cafe.core.signals import E7_SESSION_ERROR
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from stp.equipment.ccfg.webPage import WebSession
# Imported to deal with wait for next page to load
from selenium.webdriver.support.expected_conditions import staleness_of
import contextlib
from selenium.common.exceptions import NoSuchElementException
import time
import cafe


logger = Logger(__name__)
debug = logger.debug
error = logger.error


# class ONTGuiException(Exception):
#     def __init__(self, msg=""):
#         logger.exception(msg, signal=E7_SESSION_ERROR)


class CCFGGuiApiClass(WebSession):
    """
    Class: ONTGuiApiClass is base class of ONTGUI.  This class is generic for now hoping all ONTs follow a consistent
           GUI model.  It is acceptable that not all ONTs will support all features and functionality.  It is up to
           the user to choose the methods that make sense for the ONT under test.

    """
    @contextlib.contextmanager
    def __wait_for_page_load(self, timeout=30):
        """
        Description:
            Experimental waiting for "new" page to be loaded.  Note this will not work for pages that do not
            change after a button like the apply button is clicked.
        Args:
            timeout(int): Timeout to wait for new page.
        Returns:
        """
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(staleness_of(old_page))

    # def is_element_present(self, how, what):
    #     """
    #     Description: Utility method to check presence of an element on page.
    #     Experimental stage
    #     Args:
    #
    #     Returns:
    #
    #     """
    #     try: self.driver.find_element(by=how, value=what)
    #     except NoSuchElementException, e:return False
    #     return True

    def __is_checkbox_selected(self, how, what):
        """
        Description: Utility method to determine if checkbox is checked.
        Args:
            how(str)(required):
            what(str)(required):
        Returns:
            Boolean: True if checked. False if unchecked. None if failure occurred.
        """
        try:
            element = self.driver.find_element(by=how, value=what)
            is_checkbox_checked = element.is_selected()
        except NoSuchElementException as exception:
            print("Exception: ", exception)
            return None
        return is_checkbox_checked

    def __click_element(self, how, what):
        """
        Description:
            Utility method to click on a page element.
        Args:
            how(str)(required):
            what(str)(required):
        Returns:
            Boolean: True if successful. False if not successful.
        """
        try:
            element = self.driver.find_element(by=how, value=what)
            element.click()
        except NoSuchElementException as exception:
            print("Exception: ", exception)
            return False
        # TODO: add in obtaining wait time from parameters - also add in random useage
        time.sleep(1)
        return True

    def __select_element_txt(self, how, what, txt):
        """
        Description:
            Utility method to select an page elements visible text.  Assumption is unqiue text elements in
            pulldown list.
        Args:
            how(str)(required):
            what(str)(required):
        Returns:
            Boolean: True if successful. False if not successful.
        """
        try:
            element = Select(self.driver.find_element(by=how, value=what))
            element.select_by_visible_text(txt)
        except NoSuchElementException as exception:
            print("Exception: ", exception)
            return False
        # TODO: add in obtaining wait time from parameters - also add in random usage
        time.sleep(1)
        return True

    def __enter_element_txt(self, how, what, txt):
        """
        Description:
            Utility method to write text to a text box.
        Args:
            how(str)(required): How to find the element on the page
            what(str)(required): What element to find on the page
            txt(str): Text to send
        Returns:
            Boolean: True if successful. False if not successful.
        """
        try:
            element = self.driver.find_element(by=how, value=what)
            element.clear()
            element.send_keys(txt)
        except NoSuchElementException as exception:
            print(exception)
            return False
        # TODO: add in obtaining wait time from parameters - also add in random usage
        time.sleep(1)
        return True

    def __enter_element(self, how, what):
        """
        Description:
            Utility method to click on a page element.
        Args:
            how(str)(required):
            what(str)(required):
        Returns:
            Boolean: True if successful. False if not successful.
        """
        try:
            element = self.driver.find_element_by_xpath('//input[@' + how + '="' + what + '"]')
            element.send_keys(Keys.ENTER)
        except NoSuchElementException as exception:
            print("Exception: ", exception)
            return False
        # TODO: add in obtaining wait time from parameters - also add in random useage
        time.sleep(1)
        return True

    # ##################################################################################################################
    # External single commands to class
    # ##################################################################################################################

    def login(self, ccfg_ip, username, password):
        """
        Description:
            Login into CCFG.
        Args:
            ccfg_ip: Domain Name of CCFG
            username(str): Username used to log into CCFG
            password(str): Password used to log into CCFG
        Returns:
            True if login is successful.
            An exception is raised if login fails.  Considered a critical failure.
        """
        # Goto login screen.
        self.driver.get("http://" + ccfg_ip + "/login")
        WebDriverWait(self.driver, 30)\
            .until(lambda s: s.find_element_by_xpath('//input[@value="Login"]'))
        # Enter username in text box
        self.__enter_element_txt(how="name", what="userName", txt=username)
        # Enter password in text box
        self.__enter_element_txt(how="name", what="password", txt=password)

        self.__enter_element(how="value", what="Login")

    def click_btn(self, ccfg_ip, ccfg_loc, ccfg_xpath, wait_xpath):
        """
        Description:
            Click vs. Enter button based on CCFG and target page
        Args:
            ccfg_ip = Domain Name of CCFG
            ccfg_loc = Page location of target
            ccfg_xpath = Location of button
            wait_xpath = Wait to execute based on page population
        Returns:
            True if login is successful.
            An exception is raised if login fails.  Considered a critical failure.
        """
        try:
            # Goto login screen.
            self.driver.get('http://' + ccfg_ip + '/' + ccfg_loc)
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_xpath(wait_xpath))
            # Click Collapse (expand or contract)
            #self.driver.find_element_by_xpath(ccfg_xpath).click()
            self.__click_element(how='xpath', what=ccfg_xpath)

        except:
            raise RuntimeError("Action was not performed for click_btn. CCFG=%s", ccfg_ip)
        return True

    def enter_btn(self, ccfg_ip, ccfg_loc, ccfg_xpath, wait_xpath):
        """
        Description:
            Enter vs Click button based on CCFG and target page
        Args:
            ccfg_ip = Domain Name of CCFG
            ccfg_loc = Page location of target
            ccfg_xpath = Location of button
            wait_xpath = Wait to execute based on page population
        Returns:
            True if login is successful.
            An exception is raised if login fails.  Considered a critical failure.
        """
        try:
            # Goto login screen.
            self.driver.get('http://' + ccfg_ip + '/' + ccfg_loc)
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_xpath(wait_xpath))
            # Click Collapse (expand or contract)
            #self.__enter_element(how="xpath", what=ccfg_xpath)
            enter_btn = self.driver.find_element_by_xpath(ccfg_xpath)
            enter_btn.send_keys(Keys.ENTER)

        except:
            raise RuntimeError("Action was not performed for enter_btn. CCFG=%s", ccfg_ip)
        return True

    def dld_cfg_file(self, ccfg_ip, cfg_file_page, wf_name_val, wf_desc_val, ont_type, wf_oper_val, cfg_file, wf_type, wf_exec_wndw_val):
        """
        Description:
            Create worflow and execute said workflow to download the golden config file
            to the 800GC/GH/E
        Args:
            ccfg_ip           =  Domain name of CCFG
            cfg_file_page     =  Workflow Start Page
            # Step 1:  Start
            wf_name_val       =  Workflow name
            wf_desc_val       =  Workflow description (optional)
            # Step 2:  Select Device Group(s)
            ont_type          =  Model: (800GC|800GH|800E) (Check Box)
            # Step 3:  Select Operation Parameters
            wf_oper_val       =  Options: Configuration File Download, Download SW/FW Image, Apply Configuration Profile
            cfg_file          =  Config file to download (Radio Button)
            # Step 4:  Select Schedule Parameters
            wf_type           =  Trigger (On Discovery|Time Scheduler)
            wf_exec_wndw_val  =  Time Window in minutes
        Returns:
            True if login is successful.
            An exception is raised if login fails.  Considered a critical failure.
        """
        # print(ccfg_ip)
        # print(cfg_file_page)
        # print(wf_name_val)
        # print(wf_desc_val)
        # print(wf_oper_val)
        # print(cfg_file)
        # print(wf_type)
        # print(wf_exec_wndw_val)
        try:
            #wf_page = cfg_file_page.split("/")[0]
            #file_delete = self.del_cfg_file(ccfg_ip, wf_page, wf_name_val)
            #page = "http://" + ccfg_ip + '/' + cfg_file_page
            #print(page)
            #self.driver.get(page)
            self.driver.get('http://' + ccfg_ip + '/' + cfg_file_page)
            #self.driver.get("http://min-cmdctr.calix.local/netop-workflows/wizard")
            #----------------------------------------------------------------------------------------------
            #  Start New Workflow by clicking New Workflow Button
            cfg_btn = "btn-netWorkflow"
            self.__click_element(how='id', what=cfg_btn)

            #----------------------------------------------------------------------------------------------
            #  Enter values
            #  1) Name of Operation
            #  2) Description of Operation
            #  3) Click Next
            # wf_name_val = "844E CFG DLD"
            # wf_desc_val = "DLD Config File for Testing"
            wf_name = "inputName"
            wf_desc = "inputDescription"
            wf_nxt_btn = '//a[contains(text(),"Next")]'
            self.__enter_element_txt(how="id", what=wf_name, txt=wf_name_val)
            self.__enter_element_txt(how="id", what=wf_desc, txt=wf_desc_val)
            self.__click_element(how="xpath", what=wf_nxt_btn)

            #----------------------------------------------------------------------------------------------
            #  Check box for EUT based on ont_type
            #  Note: Values must have been pre-configured
            #  //td[contains(text(),"844E")]/preceding-sibling::td/input[@type="checkbox"]
            # ont_type = "844E"
            ont_chk_box = '//td[contains(text(),"' + ont_type + '")]/preceding-sibling::td/input[@type="checkbox"]'
            self.__click_element(how='xpath', what=ont_chk_box)

            # Click Next Button (wf_nxt_btn)
            self.__click_element(how="xpath", what=wf_nxt_btn)

            #----------------------------------------------------------------------------------------------
            #  Click New Operation
            wf_new_oper_btn = '//button[@id="btn-newOperation"]'
            self.__click_element(how='xpath', what=wf_new_oper_btn)

            #----------------------------------------------------------------------------------------------
            #  Select Work Flow Operation
            #  Work Flow Operations:
            #  1) WorkFlowConfigFileDownload
            #  2) WorkFlowImageFileDownload
            #  3) WorkFlowProfile
            # wf_oper_val = "WorkFlowConfigFileDownload"
            # wf_oper = '//select[@id="inputOperationType"]'
            wf_oper = "inputOperationType"
            self.__select_element_txt(how="id", what=wf_oper, txt=wf_oper_val)

            #----------------------------------------------------------------------------------------------
            #  Click Radio button for Config file
            #  Note: Config files must have been loaded previous to this operation
            #  //td[contains(text(),"800E_ds_1069-w-inTr69_slaac")]/preceding-sibling::td/input[@type="radio"]
            # cfg_file = "800E_ds_1069-w-inTr69_slaac"
            cfg_file_chk_box = '//td[contains(text(),"' + cfg_file + '")]/preceding-sibling::td/input[@type="radio"]'
            self.__click_element(how="xpath", what=cfg_file_chk_box)

            #----------------------------------------------------------------------------------------------
            #  Click Done
            done_btn = '//button[@id="btn-doneOperation"]'
            self.__click_element(how="xpath", what=done_btn)

            #----------------------------------------------------------------------------------------------
            #  Click Next Button (wf_nxt_btn)
            self.__click_element(how="xpath", what=wf_nxt_btn)

            #----------------------------------------------------------------------------------------------
            #  Work Flow Execution type
            #  1) WorkFlowEventTrigger
            #  2) WorkFlowSchedulerTrigger
            # wf_type = "WorkFlowSchedulerTrigger"
            # wf_exec_type = '//select[@id="inputTriggerType"]//option[@value="' + wf_type + '"]'
            time.sleep(3)
            # wf_exec_type = '//select[@id="inputTriggerType"]'
            wf_exec_type = "inputTriggerType"
            self.__select_element_txt(how="id", what=wf_exec_type, txt=wf_type)

            #----------------------------------------------------------------------------------------------
            #  Input value = time in minutes
            # wf_exec_wndw_val = "10"
            time.sleep(5)
            wf_exec_window = '//input[@id="windowlength"]'
            self.__enter_element_txt(how="xpath", what=wf_exec_window, txt=wf_exec_wndw_val)

            #----------------------------------------------------------------------------------------------
            #  Click Next Button (wf_nxt_btn)
            self.__click_element(how="xpath", what=wf_nxt_btn)

            #----------------------------------------------------------------------------------------------
            #  Click Finish Button
            wf_finish_btn = '//a[contains(text(),"Finish")]'
            self.__click_element(how="xpath", what=wf_finish_btn)
        except:
            raise RuntimeError("fubar %s", ccfg_ip)
        return True

    def del_cfg_file(self, ccfg_ip, wf_page, wf_name_val):
        """
        :param ccfg_ip:
        :param wf_page:
        :param wf_name_val:
        :return:
        """
        try:
            print("Trying to delete: " + str(wf_name_val) + " at page: " + str(wf_page))
            self.driver.get('http://' + ccfg_ip + '/' + wf_page)
            cfg_del_btn = '//tr[descendant::td[contains(.,"' + wf_name_val + '")]]//i[@data-original-title="Delete"]'
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_xpath(cfg_del_btn))
            if self.driver.find_element_by_xpath(cfg_del_btn):
                self.__click_element(how="xpath", what=cfg_del_btn)
                del_confirm_btn = '//button[@class="btn btn-warning pull-right confirm"]'
                self.__click_element(how="xpath", what=del_confirm_btn)
            else:
                print("No Config File Found for deletion!")
                return True
        except:
            raise RuntimeError("Config file not Present: %s", wf_name_val)
        return True

    def chk_dld_status(self, ccfg_ip, wf_page, wf_name_val):
        """
        :param ccfg_ip:
        :param wf_page:
        :param wf_name_val:
        :return:
        """
        try:
            self.driver.get('http://' + ccfg_ip + '/' + wf_page)
            pass_wf_status = '//td[contains(text(),"' + wf_name_val + '")]/following-sibling::td[contains(text(),"Completed")]'
            fail_wf_status = '//td[contains(text(),"' + wf_name_val + '")]/following-sibling::td[contains(text(),"Failed")]'
            while complete == 0:
                self.driver.get('http://' + ccfg_ip + '/' + wf_page)
                if self.driver.find_element_by_xpath(pass_wf_status):
                    complete = 1
                elif self.driver.find_element_by_xpath():
                    complete = 0
                    time.sleep(30)
        except:
            raise RuntimeError("Config file not Present: %s", wf_name_val)
        return True

    def get_page(self, ccfg_ip, cfg_file_page):
        self.driver.get("http://" + ccfg_ip + "/" + cfg_file_page)