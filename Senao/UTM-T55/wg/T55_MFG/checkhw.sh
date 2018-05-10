#!/bin/bash

HOSTNAME=$(hostname)

/root/automation/T55_MFG/hwconfig 2> /dev/null | grep Processors > /root/processors 
/root/automation/T55_MFG/hwconfig 2> /dev/null | grep Memory > /root/memory
/root/automation/T55_MFG/hwconfig 2> /dev/null | grep Disk: > /root/disk
/root/automation/T55_MFG/hwconfig 2> /dev/null | grep Network > /root/network
cat /sys/class/dmi/id/bios_version > /root/bios_version

if grep -q '1 x Celeron N3060 1.60GHz (2 cores)' /root/processors
then
echo CPU check ok
else
echo CPU check fail
fi

if grep -q '1.8GB' /root/memory
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


if  grep -q 'eth0 (dsa)' /root/network 
then
echo Network check ok
else
echo Network check fail
fi

t55w=$(/root/automation/T55_MFG/readmfg wg | grep -q "wg: D023" && echo T55-W || echo T55)
if [[ $t55w == "T55-W" ]] ; then
    lspci -k > /root/wifi

    if  grep -q 'ath10k_pci' /root/wifi
    then
        echo Wi-Fi check ok
    else
		echo Wi-Fi check fail
    fi
fi

if grep -q '77.05' /root/bios_version
then 
echo BIOS version 77.05
else
echo BIOS vesrion check fail
fi

rm /root/processors /root/memory /root/disk /root/network 
if [ "$HOSTNAME" == "WatchGuard-XTM" ]; then
   rm /root/wifi
fi
rm /root/bios_version

exit 0
