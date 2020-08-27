#!/bin/bash

echo "10" > /proc/suio_gpio 
i2cset -y 0 0x21 0x07 0x00
i2cset -y 0 0x21 0x03 0xFF
i2cset -y 0 0x21 0x03 0xEF
i2cset -y 0 0x21 0x03 0xCF
i2cset -y 0 0x21 0x03 0x0F
ifconfig eth0 up
ifconfig eth0 192.168.1.100
ping 192.168.1.10 -c 5
dmidecode -t processor | grep C3558
dmidecode -t processor | grep "Core Count"
dmidecode -t processor | grep "Thread Count"
dmidecode -t 17 | grep 8192
