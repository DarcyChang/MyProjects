#!/bin/bash

while [ 1 ]
do
#	hdparm -t /dev/sda
#	hdparm -t --direct /dev/sda
	/root/pre_test.sh
	/root/memory_detect.sh
	i2cset -y 0 0x25 0x06 0xFF
	sleep 1
done
