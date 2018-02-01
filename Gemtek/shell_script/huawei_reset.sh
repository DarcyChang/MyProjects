#!/bin/sh

huawei_vid='12d1'
huawei_pid=$(lsusb | grep 'Huawei' | cut -d ' ' -f6 | cut -d ':' -f2)
echo huawei_vid $huawei_vid
echo huawei_pid $huawei_pid

echo "0 4 1 7" > /proc/sys/kernel/printk

at-cmd /dev/ttyUSB0 at^tmode=3 &
sleep 2

rm /tmp/at_no_response
killall at-cmd
sleep 2

rmmod option
rmmod option
sleep 2

modprobe option
sleep 2

echo $huawei_vid $huawei_pid > /sys/bus/usb-serial/drivers/option1/new_id
sleep 2

echo "4 4 1 7" > /proc/sys/kernel/printk

hotplug pincode
