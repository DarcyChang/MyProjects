#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cafe.core.logger import CLogger

__author__ = 'David Qian'

"""
Created on 05/04/2016
@author: David Qian

"""

_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warn
error = _module_logger.error


class BaseBrowser(object):
    def __init__(self, session_name, session_logger, implicit_wait_in_secs, speed_in_secs, timeout_in_secs, browser_options):
        self._session_name = session_name
        self._session_logger = session_logger
        self._instance = self._create_real_browser(**browser_options)
        self._set_browser_window_size(browser_options.get('width', 1920), browser_options.get('height', 1080))
        # set selenium parameter
        self._instance.implicitly_wait(implicit_wait_in_secs)
        self._instance.set_speed(speed_in_secs)
        self._instance.set_script_timeout(timeout_in_secs)
        info('create webgui browser %s with type %s' % (self._session_name, self.type))
        info('selenium parameter: implicit_wait=%fsecs, execute_speed=%fsecs, timeout=%fsecs'
             % (implicit_wait_in_secs, speed_in_secs, timeout_in_secs))

    def _create_real_browser(self, **browser_options):
        raise NotImplementedError

    def get_real_browser(self):
        return self._instance

    @property
    def type(self):
        return self.__class__.__name__

    def _set_browser_window_size(self, width, height):
        self._instance.set_window_size(width, height)
