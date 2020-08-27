#!/bin/bash
# Author Darcy.Chang
# Date 2020.08.31
# Version 1.0.0



rmmod igb
rmmod i2c_ismt
modprobe i2c-i801
modprobe igb
insmod /root/superio_smbus/suio_smbus.ko
#i2cset -y 0 0x77 0x01
#/root/i2c_init.sh

#echo 0 > /proc/sys/kernel/hung_task_timeout_secs

#iperf -s -D -w 512k
#iperf -s -D -u -w 512k

#i2cset -y 0 0x77 0x02
#i2cset -y 0 0x22 0x02 0xFF
#i2cset -y 0 0x22 0x06 0x19

#/root/MFG/prepare.sh
#/root/MFG/sys_led.sh
#/root/MFG/ping.sh
#/root/MFG/stress.sh -t 3600
#/root/MFG/result.sh
