#!/bin/bash
# Authot Darcy.Chang
# Date 2020.08.05
# Version 1.1.0

#echo "10" > /proc/suio_gpio | tee -a /root/MFG/logs/log.txt
#i2cset -y 0 0x21 0x07 0x00

while true
do
	/root/MFG/ctl_led.sh bi on
	sleep 0.3
	/root/MFG/ctl_led.sh bi off
	sleep 0.3
done
