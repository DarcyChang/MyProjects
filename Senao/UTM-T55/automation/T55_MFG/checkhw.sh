#!/bin/bash

HOSTNAME=$(hostname)

/root/automation/T55_MFG/hwconfig | grep Processors > /root/processors 
/root/automation/T55_MFG/hwconfig | grep Memory > /root/memory
/root/automation/T55_MFG/hwconfig | grep Disk: > /root/disk
/root/automation/T55_MFG/hwconfig | grep Network > /root/network
cat /sys/class/dmi/id/bios_version > /root/bios_version

if grep -q '1 x Celeron N3060 1.60GHz 80MHz FSB (2 cores)' /root/processors
then
echo CPU check ok
else
echo CPU check fail
fi

if grep -q '1.9GB / 2GB 1600MHz DDR3 == 1 x 2GB' /root/memory
then
echo Memory check ok
else
echo Memory check fail
fi

if grep -q 'sda' /root/disk && 
   grep -q 'sdb' /root/disk && 
   grep -q 'sdc' /root/disk
then
echo Disk check ok
else
if grep -q 'sda' /root/disk
then
echo USB check fail
else
echo Disk check fail
fi
fi


if  grep -q 'eth0 (igb): Intel I210 Gigabit Backplane Connection' /root/network 
then
echo Network check ok
else
echo Network check fail
fi

if [ "$HOSTNAME" == "T55-wifi" ]; then
    lspci > /root/wifi

    if  grep -q 'Qualcomm Atheros QCA986x/988x 802.11ac Wireless Network Adapter' /root/wifi
    then
        echo Wi-Fi check ok
    else
		echo Wi-Fi check fail
    fi
fi

if grep -q '73.10' /root/bios_version
then 
echo BIOS version 73.10
else
echo BIOS vesrion check fail
fi

rm /root/processors /root/memory /root/disk /root/network 
if [ "$HOSTNAME" == "T55-wifi" ]; then
   rm /root/wifi
fi
rm /root/bios_version

exit 0
