#!/bin/bash

bus_num=$(/root/i2c_bus.sh)
if [ "$bus_num" == 2 ] ; then
	i2cset -y 0 0x77 0x01
else
	i2cset -y 12 0x77 0x01
fi
