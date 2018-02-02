import errno

import re
import robot
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from cafe.constants.sessions.webgui import ScreenshotMode
from cafe.sessions.util.webgui.locator.elementfinder import ElementFinder
from cafe.sessions.util.webgui.locator.tableelementfinder import TableElementFinder

__author__ = 'kelvin'

from selenium.webdriver import ActionChains

from cafe.core.logger import CLogger as Logger
from cafe.core.utils import create_folder, index_generator
import os
import time
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
_module_logger = Logger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warn
error = _module_logger.error

Logger("selenium.webdriver.remote.remote_connection").console = False
#webdriver_log.enable_file_logging("webdriver.log")

class WebDriverMonkeyPatches:

    RemoteWebDriver._base_execute2 = RemoteWebDriver.execute

    def execute(self, driver_command, params=None):
        result = self._base_execute2(driver_command, params)
        speed = self._get_speed2()
        if speed > 0:
            time.sleep(speed)
        return result

    def get_current_url(self):
        return self.current_url

    def get_current_window_handle(self):
        return self.current_window_handle

    def get_current_window_info(self):
        id_, name, title, url = self.execute_script("return [ window.id, window.name, document.title, document.URL ];")
        id_ = id_ if id_ is not None else 'undefined'
        name, title, url = (att if att else 'undefined' for att in (name, title, url))
        return self.current_window_handle, id_, name, title, url

    def get_page_source(self):
        return self.page_source

    def get_title(self):
        return self.title

    def get_window_handles(self):
        return self.window_handles

    def current_window_is_main(self):
        return self.current_window_handle == self.window_handles[0];

    def set_speed(self, seconds):
        self._speed2 = seconds

    def _get_speed2(self):
        if not hasattr(self, '_speed2'):
            self._speed2 = float(0)
        return self._speed2

    RemoteWebDriver.get_title = get_title
    RemoteWebDriver.get_current_url = get_current_url
    RemoteWebDriver.get_page_source = get_page_source
    RemoteWebDriver.get_current_window_handle = get_current_window_handle
    RemoteWebDriver.get_current_window_info = get_current_window_info
    RemoteWebDriver.get_window_handles = get_window_handles
    RemoteWebDriver.set_speed = set_speed
    RemoteWebDriver._get_speed2 = _get_speed2
    RemoteWebDriver.execute = execute


