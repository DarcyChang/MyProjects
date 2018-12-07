#!/bin/bash

usb_count=3
modem_count=1
sim_count=1
sata_count=1

./hwconfig 2> /dev/null > /tmp/hw_info

disk_list=`fdisk -l | grep Disk | grep /dev/ | cut -d' ' -f2 | sed 's/://g'`
rm -f /tmp/disk_devpath_tmp
for disk in $disk_list; do
    udevadm info $disk 2> /dev/null | grep DEVPATH | cut -d/ -f5 >> /tmp/disk_devpath_tmp
done

disk_ok=1

detected_count=`grep usb /tmp/disk_devpath_tmp -c`
if [ $detected_count -lt $usb_count ]; then
    echo USB check fail
    disk_ok=0
else
    echo USB check ok
fi

if [ "$disk_ok" != "1" ]; then
    cat /tmp/hw_info | grep Disk:
    exit_code=1
fi

count=`mmcli -L | grep Modem/0 -c`
if [ $count -lt $modem_count ]; then
    echo LTE Modem check fail
    exit_code=1
else
    echo LTE Modem check ok
fi

count=`mmcli -m 0 | grep SIM/ -c`
if [ $count -lt $sim_count ]; then
    echo SIM Card check fail
    exit_code=1
else
    echo SIM Card check ok
fi

echo "Test audio..."
./audio_test.sh mic 
