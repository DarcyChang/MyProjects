#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver

from cafe.core.logger import CLogger
from cafe.sessions.util.webgui.browser.base import BaseBrowser

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


class Chrome(BaseBrowser):
    def _create_real_browser(self, **browser_options):
        return webdriver.Chrome()

