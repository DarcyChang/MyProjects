__author__ = 'gliverm'

from cafe.core.db import teststep
from cafe.core.logger import CLogger as Logger
# from cafe.core.signals import E7_SESSION_ERROR
from cafe.sessions.webgui import WebGuiSession
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
# Imported to deal with wait for next page to load
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
import contextlib
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import cafe
import re


logger = Logger(__name__)
debug = logger.debug
error = logger.error


# class ONTGuiException(Exception):
#     def __init__(self, msg=""):
#         logger.exception(msg, signal=E7_SESSION_ERROR)


class ONTGuiApiClass(WebGuiSession):
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

    # def __get_pulldown_index(self, how, what):
    #     """
    #     Description: Utility method to retrieve pull down selected index value.
    #     Args:
    #         how(str)(required):
    #         what(str)(required):
    #     Returns:
    #         Integer: Integer value of selected index.  None if failure occurred.
    #     """
    #     try:
    #         pulldown = Select(self.driver.find_element(by=how, value=what))
    #         selected = pulldown.first_selected_option
    #         all_options = pulldown.options
    #         base_ssid = all_options.0.text
    #         #selected_index = selected.get_attribute("index")
    #         print('yodel')
    #     except NoSuchElementException as exception:
    #         print("Exception: ", exception)
    #         return None
    #     return selected_index

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

    # ##################################################################################################################
    # External single commands to class
    # ##################################################################################################################

    def login(self, ontip, username="support", password="support"):
        """
        Description:
            Login into the ONT GUI.
        Args:
            ontip(str): IP address of ONT to log into. Default = NA
            username(str): Username used to log into the ONT. Default = "support"
            password(str): Password used to log inot the ONT. Default = "support"
        Returns:
            True if login is successful.
            An exception is raised if login fails.  Considered a critical failure.
        """
        connected = False
        retry_cnt = 0
        while connected == False:
            if retry_cnt <= 10:
                self.driver.get("http://" + ontip + "/login.html")
                connected = self.chk_element_exist(how="id", what="login_btn")
                if connected == False:
                    retry_cnt += 1
                    print("Retrying connection for count: " + str(retry_cnt))
            else:
                connected = "Fail"
                return False
        try:
            # Goto login screen.

            self.driver.get("http://" + ontip + "/login.html")
            WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "login_btn")))
            # WebDriverWait(self.driver, 30)\
            #     .until(lambda s: s.find_element_by_id("login_btn"))

            # Enter username in text box
            self.__enter_element_txt(how="id", what="user_name_field", txt=username)
            # Enter password in text box
            self.__enter_element_txt(how="id", what="password_field", txt=password)

            with self.__wait_for_page_load(timeout=30):
                self.__click_element(how="id", what="login_btn")
        except:
            raise RuntimeError("Not able to log into ONT. ONTIP=%s", ontip)
        return True

    def close_gui(self):
        self.driver.close()

    def wireless_radiosetup(self, ontip, radiotype, radio=None, mode=None, bandwidth=None, channel=None,
                            powerlevel=None, dfs=None, multicastforwarding=None):
        """
        Description:
            Perform provisioning work on the WiFi radio setup screen for both the 2.4GHz and 5GHz radios.  It is up to
            the user of this method to choose the correct values to configure.
        Args:
            ontip(str)(required): IP address of ONT to configure
            radiotype(str)(required): WiFi radio type to configure
                Valid values: (2.4GHz, 5GHz). Non-case sensitive
            radio(str)(optional): Set radio on or off 
                Valid values: (on, off) Non-case sensitive
            mode(str)(optional): Mode of radio
                Valid Values: Any actual value available in pull down element
            bandwidth(str)(optional): Bandwidth of radio
                Valid values: Any actual value available in pull down element
            channel(str)(optional): Channel set for the radio
                Valid values: Any actual value available in pull down element
            powerlevel(str)(optional): Power level of radio
                Valid values: Any actual value available in pull down element
            dfs(str)(optional): Enable/disable DFS of 5GHz radio
                Valid values: (disabled, enabled). Non-case sensitive
            multicastforwarding(str)(optional): Enable/disable multicast forwarding of 2.4GHz radio
                Valid values: (disabled, enabled). Non-case sensitive
        Returns:
            Dictionary: 'success' : set to string "True" when ALL provisioning actions pass otherwise "False"
        """
        totalsuccess = True
        # TODO: Need to migrate to key map logic in case page changes to easily modify change in one location

        # Get radio configuration page
        radiotype_str = str(radiotype).lower()
        if radiotype_str == "5ghz":
            radiotype_url = "5ghz"
        elif radiotype_str == "2.4ghz":
            radiotype_url = "2dot4ghz"
        else:
            radiotype_url = "bogus"
        try:
            self.driver.get("http://" + ontip + "/html/wireless/" + radiotype_url + "/wireless_radiosetup.html")
            # Wait put in to stop from detecting apply_btn in previous page
            time.sleep(1)
            WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
            ##WebDriverWait(self.driver, 30)\
            ##    .until(lambda s: s.find_element_by_id("apply_btn"))
        except:
            totalsuccess = False
        
        # Initialize if the apply button should be clicked.
        click_apply = False

        # Set WiFi Radio (radio button)
        if radio is not None:
            click_apply = True
            radio_str = str(radio).lower()
            success = True
            if radio_str == "on":
                success = self.__click_element(how="id", what="id_wl_on")
            if radio_str == "off":
                success = self.__click_element(how="id", what="id_wl_off")
            if not success:
                totalsuccess = False

        # Set WiFi radio mode (select)
        if mode is not None:
            # valid 5GHz values: "802.11n", 802.11"
            # valid 2.4GHz values: "802.11b, 802.11g, and 802.11n", "802.11g and 802.11n", "802.11",
            # "802.11b and 802.11g", "802.11b"
            click_apply = True
            success = self.__select_element_txt(how="id", what="id_80211bgn_mode", txt=mode)
            if not success:
                totalsuccess = False

        # Set WiFi radio bandwidth (select)
        if bandwidth is not None:
            # Valid 5GHz values: "20 MHz", "40 MHz", "80 MHz"
            # Valid 2.4GHz values: "20 MHz", "40 MHz"
            click_apply = True
            success = self.__select_element_txt(how="id", what="id_bandwidth", txt=bandwidth)
            if not success:
                totalsuccess = False

        # Set DFS (checkbox)
        # Needs to be positioned before choosing channel because choices change
        if dfs is not None:
            if radiotype_str == "5ghz":
                # TODO: Need to implement wrapper around the direct selenium calls
                click_apply = True
                success = True
                dfs_str = str(dfs).lower()
                is_dfs_checked = self.__is_checkbox_selected(how="id", what="dfs_check_obj_id")
                # if dfs_str == "enabled" and is_dfs_checked: Do nothing
                if dfs_str == "disabled" and is_dfs_checked:
                    success = self.__click_element(how="id", what="dfs_check_obj_id")
                if dfs_str == "enabled" and is_dfs_checked is False:
                    success = self.__click_element(how="id", what="dfs_check_obj_id")
                # if dfs_str == "disabled" and not is_dfs_checked: Do nothing
                if not success:
                    totalsuccess = False

        # Set WiFi radio channel (select)
        if channel is not None:
            # Valid 5GHz values: "Auto", "36", "40", "44", "48", "52", "56", "60", "64", "100", "104", "108", "112",
            #     "132", 136"
            # Valid 2.4GHz values: "Auto",
            click_apply = True
            success = self.__select_element_txt(how="id", what="channel_obj_id", txt=channel)
            if not success:
                totalsuccess = False

        # Set WiFi radio power level (select)
        if powerlevel is not None:
            # Value values: "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"
            click_apply = True
            success = self.__select_element_txt(how="id", what="id_power_level", txt=powerlevel)
            if not success:
                totalsuccess = False

        # Set Multicast Forwarding (checkbox)
        if multicastforwarding is not None:
            if radiotype_str == "2.4ghz":
                # TODO: Need to implement wrapper around the direct selenium calls
                click_apply = True
                success = True
                multicastforwarding_str = str(multicastforwarding).lower()
                is_multicastforwarding_checked = self.__is_checkbox_selected(how="id", what="id_MulticastForwarding")
                # if g_multicastforwarding == "enabled" and is_multicastforwarding_checked: Do nothing
                if multicastforwarding_str == "disabled" and is_multicastforwarding_checked:
                    success = self.__click_element(how="id", what="id_MulticastForwarding")
                if multicastforwarding_str == "enabled" and is_multicastforwarding_checked is False:
                    success = self.__click_element(how="id", what="id_MulticastForwarding")
                # if multicastforwarding_str == "disabled" and not is_multicastforwarding_checked: # Do nothing
                if not success:
                    totalsuccess = False

        if click_apply:
            success = self.__click_element(how="id", what="apply_btn")
            if not success:
                totalsuccess = False
            try:
                # The page seams to be be reloaded when apply button is clicked.  The following waits for the
                # apply button to be redisplayed just as done for initial loading of the page.
                #WebDriverWait(self.driver, 30) .until(lambda s: s.find_element_by_id("apply_btn"))
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
            except:
                totalsuccess = False

        result = {}
        # TODO: IF method fails want to build a list of errors to report in failure message
        result['checkpoint'] = cafe.Checkpoint(str(totalsuccess)).contains(exp="True",
                                                        title="ONT Web GUI WiFi radio provisioning",
                                                        pos_msg="success : all provisioning actions performed",
                                                        neg_msg="fail : TODO Build list of errors here")
        return result

    def wireless_ssidsetup(self, ontip, radiotype, ssid, ssidstate=None, broadcast=None, renamessid=None,
                           clientisolate=None, l2wansvc=None, ssidisolate=None, gw=None, startip=None,
                           stopip=None, mask=None):
        """
        Description:
            Perform provisioning work on the WiFi SSID Setup screen for both the 2.4GHz and 5GHz radios.  It is up to
            the user of this method to choose the correct values to configure.
        Args:
            ontip(str)(required): IP address of ONT to configure
            radiotype(str)(required): WiFi radio type to configure
                Valid values: (2.4GHz, 5GHz) Non-case sensitive
            ssid(str)(required): SSID to operate on
                Valid values: Any actual value available in pull down element
            ssidstate(str)(optional): Enable/disable the SSID state
                Valid values: (disabled, enabled) Non-case sensitive
            broadcast(str)(optional): Enable/disable broadcasting of SSID
                Valid values: (disabled, enabled) Non-case sensitive
            renamessid(str)(optional): Name to rename the SSID to
                Valid values: Any valid SSID value
            clientisolate(str)(optional): Enable/disable isolation of clients on the SSID
                Valid values: (disabled, enabled) Non-case sensitive
            l2wansvc(str)(optional): Enable/disable the SSID to be used in bridged WAN service
                Valid values: (disabled, enabled) Non-case sensitive
            ssidisolate(str)(optional): Enable/disable isolation between SSIDs
                Valid values: (disabled, enabled). Non-case sensitive
            gw(str)(optional): Gateway IP address of SSID Isolation enabled DHCP address pool
                Valid values: Valid gateway IP address value
            startip(str)(optional): Starting IP address of SSID Isolation enabled DHCP address pool
                Valid values: Valid start IP address value
            stopip(str)(optional): Stopping IP address of SSID Isolation enabled DHCP address pool
                Valid values: Valid stop IP address value
            mask(str)(optional): IP address subnet mask of SSID Isolation enabled DHCP address pool
                Valid values: Valid IP address subnet mask value
        Returns:
            Dictionary: 'success' : set to string "True" when ALL provisioning actions pass otherwise "False"
        """
        totalsuccess = True

        radiotype_str = str(radiotype).lower()
        if radiotype_str == "5ghz":
            radiotype_url = "5ghz"
        elif radiotype_str == "2.4ghz":
            radiotype_url = "2dot4ghz"
        else:
            radiotype_url = "bogus"
        try:
            self.driver.get("http://" + ontip + "/html/wireless/" + radiotype_url + "/wireless_multiplessid.html")
            WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
            # WebDriverWait(self.driver, 30)\
            #     .until(lambda s: s.find_element_by_id("apply_btn"))
        except:
            totalsuccess = False

        # Initialize if the apply button should be clicked.
        click_apply = False

        # Set SSID to work on (selected item from pull down)
        success = self.__select_element_txt(how="id", what="id_ssid", txt=ssid)
        if success:
            try:
                # Determine if this is the base SSID? - No use for info at this time
                pulldown = Select(self.driver.find_element(by='id', value='id_ssid'))
                selected = (pulldown.first_selected_option).text
                all_options = pulldown.options
                # Extract the base SSID (index value 0)
                base_ssid = all_options[0].text
                if base_ssid == selected:
                    is_base_ssid = True
                else:
                    is_base_ssid = False

                # Wait for apply button to become visible again
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                # WebDriverWait(self.driver, 30)\
                #     .until(lambda s: s.find_element_by_id("apply_btn"))
            except:
                totalsuccess = False
        else:
            totalsuccess = False
            
        # Set SSID state (radio button)
        if ssidstate is not None:
            click_apply = True
            success = True
            ssidstate_str = str(ssidstate).lower()
            if ssidstate_str == "enabled":
                success = self.__click_element(how="id", what="id_ssid_enable")
            if ssidstate_str == "disabled":
                success = self.__click_element(how="id", what="id_ssid_disable")
            if not success:
                    totalsuccess = False
            else:
                try:
                    # Wait for apply button to become visible again
                    WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                    # WebDriverWait(self.driver, 30)\
                    #     .until(lambda s: s.find_element_by_id("apply_btn"))
                except:
                    totalsuccess = False

        # Set broadcast of SSID (radio button)
        if broadcast is not None:
            click_apply = True
            success = True
            broadcast_str = str(broadcast).lower()
            if broadcast_str == "enabled":
                success = self.__click_element(how="id", what="id_mode_bcast")
            if broadcast_str == "disabled":
                success = self.__click_element(how="id", what="id_mode_hide")
            if not success:
                totalsuccess = False

        # Rename SSID (text)
        if renamessid is not None:
            click_apply = True
            success = self.__enter_element_txt(how="id", what="id_ssid_name", txt=renamessid)
            if not success:
                totalsuccess = False

        # Set Client Isolation (checkbox)
        if clientisolate is not None:
            # TODO: Need to implement wrapper around the direct selenium calls
            click_apply = True
            success = True
            clientisolate_str = str(clientisolate).lower()
            is_clientisolate_checked = self.__is_checkbox_selected(how="id", what="clientIsolateObj")
            # if g_clientisolate == "enabled" and is_clientisolate_checked: Do nothing
            if clientisolate_str == "enabled" and is_clientisolate_checked:
                success = self.__click_element(how="id", what="clientIsolateObj")
            if clientisolate_str == "disabled" and is_clientisolate_checked is False:
                success = self.__click_element(how="id", what="clientIsolateObj")
            # if g_clientisolate == "disabled" and not is_clientisolate_checked: Do nothing
            if not success:
                totalsuccess = False

        # Set L2 Bridged WAN Service (checkbox)
        if l2wansvc is not None:
            # TODO: Need to implement wrapper around the direct selenium calls
            click_apply = True
            success = True
            l2wansvc_str = str(l2wansvc).lower()
            is_l2wansvc_checked = self.__is_checkbox_selected(how="id", what="l2bridgeObj")
            # if g_l2wansvc == "enabled" and is_l2wansvc_checked: Do nothing
            if l2wansvc_str == "disabled" and is_l2wansvc_checked:
                success = self.__click_element(how="id", what="l2bridgeObj")
            if l2wansvc_str == "enabled" and is_l2wansvc_checked is False:
                success = self.__click_element(how="id", what="l2bridgeObj")
            # if g_l2wansvc == "disabled" and not is_l2wansvc_checked: Do nothing
            if not success:
                totalsuccess = False

        # Set Inter SSID Isolation (checkbox)
        if ssidisolate is not None:
            # TODO: Need to implement wrapper around the direct selenium calls
            click_apply = True
            success = True
            ssidisolate_str = str(ssidisolate).lower()
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "interIsolateObj")))
                # WebDriverWait(self.driver, 10)\
                #     .until(lambda s: s.find_element_by_id("interIsolateObj"))
            except:
                totalsuccess = False
            else:
                is_ssidisolate_checked = self.__is_checkbox_selected(how="id", what="interIsolateObj")
                # if g_ssidisolate == "enabled" and is_ssidisolate_checked: Do nothing
                if ssidisolate_str == "disabled" and is_ssidisolate_checked:
                    success = self.__click_element(how="id", what="interIsolateObj")
                if ssidisolate_str == "enabled" and is_ssidisolate_checked is False:
                    success = self.__click_element(how="id", what="interIsolateObj")
                # if g_ssidisolate== "disabled" and not is_ssidisolate_checked: Do nothing
                if not success:
                    totalsuccess = False

        # Set Gateway IP address
        if gw is not None:
            click_apply = True
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "gatewayObj")))
                # WebDriverWait(self.driver, 10)\
                #     .until(lambda s: s.find_element_by_id("gatewayObj"))
            except:
                totalsuccess = False
            else:
                success = self.__enter_element_txt(how="id", what="gatewayObj", txt=gw)
                if not success:
                    totalsuccess = False

        # Set Beginning IP Address
        if startip is not None:
            click_apply = True
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "ipAddressStartObj")))
                # WebDriverWait(self.driver, 10)\
                #     .until(lambda s: s.find_element_by_id("ipAddressStartObj"))
            except:
                totalsuccess = False
            else:
                success = self.__enter_element_txt(how="id", what="ipAddressStartObj", txt=startip)
                if not success:
                    totalsuccess = False

        # Set Ending IP Address
        if stopip is not None:
            click_apply = True
            try:
                WebDriverWait(self.driver, 10)\
                .until(lambda s: s.find_element_by_id("ipAddressEndObj"))
            except:
                totalsuccess = False
            else:
                success = self.__enter_element_txt(how="id", what="ipAddressEndObj", txt=stopip)
                if not success:
                    totalsuccess = False

        # Set Subnet Mask
        if mask is not None:
            click_apply = True
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "ipAddressMaskObj")))
                # WebDriverWait(self.driver, 10)\
                #     .until(lambda s: s.find_element_by_id("ipAddressMaskObj"))
            except:
                totalsuccess = False
            else:
                success = self.__enter_element_txt(how="id", what="ipAddressMaskObj", txt=mask)
                if not success:
                    totalsuccess = False
            
        if click_apply:
            success = self.__click_element(how="id", what="apply_btn")
            if not success:
                    totalsuccess = False
            # The page seams to be be reloaded when apply button is clicked.  The following waits for the
            # apply button to be redisplayed just as done for initial loading of the page.
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                # WebDriverWait(self.driver, 30)\
                #     .until(lambda s: s.find_element_by_id("apply_btn"))
            except:
                totalsuccess = False

        result = {}
        # TODO: IF method fails want to build a list of errors to report in failure message
        result['checkpoint'] = cafe.Checkpoint(str(totalsuccess)).contains(exp="True",
                                                        title="ONT Web GUI WiFi SSID setup provisioning",
                                                        pos_msg="success : all provisioning actions performed",
                                                        neg_msg="fail : TODO Build list of errors here")
        return result

    def wireless_securitysetup(self, ontip, radiotype, ssid, securitytype=None, encryptiontype=None, keytype=None,
                               passphrase=None):
        """
        Description:
            Perform provisioning work on the WiFi Security Setup screen for both the 2.4GHz and 5GHz radios.  It is up
            to the user of this method to choose the correct values to configure.
        Args:
            ontip(str)(required): IP address of ONT to configure
            radiotype(str)(required): WiFi radio type to configure
                Valid values: (2.4GHz, 5GHz) Non-case sensitive
            ssid(str)(required): SSID to operate on
                Valid values: (Any actual value available in pull down element
            securitytype(str)(optional): SSID Security type
                Valid values: Any actual value available in pull down element
            encryptiontype(str)(optional): SSID security type encryption type
                Valid values: Any actual value available in pull down element for security type
            keytype(str)(optional): Name to rename the SSID to
                Valid values: (Default, Custom) non-case sensitive
            passphrase(str)(optional): SSID Security custom passphrase
                Valid values: Any valid passphrase value.
        Returns:
            Dictionary: 'success' : set to string "True" when ALL provisioning actions pass otherwise "False"
        """
        totalsuccess = True

        radiotype_str = str(radiotype).lower()
        if radiotype_str == "5ghz":
            radiotype_url = "5ghz"
        elif radiotype_str == "2.4ghz":
            radiotype_url = "2dot4ghz"
        else:
            radiotype_url = "bogus"
        try:
            self.driver.get("http://" + ontip + "/html/wireless/" + radiotype_url + "/wireless_security.html")
            WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
            # WebDriverWait(self.driver, 30)\
            #     .until(lambda s: s.find_element_by_id("apply_btn"))
        except:
            totalsuccess = False

        # Initialize if the apply button should be clicked.
        click_apply = False

        # Set SSID to work on (selected item from pull down)
        success = self.__select_element_txt(how="id", what="id_ssid", txt=ssid)
        if success:
            try:
                # Wait for apply button to become visible again
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                # WebDriverWait(self.driver, 30)\
                #     .until(lambda s: s.find_element_by_id("apply_btn"))
            except:
                totalsuccess = False
        else:
            totalsuccess = False

        # Set Security type (selected item from pull down)
        if securitytype is not None:
            # valid values: "WPA-WPA2-Personal", "WPA2-Personal", "Security Off"
            click_apply = True
            success = self.__select_element_txt(how="id", what="security_type", txt=securitytype)
            if success:
                try:
                    # Wait for apply button to become visible again
                    WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                    # WebDriverWait(self.driver, 30)\
                    #     .until(lambda s: s.find_element_by_id("apply_btn"))
                except:
                    totalsuccess = False
            else:
                totalsuccess = False

        # Set Encryption type (selected item from pull down)
        if encryptiontype is not None:
            # valid values: "Both", "AES", "TKIP"
            click_apply = True
            success = self.__select_element_txt(how="id", what="id_wpa_cipher", txt=encryptiontype)
            if success:
                try:
                    # Wait for apply button to become visible again
                    WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                    # WebDriverWait(self.driver, 30)\
                    #     .until(lambda s: s.find_element_by_id("apply_btn"))
                except:
                    totalsuccess = False
            else:
                totalsuccess = False

        # Set passphrase key type (radio button)
        if keytype is not None:
            click_apply = True
            keytype_str = str(keytype).lower()
            success = None
            if keytype_str == "default":
                success = self.__click_element(how="id", what="lshxq01")
            if keytype_str == "custom":
                success = self.__click_element(how="id", what="lshxq02")
            if not success:
                totalsuccess = False

        # Set custom passphrase
        if passphrase is not None:
            click_apply = True
            success = None
            try:
                WebDriverWait(self.driver, 10)\
                    .until(lambda s: s.find_element_by_id("pskKeyInput"))
            except:
                totalsuccess = False
            else:
                self.__enter_element_txt(how="id", what="pskKeyInput", txt=passphrase)
                if not success:
                    totalsucess = False

        if click_apply:
            success = self.__click_element(how="id", what="apply_btn")
            if not success:
                    totalsuccess = False
            # The page seams to be be reloaded when apply button is clicked.  The following waits for the
            # apply button to be redisplayed just as done for initial loading of the page.
            try:
                WebDriverWait(self.driver, 30).until(visibility_of_element_located((By.ID, "apply_btn")))
                # WebDriverWait(self.driver, 30)\
                #     .until(lambda s: s.find_element_by_id("apply_btn"))
            except:
                totalsuccess = False

        result = {}
        # TODO: IF method fails want to build a list of errors to report in failure message
        result['checkpoint'] = cafe.Checkpoint(str(totalsuccess)).contains(exp="True",
                                                        title="ONT Web GUI WiFi security provisioning",
                                                        pos_msg="success : all provisioning actions performed",
                                                        neg_msg="fail : TODO Build list of errors here")
        return result

    def chk_element_exist(self, how, what):
        try:
            #print("Checking for element: " + what)
            self.driver.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def tr069_setup(self, ontip, acs_url, uname, pword, periodic_inform, inform_intvl, tr069_vlan, tr069_wan):
        """
        :param ontip:
        :param acs_url:
        :param uname:
        :param pword:
        :param periodic_inform:
        :param inform_intvl:
        :param tr69_wan:
        :return:
        """
        totalsuccess = True
        try:
            #----------------------------------------------------------------------------------
            # Initialize Variables for ACS
            #
            acs_url_loc = '//input[@id="acs_url_field"]'
            uname_loc = '//input[@id="username_field"]'
            pword_loc = '//input[@id="password_password_field"]'
            if periodic_inform == True:
                periodic_inf_loc = '//input[@id="periodic_inform_state_enabled_radio"]'
            else:
                periodic_inf_loc = '//input[@id="periodic_inform_state_disabled_radio"]'
            periodic_inf_intvl_loc = '//input[@id="periodic_inform_interval_field"]'
            tr069_wan_loc = '//input[@id="service_label"]'

            #----------------------------------------------------------------------------------
            # Initialize Variables for TR-069 Service
            #
            edit_btn_loc = '//button[contains(text(),"Edit")]'
            tag_action_loc = '//input[@name="VLAN_config"]'
            tag_act_val = '//input[@id="vlan_config_vlan_id"]'
            tag_prio_val = '//input[@id="vlan_config_priority"]'

            #----------------------------------------------------------------------------------
            # Configure WAN Interface
            #
            self.driver.get("http://" + ontip + "/html/support/support_wan_setting_ipv6.html")
            wan_found = self.chk_element_exist(how="xpath", what=edit_btn_loc)
            if wan_found == True:
                self.__click_element(how="xpath", what=edit_btn_loc)
            else:
                self.__click_element(how="id", what="create_new_vlan_button")
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_id("form_apply_btn"))
            self.__enter_element_txt(how="xpath", what=tr069_wan_loc, txt=tr069_wan)
            self.__click_element(how="xpath", what=tag_action_loc)
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_id("vlan_config_vlan_id"))
            self.__enter_element_txt(how="xpath", what=tag_act_val, txt=tr069_vlan)
            self.__enter_element_txt(how="xpath", what=tag_prio_val, txt="0")
            self.__click_element(how="id", what="form_apply_btn")

            #----------------------------------------------------------------------------------
            # Configure TR-069 Interface
            #
            self.driver.get("http://" + ontip + "/html/support/tr069.html")
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_id("apply_button"))

            try:
                self.__enter_element_txt(how="xpath", what=acs_url_loc, txt=acs_url)
            except:
                totalsuccess = False

            try:
                self.__enter_element_txt(how="xpath", what=uname_loc, txt=uname)
            except:
                totalsuccess = False

            try:
                self.__enter_element_txt(how="xpath", what=pword_loc, txt=pword)
            except:
                totalsuccess = False

            try:
                self.__click_element(how="id", what="periodic_inform_state_enabled_radio")
            except:
                totalsuccess = False

            try:
                self.__enter_element_txt(how="xpath", what=periodic_inf_intvl_loc, txt=inform_intvl)
            except:
                totalsuccess = False

            try:
                self.__select_element_txt(how="id", what="tr069_ifname", txt=tr069_wan)
            except:
                totalsuccess = False

            if totalsuccess == True:
                try:
                    self.__click_element(how="id", what="apply_button")
                except:
                    raise RuntimeError("Failed to Apply TR-069 Config! %s", ontip)
        except:
            raise RuntimeError("Failed to Apply TR-069 Config! %s", ontip)
        return totalsuccess

    def restore_dflts(self, ontip):
        """
        :param ontip:
        :return:
        """
        print("# Restoring ONT Defaults!")
        connected = False
        while connected == False:
            self.driver.get("http://" + ontip + "/html/utilities/utilities_restoredefaultsettings.html")
            connected = self.chk_element_exist(how="id", what="restore_btn")

        rstr_dflt_complete = False
        rstr_dflt_fail_cnt = 0
        ok_btn_loc = '//button[contains(text(),"Ok")]'
        self.__click_element(how="id", what="restore_btn")
        WebDriverWait(self.driver, 30)\
            .until(lambda s: s.find_element_by_xpath(ok_btn_loc))
        self.__click_element(how="xpath", what=ok_btn_loc)
        time.sleep(60)
        while rstr_dflt_complete == False:
            if rstr_dflt_fail_cnt <= 20:
                self.driver.get("http://" + ontip + "/html/support/tr069.html")
                rstr_dflt_complete = self.chk_element_exist(how="id", what="apply_button")
                if rstr_dflt_complete == False:
                    time.sleep(5)
                    rstr_dflt_fail_cnt += 1
                    print("Retry Restore Validation for count: " + str(rstr_dflt_fail_cnt))
            else:
                str_dflt_complete = "Fail"

        if rstr_dflt_complete == True:
            return True
        else:
            return False


    def chk_dld_cmplt(self, ontip, eut, scenario):
        """
        :param eut:
        :param scenario:
        :return:
        """
        connected = False
        dld_fail = False
        scenario = scenario.split('-')[0]
        if scenario == "fw":
            scenario = "ds"
        while connected == False:
            self.driver.get("http://" + ontip + "/html/support/support_wan_setting_ipv6.html")
            connected = self.chk_element_exist(how="xpath", what='//button[contains(text(),"Edit")]')
        dld_cmplt = False
        dld_chk_cnt = 0
        while dld_cmplt == False:
            if dld_chk_cnt <= 10:
                self.driver.get("http://" + ontip + "/html/support/support_wan_setting_ipv6.html")
                eut_found = self.chk_element_exist(how="xpath", what='//td[contains(text(),"' + eut + '")]')
                print("EUT Found: " + str(eut_found) + " for " + eut)
                scenario_found = self.chk_element_exist(how="xpath", what='//td[contains(text(),"' + scenario + '")]')
                print("Scenario Found: " + str(scenario_found) + " for " + scenario)
                if eut_found == True and scenario_found == True:
                    dld_cmplt = True
                else:
                    print("Checking again for count " + str(dld_chk_cnt) + "!")
                    dld_chk_cnt += 1
                    time.sleep(5)
            else:
                print("Download Failed!")
                dld_cmplt = True
                dld_fail = True
        if dld_cmplt == True:
            if dld_fail == True:
                return False
            else:
                return True
        else:
            return False

    def cfg_wifi_cdr(self, ontip, ssid, pword):
        """
        :param eut:
        :param scenario:
        :return:
        """
        try:
            # Change SSID for CD Router Wifi Testing
            self.driver.get("http://" + ontip + "/html/wireless/2dot4ghz/wireless_multiplessid.html")
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_id("apply_btn"))
            try:
                self.__enter_element_txt(how="id", what="id_ssid_name", txt=ssid)
            except:
                totalsuccess = False
            try:
                self.__click_element(how="id", what="apply_btn")
            except:
                totalsuccess = False
            # Set the WPA password
            self.driver.get("http://" + ontip + "/html/wireless/2dot4ghz/wireless_security.html")
            WebDriverWait(self.driver, 30)\
                .until(lambda s: s.find_element_by_id("apply_btn"))
            try:
                self.__enter_element_txt(how="id", what="pskKeyInput", txt=pword)
            except:
                totalsuccess = False
            try:
                self.__click_element(how="id", what="apply_btn")
            except:
                totalsuccess = False
        except:
            print("Fubar")

    def get_ont_version(self,ontip):
        ont_ver = "null"
        self.driver.get("http://" + ontip + "/html/status/status_connection.html")
        ont_ver_xpath = '//td[contains(text(),"Software Version")]/following-sibling::*[1]'
        ont_ver = (self.driver.find_element_by_xpath(ont_ver_xpath).text)
        return ont_ver

    def set_ont_fw(self, ontip, sm, fw):
        totalsuccess = True
        if sm == "":
            sm = "en"
        fw_off = '//input[@id="security_level_off"]'
        fw_low = '//input[@id="security_level_low"]'
        fw_med = '//input[@id="security_level_medium"]'
        fw_hi = '//input[@id="security_level_high"]'
        sm_en = '//input[@id="stealth_mode_enabled_radio"]'
        sm_dis =  '//input[@id="stealth_mode_disabled_radio"]'
        self.driver.get("http://" + ontip + "/html/advanced/security/advanced_security_firewallsettings.html")
        continue_prov = self.chk_element_exist(how="id", what='apply_btn')
        if continue_prov == True:
            if not sm == "en":
                try:
                    self.__click_element(how="xpath", what=sm_dis)
                except:
                    totalsuccess = False
            else:
                try:
                    self.__click_element(how="xpath", what=sm_en)
                except:
                    totalsuccess = False

            if fw == "off":
                try:
                    self.__click_element(how="xpath", what=fw_off)
                except:
                    totalsuccess = False
            elif fw == "lo":
                try:
                    self.__click_element(how="xpath", what=fw_low)
                except:
                    totalsuccess = False
            elif fw == "med":
                try:
                    self.__click_element(how="xpath", what=fw_med)
                except:
                    totalsuccess = False
            else:
                try:
                    self.__click_element(how="xpath", what=fw_hi)
                except:
                    totalsuccess = False
        if totalsuccess == True:
            self.__click_element(how="id", what="apply_btn")

    def set_fw_svc_state(self, ontip, svc_name, svc_state):
        totalsuccess = True
        dbglvl = "info"

        time.sleep(5)
        self.__click_element(how="xpath", what='(//button[@class="expand-collapse"])[2]')
        #enter_btn = self.driver.find_element_by_xpath('//button[@class="expand-collapse"]')
        #enter_btn.send_keys(Keys.ENTER)
        for i in range(len(svc_name)):
            if re.search("Stealth", svc_name[i], re.S):
                print("Found Stealth Mode!")
            elif re.search("Firewall", svc_name[i], re.S):
                print("Found Firewall Level!")
            else:
                if dbglvl == "dbg":
                    print("Service: " + svc_name[i] + " == " + svc_state[i])
                svc_xpath = '//input[@id="' + svc_name[i] + '"]'
                chk_box_selected = self.__is_checkbox_selected(how="xpath", what=svc_xpath)
                svc_name_found = self.chk_element_exist(how="xpath", what=svc_xpath)
                if svc_name_found == True:
                    if svc_state[i] == "1":
                        if chk_box_selected != True:
                            try:
                                self.__click_element(how="xpath", what=svc_xpath)
                            except:
                                if totalsuccess != False:
                                    totalsuccess = False
                    elif svc_state[i] == "0":
                        if chk_box_selected == True:
                            try:
                                self.__click_element(how="xpath", what=svc_xpath)
                            except:
                                if totalsuccess != False:
                                    totalsuccess = False
                else:
                    print("Svc Name: " + svc_name + " Not Found!")
                    if totalsuccess != False:
                        totalsuccess = False

        if totalsuccess == True:
            self.__click_element(how="id", what="apply_btn")
            return True
        else:
            return False


# if __name__ == "__main__":
#     '''
#     The purpose of this section is to test teh APIs created.
#     '''
#     import cafe
#     session_mgr = cafe.get_session_manager()
#     # create a ssh session to exa device
#     exa_ssh_session = session_mgr.create_session("exa1", session_type="ssh",
#                                                  host="10.243.19.213",
#                                                  user="root", password="root")
#     # get EXACommClass object - EXA equipment lib
#     exa = EXAApiClass(exa_ssh_session)
#     # login and open exa cli console
#     exa.login()
#     # exa.command return a dict data structure as we have declare it as teststep
#     r = exa.command("show interface craft 1")
#     cafe.Checkpoint(r['response']).regex("craft 1")
#
#     r = exa.get_interface_craft(1)
#     cafe.Checkpoint(r['name']).regex("craft 1")
