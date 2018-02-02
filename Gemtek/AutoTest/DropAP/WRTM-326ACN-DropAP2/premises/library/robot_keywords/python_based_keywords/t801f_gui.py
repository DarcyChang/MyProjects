import cafe
from cafe import App
from cafe.core.logger import CLogger
from caferobot.web.device.webgui import WebBrowser

_module_logger = CLogger(__name__)
info = _module_logger.info


def t801f_gui_click(browser, element_type, text, header=None):
    gui = WebBrowser(browser)

    if element_type == 'link':
        locator = str("link=%s" % text)
    elif element_type == 'button':
        if header == None:
            locator = str("xpath=//button[contains(text(),'%s')]" % (text))
        else:
            locator = str("xpath=//h1[text()='%s']/parent::form//button[contains(text(),'%s')]" % (header, text))
    # elif element_type == 'checkbox':
    #     locator = str("xpath=//*[contains(text(),'%s']/input[@type='checkbox']" % text)
    else:
        raise ValueError("Invalid Element Type: %s" % element_type)

    gui.click_element(locator)
    info("click %s '%s'." % (element_type, text))


def t801f_gui_set_value(browser, element_type, text, value):
    gui = WebBrowser(browser)

    if element_type == 'input':
        # locator = str("xpath=//label[contains(text(),'%s')]/parent::div//input" % lable_text)
        locator = str("xpath=//*[text()='%s']/parent::div//input" % text)
        gui.input_text(locator, value)
    # elif element_type == '':
    #     locator = str("xpath=//label[contains(text(),'%s')]/parent::div//input" % lable_text)
    else:
        raise ValueError("Invalid Element Type: %s" % element_type)

    info("set %s element '%s' to '%s'." % (element_type, text, value))


def t801f_gui_get_value(browser, element_type, lable_text):
    gui = WebBrowser(browser)

    if element_type == 'input':
        # locator = str("xpath=//label[contains(text(),'%s')]/parent::div//input" % lable_text)
        locator = str("xpath=//*[text()='%s']/parent::div//input" % lable_text)
        value = gui.get_element_value(locator)
    # elif element_type == '':
    #     locator = str("xpath=//label[contains(text(),'%s')]/parent::div//input" % lable_text)
    else:
        raise ValueError("Invalid Element Type: %s" % element_type)

    info("set %s element '%s' to '%s'." % (element_type, lable_text, value))
    return value


def t801f_gui_get_table_cell_value(browser, table_header, table_index, tr_index, td_index):
    gui = WebBrowser(browser)
    result = gui.get_element_text("xpath=//h1[text()='%s']/parent::div//table[%d]//tr[%d]/td[%d]" % (table_header, table_index, tr_index, td_index))
    return result


def t801f_gui_login(browser, user, pwd):
    locator = str("xpath=//button[contains(text(),'Login')]")
    gui = WebBrowser(browser)
    gui.wait_until_element_is_visible(locator)

    t801f_gui_set_value(browser, 'input', 'User Name:', user)
    t801f_gui_set_value(browser, 'input', 'Password:', pwd)
    t801f_gui_click(browser, 'button', 'Login')

def t801f_gui_open_link(browser, *links):
    for linkname in links:
        t801f_gui_click(browser, 'link', linkname)
        info("open link %s" % linkname)

def t801f_gui_set_password(browser, new_pwd):
    t801f_gui_set_value(browser, 'input', 'New Password', new_pwd)
    t801f_gui_set_value(browser, 'input', 'Password Confirmation', new_pwd)
    t801f_gui_click(browser, 'button', 'Apply')

def t801f_gui_set_acs(browser, url=None, user=None, pwd=None):
    if url != None:
        t801f_gui_set_value(browser, 'input', 'ACS URL', url)
    if user != None:
        t801f_gui_set_value(browser, 'input', 'Username', user)
    if pwd != None:
        t801f_gui_set_value(browser, 'input', 'Password', pwd)
    t801f_gui_click(browser, 'button', 'Apply', 'TR-069')

def t801f_gui_ping(browser, url):
    gui = WebBrowser(browser)
    gui.input_text("id=id_host_ping", url)
    gui.click_element("id=id_submitBtn_ping")
    result = gui.get_element_value("id=ping_result")
    return result

def t801f_gui_get_wan_stats(browser, item):
    dict_table_index = {'Wan IP Netmask':2, 'Wan Gateway':3, 'Packets Sent':4, 'Packets Received':5}
    td_index = dict_table_index.get(item)
    result = t801f_gui_get_table_cell_value(browser, 'IF-MIB Stats', 1, 2, td_index)
    return result

def t801f_gui_get_lan_stats(browser, item):
    dict_table_index = {'IP Connection Speed':2, 'RX Pkt Rate':3, 'TX Pkt Rate':4, 'RX Pkt Cnt':5, 'TX Pkt Cnt':6}
    td_index = dict_table_index.get(item)
    result = t801f_gui_get_table_cell_value(browser, 'IF-MIB Stats', 2, 2, td_index)
    return result

def t801f_gui_get_gfast_stats(browser, item='Link State'):
    dict_table_index = {'Link State':2, 'RX Phy Rate':3, 'TX Phy Rate':4, 'RX ETR':5, 'TX ETR':6}
    td_index = dict_table_index.get(item)
    result = t801f_gui_get_table_cell_value(browser, 'G.Fast', 1, 2, td_index)
    return result

def t801f_gui_get_tr69_stats(browser, item='Link State'):
    dict_table_index = {'IP HOST':2, 'STATUS':3}
    td_index = dict_table_index.get(item)
    result = t801f_gui_get_table_cell_value(browser, 'IP Host/TR-69 Status', 1, 2, td_index)
    # gui = WebBrowser(browser)
    # result = gui.get_element_text("xpath=//h1[text()='IP Host/TR-69 Status']/parent::div//table//tr[2]/td[%d]" % index)
    return result
