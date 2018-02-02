#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

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


class Firefox(BaseBrowser):
    def _create_real_browser(self, **browser_options):
        firefox_profile = None
        if 'firefox_profile' in browser_options:
            firefox_profile = self._load_profile(browser_options['firefox_profile'])

        if 'auto_download' in browser_options:
            firefox_profile = self._config_auto_download(browser_options['auto_download'], firefox_profile)

        return webdriver.Firefox(firefox_profile=firefox_profile)

    def _load_profile(self, profile_config):
        info('firefox_profile: %s' % profile_config)
        self._session_logger.info('firefox_profile: %s' % profile_config)
        return FirefoxProfile(profile_config)

    def _config_auto_download(self, download_opt, ff_profile):
        if not ff_profile:
            ff_profile = webdriver.FirefoxProfile()

        download_dir = download_opt['dir']
        download_file_types = download_opt['types']
        if isinstance(download_file_types, (str, unicode)):
            download_file_types = [download_file_types]

        ff_profile.set_preference("browser.download.folderList", 2)
        ff_profile.set_preference("browser.download.manager.showWhenStarting", False)
        ff_profile.set_preference("browser.download.dir", download_dir)
        ff_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ','.join(download_file_types))

        return ff_profile



















