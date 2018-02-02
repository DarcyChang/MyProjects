#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cafe.sessions.util.webgui.browser.chrome import Chrome
from cafe.sessions.util.webgui.browser.firefox import Firefox

from cafe.core.logger import CLogger
from cafe.sessions.util.webgui.browser.phantomjs import PhantomJS

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


class BrowserBuilder(object):
    CREATORS = {
        'FIREFOX': Firefox,
        'FF': Firefox,
        'GOOGLECHROME': Chrome,
        'GC': Chrome,
        'CHROME': Chrome,
        'PHANTOMJS': PhantomJS,
    }

    def __init__(self, browser_type):
        self._builder = self._get_builder(browser_type)

    def build(self, **browser_options):
        return self._builder(**browser_options)

    def _get_builder(self, browser_type):
        browser_type = browser_type.upper()
        if browser_type in self.CREATORS:
            return self.CREATORS[browser_type]

        # unknown browser type
        warn('%s is not support yet. FireFox browser is used instead' % browser_type)
        browser_type = 'FIREFOX'
        return self.CREATORS[browser_type]
