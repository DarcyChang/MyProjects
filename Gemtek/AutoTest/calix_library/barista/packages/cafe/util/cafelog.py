#!/usr/bin/env python
# -*- coding: utf-8 -*-
from robot.api import logger as robot_logger

from cafe.core.logger import CLogger

__author__ = 'David Qian'

"""
Created on 08/22/2016
@author: David Qian

"""


_module_logger = CLogger(__name__)
trace = _module_logger.trace
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warning
error = _module_logger.error
exception = _module_logger.exception


def is_string(item):
    return isinstance(item, basestring)


def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '')
    return bool(item)


def cafelog(message, level='INFO', console=True):
    """User can use this function to log message

    Args:
        message:  log message content
        level: log level
        console: whether output to console


    """
    log_func = {
        'TRACE': trace,
        'DEBUG': debug,
        'INFO': info,
        'WARN': warn,
        'ERROR': error,
        'EXCEPTION': exception,
    }[level]

    log_func(message)

    if is_truthy(console):
        robot_logger.console(message)
