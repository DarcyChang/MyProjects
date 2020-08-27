#!/bin/bash
# Author Darcy.Chang
# Date 2020.08.06
# Version 1.0.0

echo "10" > /proc/suio_gpio
i2cset -y 0 0x21 0x07 0x00

/root/MFG/ctl_led.sh echo on
