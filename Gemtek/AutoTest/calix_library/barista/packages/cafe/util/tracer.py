#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from decorator import decorator

from cafe.core.logger import CLogger

__author__ = 'David Qian'

"""
Created on 08/15/2016
@author: David Qian

"""


_module_logger = CLogger(__name__)

debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


@decorator
def time_tracer(func, *args, **kwargs):
    func_name = func.__name__

    debug("Enter %s" % func_name)
    start_time = time.time()
    ret_value = func(*args, **kwargs)
    end_time = time.time()
    debug("Exit %s, takes %f secs." % (func_name, end_time - start_time))
    return ret_value