class WebGuiSession(object):
    _screenshot_index_generator = index_generator()

    def __init__(self, sid=None, browser=None, default_element_wait=10, logfile=None, logger=Logger(__name__),
                 execute_speed=0.0, default_timeout=10.0, screenshot_mode='FAIL', **kwargs):
        self.sid = sid
        self.logger = logger
        self.session_log = logger.get_child("log")
        self.logfile = logfile
        self.browser = browser
        self._driver_args = kwargs
        self._driver = None
        self._element_finder = ElementFinder()
        self._table_element_finder = TableElementFinder()
        self._implicit_wait_in_secs = default_element_wait
        self._speed_in_secs = execute_speed
        self._timeout_in_secs = default_timeout
        self._screenshot_mode = ScreenshotMode.get_screenshot_mode(screenshot_mode)

    def set_webdriver_log(self, logfile):
        if logfile:
            Logger("selenium.webdriver.remote.remote_connection").enable_file_logging(logfile)
            Logger("selenium.webdriver.remote.remote_connection").console = False

    def set_webdriver_log_console_display(self, v=True):
        Logger("selenium.webdriver.remote.remote_connection").console = v

    @property
    def driver(self):
        if self._driver is not None:
            return self._driver

        self._driver = self._get_driver(self.browser)
        return self._driver

    @property
    def logfile(self):
        return self._logfile

    @logfile.setter
    def logfile(self, f):
        if f is None:
            self.session_log.disable_file_logging()
            return
        if create_folder(f):
            self.logger.info("create folder for file %s successful" % f)
        else:
            self.logger.info("create folder for file %s failed" % f)
            return
        self._logfile = f
        self.session_log.enable_file_logging(log_file=f)

    def get_action_chains(self):
        """
        get the selenium ActionChains object for the drivers
        """
        self.open_browser()
        return ActionChains(self.driver)

    def close(self):
        self.close_browser()
        # try:
        #     self._driver.quit()
        # except:
        #     pass

    def open_browser(self):
        if self._driver is None:
            info('open browser')
        return self.driver

    def close_browser(self):
        if self._driver is None:
            return

        info('close browser')

        try:
            # self._driver.close()
            self._driver.quit()
        except Exception:
            pass
        finally:
            self._driver = None

    def go_to_page(self, url):
        info('Go to page: %s' % url)
        self._driver.get(url)

    def add_cookie(self,name, value, path=None, domain=None, secure=None,
            expiry=None):
        """Adds a cookie to your current session.
        "name" and "value" are required, "path", "domain" and "secure" are
        optional"""
        new_cookie = {'name': name,
                      'value': value}
        if path: new_cookie['path'] = path
        if domain: new_cookie['domain'] = domain
        #secure should be True or False so check explicitly for None
        if secure is not None: new_cookie['secure'] = secure

        self._driver.add_cookie(new_cookie)

    def delete_cookie(self, name):
        """Deletes cookie matching `name`.

        If the cookie is not found, nothing happens.
        """
        self._driver.delete_cookie(name)

    def get_cookie(self, name):
        return self._driver.get_cookie(name)

    def get_checkbox(self, locator):
        return self._element_find(locator, True, True, tag='input')

    def choose_file(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `locator`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host
        where the Selenium Server is running.

        Example:
        | Choose File | my_upload_field | /home/user/files/trades.csv |
        """
        if not os.path.isfile(file_path):
            raise AssertionError("File '%s' does not exist on the local file system"
                        % file_path)
        self._element_find(locator, True, True).send_keys(file_path)

    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    def click_visible_element(self, locator):
        """Click visible element identified by `locator
        """
        info("Clicking visible element '%s'." % locator)
        elements = self._element_find(locator, False, True)
        if not isinstance(elements, list):
            elements = [elements]
        debug('find %d elements' % len(elements))
        for elem in elements:
            if elem.is_displayed():
                debug('elem is displayed')
                elem.click()
                return

            debug('elem is not displayed')

        raise ValueError("Element locator '" + locator + "' did not match any visible elements.")


    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        info("Double clicking element '%s'." % locator)
        element = self._element_find(locator, True, True)
        ActionChains(self._driver).double_click(element).perform()

    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.

        Examples:
        | Drag And Drop | elem1 | elem2 | # Move elem1 over elem2. |
        """
        src_elem = self._element_find(source, True, True)
        trg_elem = self._element_find(target, True, True)
        ActionChains(self._driver).drag_and_drop(src_elem, trg_elem).perform()

    def is_element_enable(self, locator):
        element = self._element_find(locator, True, True)
        if not self._is_form_element(element):
            raise AssertionError("ERROR: Element %s is not an input." % (locator))
        if not element.is_enabled():
            return False
        read_only = element.get_attribute('readonly')
        if read_only == 'readonly' or read_only == 'true':
            return False
        return True

    def is_element_visible(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            return element.is_displayed()
        return None

    def get_element_text(self, locator):
        element = self._element_find(locator, True, True)
        if element is not None:
            return element.text
        return None

    def get_element_attribute(self, attribute_locator):
        """Return value of element attribute.

        `attribute_locator` consists of element locator followed by an @ sign
        and attribute name, for example "element_id@class".
        """
        locator, attribute_name = self._parse_attribute_locator(attribute_locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise ValueError("Element '%s' not found." % locator)
        return element.get_attribute(attribute_name)

    def get_implicit_wait_time(self):
        """Gets the wait in seconds that is waited by Selenium.

        See `Set Selenium Implicit Wait` for an explanation."""
        return robot.utils.secs_to_timestr(self._implicit_wait_in_secs)

    def set_implicit_wait_time(self, seconds):
        """Sets Selenium 2's default implicit wait in seconds and
        sets the implicit wait for all open browsers.

        From selenium 2 function 'Sets a sticky timeout to implicitly
            wait for an element to be found, or a command to complete.
            This method only needs to be called one time per session.'

        Example:
        | ${orig wait} = | Set Selenium Implicit Wait | 10 seconds |
        | Perform AJAX call that is slow |
        | Set Selenium Implicit Wait | ${orig wait} |
        """
        old_wait = self.get_implicit_wait_time()
        self._implicit_wait_in_secs = robot.utils.timestr_to_secs(seconds)
        self._driver.implicitly_wait(self._implicit_wait_in_secs)
        return old_wait

    def get_execute_speed(self):
        """Gets the delay in seconds that is waited after each Selenium command.

        See `Set Selenium Speed` for an explanation."""
        return robot.utils.secs_to_timestr(self._speed_in_secs)

    def set_execute_speed(self, seconds):
        """Sets the delay in seconds that is waited after each Selenium command.

        This is useful mainly in slowing down the test execution to be able to
        view the execution. `seconds` may be given in Robot Framework time
        format. Returns the previous speed value.

        Example:
        | Set Selenium Speed | .5 seconds |
        """
        old_speed = self.get_execute_speed()
        self._speed_in_secs = robot.utils.timestr_to_secs(seconds)
        self._driver.set_speed(self._speed_in_secs)
        return old_speed

    def get_timeout(self):
        """Gets the timeout in seconds that is used by various keywords.

        See `Set Selenium Timeout` for an explanation."""
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_timeout(self, seconds):
        """Sets the timeout in seconds used by various keywords.

        There are several `Wait ...` keywords that take timeout as an
        argument. All of these timeout arguments are optional. The timeout
        used by all of them can be set globally using this keyword.
        See `Timeouts` for more information about timeouts.

        The previous timeout value is returned by this keyword and can
        be used to set the old value back later. The default timeout
        is 5 seconds, but it can be altered in `importing`.

        Example:
        | ${orig timeout} = | Set Selenium Timeout | 15 seconds |
        | Open page that loads slowly |
        | Set Selenium Timeout | ${orig timeout} |
        """
        old_timeout = self.get_timeout()
        self._timeout_in_secs = robot.utils.timestr_to_secs(seconds)
        self._driver.set_script_timeout(self._timeout_in_secs)
        return old_timeout

    def get_page_title(self):
        """Returns title of current page."""
        return self._driver.title

    def get_element_value(self, locator):
        """Returns the value attribute of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._get_value(locator)

    def get_webelement(self, locator):
        """Returns the first WebElement matching the given locator.

        See `introduction` for details about locating elements.
        """
        return self._element_find(locator, True, True)

    def get_webelements(self, locator):
        """Returns list of WebElement objects matching locator.

        See `introduction` for details about locating elements.
        """
        return self._element_find(locator, False, True)

    def get_current_url(self):
        """Returns the current location."""
        return self._driver.current_url

    def is_element_present(self, locator, tag=None):
        """Check whether element present in current frame
        """
        return self._element_find(locator, True, False, tag) is not None

    def is_element_present_in_page(self, locator, tag=None):
        """Check whether element present in current page
        """
        def find_func():
            if self._element_find(locator, True, False, tag) is not None:
                return True

            return False

        return self._find_something_in_page(find_func)

    def is_text_present_in_page(self, text):
        """Check whether text present in current page
        """
        def find_func():
            if self._is_text_present(text):
                return True

            return False

        return self._find_something_in_page(find_func)

    def wait_until_element_contains(self, locator, text, timeout=None, error=None):
        element = self._element_find(locator, True, True)

        def check_text():
            actual = element.text
            if text in actual:
                return
            else:
                return error or "Text '%s' did not appear in %s to element '%s'. " \
                            "Its text was '%s'." % (text, self._format_timeout(timeout), locator, actual)

        return self._wait_until_no_error(timeout, check_text)

    def wait_until_element_does_not_contain(self, locator, text, timeout=None, error=None):
        element = self._element_find(locator, True, True)

        def check_text():
            actual = element.text
            if text not in actual:
                return
            else:
                return error or "Text '%s' did not disappear in %s from element '%s'." \
                                % (text, self._format_timeout(timeout), locator)
        return self._wait_until_no_error(timeout, check_text)

    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        def check_enabled():
            element = self._element_find(locator, True, False)
            if not element:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))

            enabled = not element.get_attribute("disabled")
            if enabled:
                return
            else:
                return error or "Element '%s' was not enabled in %s" % (locator, self._format_timeout(timeout))

        return self._wait_until_no_error(timeout, check_enabled)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        def check_visibility():
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" \
                                % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        return self._wait_until_no_error(timeout, check_visibility)

    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        def check_hidden():
            visible = self._is_visible(locator)
            if not visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" \
                                % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was still visible in %s" % (locator, self._format_timeout(timeout))
        return self._wait_until_no_error(timeout, check_hidden)

    def wait_until_page_contains_element(self, locator, timeout=None, error=None):
        def check_not_present():
            present = self.is_element_present(locator)
            if present:
                return
            else:
                return error or "Element '%s' did not disappear in %s" % (locator, self._format_timeout(timeout))

        return self._wait_until_no_error(timeout, check_not_present)

    def wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
        def check_present():
            present = self.is_element_present(locator)
            if not present:
                return
            else:
                return error or "Element '%s' did not disappear in %s" % (locator, self._format_timeout(timeout))
        return self._wait_until_no_error(timeout, check_present)

    def get_list_items(self, locator):
        select, options = self._get_select_list_options(locator)
        return self._get_labels_for_options(options)

    def get_selected_list_value(self, locator):
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute('value')

    def get_selected_list_values(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        if len(options) == 0:
            raise ValueError("Select list with locator '%s' does not have any selected values")
        return self._get_values_for_options(options)

    def get_selected_list_label(self, locator):
        select = self._get_select_list(locator)
        return select.first_selected_option.text

    def get_selected_list_labels(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        if len(options) == 0:
            raise ValueError("Select list with locator '%s' does not have any selected labels")
        return self._get_labels_for_options(options)

    def get_table_cell(self, table_locator, row, column):
        """Returns the content from a table cell.

        Row and column number start from 1. Header and footer rows are
        included in the count. A negative row or column number can be used
        to get rows counting from the end (end: -1). Cell content from header
        or footer rows can be obtained with this keyword. To understand how
        tables are identified, please take a look at the `introduction`.

        See `Page Should Contain` for explanation about `loglevel` argument.
        """
        cell = self._get_table_cell(table_locator, row, column)
        return cell.text

    def _get_table_cell(self, table_locator, row, column):
        """Returns the content from a table cell.

        Row and column number start from 1. Header and footer rows are
        included in the count. A negative row or column number can be used
        to get rows counting from the end (end: -1). Cell content from header
        or footer rows can be obtained with this keyword. To understand how
        tables are identified, please take a look at the `introduction`.

        See `Page Should Contain` for explanation about `loglevel` argument.
        """
        row = int(row)
        row_index = row
        if row > 0: row_index = row - 1
        column = int(column)
        column_index = column
        if column > 0: column_index = column - 1
        table = self._table_element_finder.find(self._driver, table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            if row_index >= len(rows) or row_index < 0:
                rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            if row_index >= len(rows) or row_index < 0:
                rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            if row_index < len(rows):
                columns = rows[row_index].find_elements_by_tag_name('th')
                if column_index >= len(columns) or column_index < 0:
                    columns.extend(rows[row_index].find_elements_by_tag_name('td'))
                if column_index < len(columns):
                    return columns[column_index]

        raise AssertionError("Cell in table %s in row #%s and column #%s could not be found." \
                             % (table_locator, str(row), str(column)))

    def get_table_cell_contains_content(self, table_locator, content):
        regexp = re.compile(content)
        rows = self._get_table_rows(table_locator)
        for i, row in enumerate(rows):
            columns = self._get_columns_by_row(row)
            for j, col in enumerate(columns):
                if regexp.match(col.text):
                    return [i+1, j+1]

        raise AssertionError("Table %s does not have any cell contains %s" % (table_locator, content))

    def get_table_cells_contains_content(self, table_locator, content):
        regexp = re.compile(content)
        ret_list = []
        rows = self._get_table_rows(table_locator)
        for i, row in enumerate(rows):
            columns = self._get_columns_by_row(row)
            for j, col in enumerate(columns):
                if regexp.match(col.text):
                    ret_list.append([i+1, j+1])

        if ret_list:
            return ret_list

        raise AssertionError("Table %s does not have any cell contains %s" % (table_locator, content))

    def get_element_attribute_from_table_cell(self, table_locator, row, column, attribute_locator):
        cell = self._get_table_cell(table_locator, row, column)
        locator, attribute_name = self._parse_attribute_locator(attribute_locator)
        elements = self._element_finder.find(cell, locator)
        if not elements:
            raise ValueError("Element '%s' not found." % locator)
        elem = elements[0]
        return elem.get_attribute(attribute_name)

    def get_table_rows_and_columns_count(self, table_locator):
        rows = self._get_table_rows(table_locator)
        if not rows:
            return [0, 0]

        row_len = len(rows)
        row = rows[0]
        columns = self._get_columns_by_row(row)
        if not columns:
            return [row_len, 0]

        column_len = len(columns)
        return [row_len, column_len]

    def _get_table_rows(self, table_locator):
        table = self._table_element_finder.find(self._driver, table_locator)
        if table is not None:
            rows = []
            for _path in ('./thead/tr', './tbody/tr', './tfoot/tr'):
                rows.extend(table.find_elements_by_xpath(_path))
            return rows

        raise AssertionError("Table %s could not be found." % table_locator)

    def _get_columns_by_row(self, row):
        columns = []
        for _path in ('th', 'td'):
            columns.extend(row.find_elements_by_tag_name(_path))
        return columns

    def input_text(self, locator, text):
        info("Typing text '%s' into text field '%s'" % (text, locator))
        self._input_text_into_text_field(locator, text)

    def submit_form(self, locator=None):
        info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        element = self._element_find(locator, True, True, 'form')
        element.submit()

    def select_from_list(self, locator, *items):
        """Selects `*items` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*items` is an empty list, all values of the list will be selected.

        *items try to select by value then by label.

        It's faster to use 'by index/value/label' functions.

        An exception is raised for a single-selection list if the last
        value does not exist in the list and a warning for all other non-
        existing items. For a multi-selection list, an exception is raised
        for any and all non-existing values.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        non_existing_items = []

        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)

        if not items:
            for i in range(len(select.options)):
                select.select_by_index(i)
            return

        for item in items:
            try:
                select.select_by_value(item)
            except Exception:
                try:
                    select.select_by_visible_text(item)
                except Exception:
                    non_existing_items = non_existing_items + [item]
                    continue

        if any(non_existing_items):
            if select.is_multiple:
                raise ValueError("Options '%s' not in list '%s'." % (", ".join(non_existing_items), locator))
            else:
                if any (non_existing_items[:-1]):
                    items_str = non_existing_items[:-1] and "Option(s) '%s'" % ", ".join(non_existing_items[:-1])
                    warn("%s not found within list '%s'." % (items_str, locator))
                if items and items[-1] in non_existing_items:
                    raise ValueError("Option '%s' not in list '%s'." % (items[-1], locator))

    def select_from_list_by_index(self, locator, *indexes):
        """Selects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not indexes:
            raise ValueError("No index given.")
        items_str = "index(es) '%s'" % ", ".join(indexes)
        info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    def select_from_list_by_value(self, locator, *values):
        """Selects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not values:
            raise ValueError("No value given.")
        items_str = "value(s) '%s'" % ", ".join(values)
        info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    def select_from_list_by_label(self, locator, *labels):
        """Selects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not labels:
            raise ValueError("No value given.")
        items_str = "label(s) '%s'" % ", ".join(labels)
        info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    def select_radio_button(self, group_name, value):
        """Sets selection of radio button group identified by `group_name` to `value`.

        The radio button to be selected is located by two arguments:
        - `group_name` is used as the name of the radio input
        - `value` is used for the value attribute or for the id attribute

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        Examples:
        | Select Radio Button | size | XL | # Matches HTML like <input type="radio" name="size" value="XL">XL</input> |
        | Select Radio Button | size | sizeXL | # Matches HTML like <input type="radio" name="size" value="XL" id="sizeXL">XL</input> |
        """
        info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    def unselect_checkbox(self, locator):
        info("Unselecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            info('Element %s is selected, click it to unselecting' % locator)
            element.click()
        else:
            info('Element %s is unselected' % locator)

    def select_frame(self, locator):
        """Sets frame identified by `locator` as current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        info("Selecting frame '%s'." % locator)
        element = self._element_find(locator, True, True)
        self._driver.switch_to_frame(element)

    def unselect_frame(self):
        """Sets the top frame as the current frame."""
        self._driver.switch_to_default_content()

    def current_frame_contains(self, text):
        """Verifies that current frame contains `text`.
        """
        if not self._is_text_present(text):
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        info("Current page contains text '%s'." % text)

    def current_frame_should_not_contain(self, text):
        """Verifies that current frame contains `text`.

        """
        if self._is_text_present(text):
            raise AssertionError("Page should not have contained text '%s' "
                                 "but it did" % text)
        info("Current page should not contain text '%s'." % text)

    def frame_should_contain(self, locator, text):
        """Verifies frame identified by `locator` contains `text`.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        if not self._frame_contains(locator, text):
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        info("Current page contains text '%s'." % text)

    def delete_all_cookies(self):
        self._driver.delete_all_cookies()

    def click_alert_ok_button(self):
        return self._close_alert(True)

    def click_alert_cancel_button(self):
        return self._close_alert(False)

    def get_radio_button_value(self, group_name):
        """Get the value of selected radio button
        """
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_attribute_from_radio_buttons(elements, 'value')
        return actual_value

    def get_radio_button_id(self, group_name):
        elements = self._get_radio_buttons(group_name)
        actual_id = self._get_attribute_from_radio_buttons(elements, 'id')
        return actual_id

    def capture_page_screenshot(self, filename=None):
        """Capture a screenshot of current page and return the link of the screenshot picture
        """
        path, link = self._get_screenshot_paths(filename)
        self._create_directory(path)

        if not self._driver.get_screenshot_as_file(path):
            raise RuntimeError('Failed to save screenshot ' + filename)

        info('capture page screenshot and save to %s' % link)
        return link

    def execute_javascript(self, *code):
        js = self._get_javascript_to_execute(''.join(code))
        info("Executing JavaScript:\n%s" % js)
        return self._driver.execute_script(js)

    def reload_page(self):
        self._driver.refresh()

    def need_capture_screenshot_after_keyword_execution(self):
        return self._screenshot_mode == ScreenshotMode.ALL


    ### Private ###
    def _get_driver(self, browser_type):
        if browser_type is None:
            browser_type = 'FireFox'
        from cafe.sessions.util.webgui.browser.builder import BrowserBuilder
        browser = BrowserBuilder(browser_type).build(session_name=self.sid,
                                                     session_logger=self.session_log,
                                                     implicit_wait_in_secs=self._implicit_wait_in_secs,
                                                     speed_in_secs=self._speed_in_secs,
                                                     timeout_in_secs=self._timeout_in_secs,
                                                     browser_options=self._driver_args)
        browser_type = browser.type
        browser = browser.get_real_browser()

        for logger in (self.logger.info, self.session_log.info):
            logger("%s browser is used" % browser_type)
            logger("%s session id: %s" % (browser_type, browser.session_id))

        return browser

    def _element_find(self, locator, first_only, required, tag=None):
        browser = self._driver
        if isinstance(locator, basestring):
            elements = self._element_finder.find(browser, locator, tag)
            if required and len(elements) == 0:
                raise ValueError("Element locator '" + locator + "' did not match any elements.")
            if first_only:
                debug('element_find, found %d elements, just need first one' % len(elements))
                if len(elements) == 0: return None
                debug('found element %s' % elements[0])
                return elements[0]
        elif isinstance(locator, WebElement):
            elements = locator
        # do some other stuff here like deal with list of webelements
        # ... or raise locator/element specific error if required
        debug('element_find, found %d elements' % len(elements))
        for elem in elements:
            debug('found element %s' % elem)
        return elements

    def _is_form_element(self, element):
        if element is None:
            return False
        tag = element.tag_name.lower()
        return tag == 'input' or tag == 'select' or tag == 'textarea' or tag == 'button' or tag == 'option'

    def _parse_attribute_locator(self, attribute_locator):
        parts = attribute_locator.rpartition('@')
        if len(parts[0]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an element locator." % (attribute_locator))
        if len(parts[2]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an attribute name." % (attribute_locator))
        return (parts[0], parts[2])

    def _get_value(self, locator, tag=None):
        element = self._element_find(locator, True, False, tag=tag)
        return element.get_attribute('value') if element is not None else None

    def _wait_until_no_error(self, timeout, wait_func, *args):
        timeout = timeout if timeout is not None else self._timeout_in_secs
        start_time = time.time()
        maxtime = start_time + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return time.time() - start_time

            if time.time() > maxtime:
                raise AssertionError(timeout_error)

            time.sleep(0.2)

    def _format_timeout(self, timeout):
        timeout = timeout if timeout is not None else self._timeout_in_secs
        return robot.utils.secs_to_timestr(timeout)

    def _is_visible(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            try:
                return element.is_displayed()
            except StaleElementReferenceException:
                # When we access the element, it is not existed
                return None
        return None

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, Select):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.options

    def _get_select_list(self, locator):
        el = self._element_find(locator, True, True, 'select')
        return Select(el)

    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels

    def _get_select_list_options_selected(self, locator):
        select = self._get_select_list(locator)
        # TODO: Handle possible exception thrown by all_selected_options
        return select, select.all_selected_options

    def _get_values_for_options(self, options):
        values = []
        for option in options:
             values.append(option.get_attribute('value'))
        return values

    def _input_text_into_text_field(self, locator, text):
        element = self._element_find(locator, True, True)
        element.clear()
        element.send_keys(text)

    def _get_radio_button_with_value(self, group_name, value):
        xpath = "xpath=//input[@type='radio' and @name='%s' and (@value='%s' or @id='%s')]" \
                 % (group_name, value, value)
        debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, True, True)

    def _get_checkbox(self, locator):
        return self._element_find(locator, True, True, tag='input')

    def _is_text_present(self, text):
        """Check whether text present in current frame
        """
        locator = "xpath=//*[contains(., %s)]" % self._escape_xpath_value(text)
        return self.is_element_present(locator)

    def _escape_xpath_value(self, value):
        value = unicode(value)
        if '"' in value and '\'' in value:
            parts_wo_apos = value.split('\'')
            return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
        if '\'' in value:
            return "\"%s\"" % value
        return "'%s'" % value

    def _frame_contains(self, locator, text):
        browser = self._driver
        element = self._element_find(locator, True, True)
        browser.switch_to_frame(element)
        info("Searching for text from frame '%s'." % locator)
        found = self._is_text_present(text)
        browser.switch_to_default_content()
        return found

    def _close_alert(self, confirm=True):
        try:
            text = self._read_alert()
            alert = self._handle_alert(confirm)
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _read_alert(self):
        alert = None
        try:
            alert = self._driver.switch_to_alert()
            text = ' '.join(alert.text.splitlines()) # collapse new lines chars
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _handle_alert(self, confirm=True):
        try:
            alert = self._driver.switch_to_alert()
            if not confirm:
                alert.dismiss()
                return False
            else:
                alert.accept()
                return True
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _get_radio_buttons(self, group_name):
        xpath = "xpath=//input[@type='radio' and @name='%s']" % group_name
        debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, False, True)

    def _get_attribute_from_radio_buttons(self, elements, attribute):
        for element in elements:
            if element.is_selected():
                return element.get_attribute(attribute)
        return None

    def _get_screenshot_paths(self, filename):
        if not filename:
            filename = 'selenium-screenshot-%s-%d.png' % \
                       (time.strftime("%Y%m%d%H%M%S"), self._screenshot_index_generator.next())
        else:
            filename = filename.replace('/', os.sep)

        screenshotDir = self._get_screenshot_directory()
        logDir = self._get_log_dir()
        path = os.path.join(screenshotDir, filename)
        link = robot.utils.get_link_path(path, logDir)
        return path, link

    def _get_screenshot_directory(self):
        return self._get_log_dir()

    def _get_log_dir(self):
        try:
            variables = BuiltIn().get_variables()
            return variables['${OUTPUTDIR}']
        except RobotNotRunningError:
            return os.getcwd()

    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else:
                    raise

    def _find_something_in_page(self, find_func):
        """Check whether element present in current page
        """
        self._driver.switch_to_default_content()
        if find_func():
            return True

        subframes = self._element_find("xpath=//frame|//iframe", False, False)
        debug('Current frame has %d subframes' % len(subframes))
        for frame in subframes:
            self._driver.switch_to_frame(frame)
            ret = find_func()
            self._driver.switch_to_default_content()
            if ret:
                return True

        return False

    def _get_javascript_to_execute(self, code):
        codepath = code.replace('/', os.sep)
        if not (os.path.isabs(codepath) and os.path.isfile(codepath)):
            return code
        debug('Reading JavaScript from file <a href="file://%s">%s</a>.'
                   % (codepath.replace(os.sep, '/'), codepath))
        codefile = open(codepath)
        try:
            return codefile.read().strip()
        finally:
            codefile.close()

if __name__ == "__main__":
    from selenium.webdriver.common.keys import Keys
    from cafe.core.logger import init_logging

    init_logging()

    session = WebGuiSession(sid="123", logfile="web.log")
    #print(session.driver.capabilities)
    session.open_browser()

    session.driver.get("http://www.python.org")

    assert "Python" in session.driver.title
    elem = session.driver.find_element_by_name("q")
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in session.driver.page_source
    import time
    time.sleep(5)
    session.close()
