#!/bin/bash
echo 1 > /sys/devices/platform/nct6775.512/wdt/enable
echo 20 > /sys/devices/platform/nct6775.512/wdt/timer
halt
