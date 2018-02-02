#!/usr/bin/env python
# -*- coding: utf-8 -*-
from robot.libraries.BuiltIn import _Misc

__author__ = 'David Qian'

"""
Created on 08/25/2016
@author: David Qian

"""


class RobotLogMonkeyPatches(object):
    _Misc._log_patch = _Misc.log

    def log(self, message, level='INFO', html=False, console=True, repr=False):
        self._log_patch(message, level, html, console, repr)

    _Misc.log = log