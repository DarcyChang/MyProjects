#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cafe.core.logger import CLogger
from cafe.core.signals import GENERATOR_INVALID_EXPRESSION, GENERATOR_INVALID_PARAMETER, \
    GENERATOR_INVALID_POOL_EXPRESSION

__author__ = 'David Qian'

"""
Created on 08/11/2016
@author: David Qian

"""

_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warning
exception = _module_logger.exception
error = _module_logger.error


class InvalidGeneratorExpression(Exception):
    def __init__(self, msg='', log=False):
        if log:
            _module_logger.exception(msg, signal=GENERATOR_INVALID_EXPRESSION)


class InvalidGeneratorParameter(Exception):
    def __init__(self, msg=''):
        _module_logger.exception(msg, signal=GENERATOR_INVALID_PARAMETER)


class InvalidGeneratorPoolExpression(Exception):
    def __init__(self, msg=''):
        _module_logger.exception(msg, signal=GENERATOR_INVALID_POOL_EXPRESSION)



