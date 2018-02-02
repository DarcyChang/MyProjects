#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from time import sleep

from caferobot.command.device.shell import ShellDevice

__author__ = 'David Qian'

"""
Created on 03/01/2016
@author: David Qian

"""
from cafe.core.logger import CLogger

_logger = CLogger()
debug = _logger.debug
info = _logger.info
warn = _logger.warn
error = _logger.error


class SerialPort(object):
    def _get_lan_gateway_from_serial_port(self, connection_name):
        device = ShellDevice(connection_name)
        result = device.command('lan show')['content']
        debug('result is ' + result)
        m = re.search(r'inet addr:(\d+\.\d+\.\d+\.\d+)', result)
        if m:
            ip_addr = m.group(1)
            info('gateway ip is: %s' % ip_addr)
            return ip_addr

        return None

    def get_lan_gateway_from_serial_port(self, connection_name):
        ip_addr = self._get_lan_gateway_from_serial_port(connection_name)
        if ip_addr:
            return ip_addr

        raise RuntimeError('get_lan_gateway_from_serial_port fail')

    def _wait_trunk_able_to_execute_command(self, connection_name, retry_time=10):
        debug('wait trunk able to execute command, check %d times' % retry_time)
        for i in range(retry_time):
            debug('try %d time...' % i)
            try:
                device = ShellDevice(connection_name)
                result = device.command('uptime', [], timeout_exception=0)['content']
                if re.search(r'0D 0H ', result):
                    info('wait trunk able to execute command, command executed succeed')
                    return True
            except:
                pass

            sleep(5)

        error('wait trunk able to execute command, command executed failed')
        return False

    def wait_trunk_able_to_execute_command(self, connection_name, retry_time=10):
        if not self._wait_trunk_able_to_execute_command(connection_name, int(retry_time)):
            raise RuntimeError('wait_trunk_able_to_execute_command fail')



def foo():
    s = """br0       Link encap:Ethernet  HWaddr 00:06:31:ED:E7:5A
          inet addr:192.168.1.3  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING ALLMULTI MULTICAST  MTU:1500  Metric:1
          RX packets:4272 multicast:583 unicast:3675 broadcast:14
          RX errors:0 dropped:0 overruns:0 frame:0
          TX packets:2746 multicast:0 unicast:2746 broadcast:0
          TX errors:0 dropped:0 overruns:0 carrier:0 collisions:0
          txqueuelen:0
          RX bytes:624060 (609.4 KiB) TX bytes:801915 (783.1 KiB)
          RX multicast bytes:195978 (191.3 KiB) TX multicast bytes:0 (0.0 B)

br0:0     Link encap:Ethernet  HWaddr 00:06:31:ED:E7:5A
          UP BROADCAST RUNNING ALLMULTI MULTICAST  MTU:1500  Metric:1"""

    m = re.search(r'inet addr:(\d+\.\d+\.\d+\.\d+)', s)
    print m.group(1)


if __name__ == '__main__':
    foo()

