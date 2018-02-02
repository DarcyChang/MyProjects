#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from decorator import decorator
from cafe.core.logger import CLogger
from .proto.base import DriverBase

__author__ = 'David Qian'

"""
Created on 01/04/2016
@author: David Qian

"""

_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warn
error = _module_logger.error


@decorator
def forward_to_session(func, instance, *args, **kwargs):
    m = getattr(instance._session, func.__name__)
    if callable(m):
        result = m(*args, **kwargs)
    else:
        result = m

    return result


class WebGuiDriver(DriverBase):
    def __init__(self, session=None, name=None, app=None):
        self._session = session
        self.name = name
        self.app = app

    def open_browser(self):
        self._session.open_browser()

    def close_browser(self):
        self._session.close_browser()

    def close(self):
        self._session.close()

    @forward_to_session
    def go_to_page(self, url):
        """
        Loads a web page in the current browser session.
        """
        pass

    @forward_to_session
    def add_cookie(self, name, value, path=None, domain=None, secure=None, expiry=None):
        pass

    @forward_to_session
    def get_cookie(self, name):
        pass

    @forward_to_session
    def get_checkbox(self, locator):
        pass

    @forward_to_session
    def choose_file(self, locator, file_path):
        pass

    @forward_to_session
    def click_element(self, locator):
        pass

    @forward_to_session
    def click_visible_element(self, locator):
        pass

    @forward_to_session
    def delete_cookie(self, name):
        pass

    @forward_to_session
    def double_click_element(self, locator):
        pass

    @forward_to_session
    def drag_and_drop(self, source, target):
        pass

    @forward_to_session
    def is_element_enable(self, locator):
        pass

    @forward_to_session
    def is_element_visible(self, locator):
        pass

    @forward_to_session
    def get_element_text(self, locator):
        pass

    @forward_to_session
    def get_element_attribute(self, attribute_locator):
        pass

    @forward_to_session
    def get_implicit_wait_time(self):
        pass

    @forward_to_session
    def set_implicit_wait_time(self, seconds):
        pass

    @forward_to_session
    def get_execute_speed(self):
        pass

    @forward_to_session
    def set_execute_speed(self, seconds):
        pass

    @forward_to_session
    def get_timeout(self):
        pass

    @forward_to_session
    def set_timeout(self, seconds):
        pass

    @forward_to_session
    def get_page_title(self):
        pass

    @forward_to_session
    def get_element_value(self, locator):
        pass

    @forward_to_session
    def get_webelement(self, locator):
        pass

    @forward_to_session
    def get_webelements(self, locator):
        pass

    @forward_to_session
    def get_current_url(self):
        pass

    @forward_to_session
    def is_element_present(self, locator, tag=None):
        pass

    @forward_to_session
    def is_element_present_in_page(self, locator, tag=None):
        pass

    @forward_to_session
    def is_text_present_in_page(self, text):
        pass

    @forward_to_session
    def wait_until_element_contains(self, locator, text, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_element_does_not_contain(self, locator, text, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_element_is_enabled(self, locator, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_element_is_not_visible(self, locator, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_page_contains_element(self, locator, timeout=None, error=None):
        pass

    @forward_to_session
    def wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
        pass

    @forward_to_session
    def get_list_items(self, locator):
        pass

    @forward_to_session
    def get_selected_list_value(self, locator):
        pass

    @forward_to_session
    def get_selected_list_values(self, locator):
        pass

    @forward_to_session
    def get_table_cell(self, table_locator, row, column):
        pass

    @forward_to_session
    def input_text(self, locator, text):
        pass

    @forward_to_session
    def submit_form(self, locator=None):
        pass

    @forward_to_session
    def select_from_list(self, locator, *items):
        pass

    @forward_to_session
    def select_from_list_by_index(self, locator, *indexes):
        pass

    @forward_to_session
    def select_from_list_by_value(self, locator, *values):
        pass

    @forward_to_session
    def select_from_list_by_label(self, locator, *labels):
        pass

    @forward_to_session
    def select_radio_button(self, group_name, value):
        pass

    @forward_to_session
    def select_checkbox(self, locator):
        pass

    @forward_to_session
    def unselect_checkbox(self, locator):
        pass

    @forward_to_session
    def select_frame(self, locator):
        pass

    @forward_to_session
    def unselect_frame(self):
        pass

    @forward_to_session
    def current_frame_contains(self, text):
        pass

    @forward_to_session
    def current_frame_should_not_contain(self, text):
        pass

    @forward_to_session
    def frame_should_contain(self, locator, text):
        pass

    @forward_to_session
    def delete_all_cookies(self):
        pass

    @forward_to_session
    def click_alert_ok_button(self):
        pass

    @forward_to_session
    def click_alert_cancel_button(self):
        pass

    @forward_to_session
    def get_radio_button_value(self, group_name):
        pass

    @forward_to_session
    def get_radio_button_id(self, group_name):
        pass

    @forward_to_session
    def capture_page_screenshot(self, filename=None):
        pass

    @forward_to_session
    def get_selected_list_label(self, locator):
        pass

    @forward_to_session
    def get_selected_list_labels(self, locator):
        pass

    @forward_to_session
    def get_table_cell_contains_content(self, table_locator, content):
        pass

    @forward_to_session
    def get_table_cells_contains_content(self, table_locator, content):
        pass

    @forward_to_session
    def get_element_attribute_from_table_cell(self, table_locator, row, column, attribute_locator):
        pass

    @forward_to_session
    def execute_javascript(self, *code):
        pass

    @forward_to_session
    def reload_page(self):
        pass

    @forward_to_session
    def get_table_rows_and_columns_count(self, table_locator):
        pass

    @forward_to_session
    def need_capture_screenshot_after_keyword_execution(self):
        pass