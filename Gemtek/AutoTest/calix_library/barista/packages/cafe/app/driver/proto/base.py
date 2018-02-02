#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Qian'
from cafe.core.exceptions.app.driver import DriverMethodNotImplementError

"""
Created on 01/11/2016
@author: David Qian

"""
class DriverBase(object):

    def is_reachable(self):
        """Return True if Driver/device is reachable

        Reachable behavior should be device/connection type specific
        For example:
            - in the context of ssh device,
            reachable means ping between
            the device and Cafe VM should work

            - in the context of ixia device,
            reachable means ping between
            Cafe VM and ixia connection server should work, and
            the ping between Cafe VM and ixia chassis should work

        """
        raise DriverMethodNotImplementError()

    def is_connected(self):
        """Return True if Driver/device is connected

        connected behavior should be device/connection type specific
        For example:
            - in the context of ssh device,
            "connected" means ssh login to the device is completed

            - in the context of ixia device,
            "connected" means ixia library loaded and ixia ports are reserved.

        """
        raise DriverMethodNotImplementError()

    def open_handle(self):
        """Open handle, this method should be called in TestCase's setup

        Returns:

        """
        raise DriverMethodNotImplementError()

    def close_handle(self):
        """Close handle, this method should be called in TestCase's teardown

        Returns:

        """
        raise DriverMethodNotImplementError()

    def disconnect(self):
        """Disconnect the real connection to server

        Returns:

        """
        raise DriverMethodNotImplementError()

