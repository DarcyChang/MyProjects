#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Qian'

"""
Created on 07/06/2016
@author: David Qian

"""


class ScreenshotMode(object):
    FAIL = 0
    ALL = 1

    @classmethod
    def get_screenshot_mode(cls, mode):
        d = {
            'FAIL': cls.FAIL,
            'ALL': cls.ALL,
        }

        return d.get(mode.upper(), cls.FAIL)
