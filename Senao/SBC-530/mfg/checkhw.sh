#!/bin/bash

cpu="N4200\|N3350"
memory="1 x 8GB"
monitor_count=2
usb_count=6
msata_count=1
sata_count=1 # sata
emmc_count=0 # mmcblk0
m2_count=1
modem_count=1
sim_count=1
nic_count=2
nic_name="I210\|I211"
exit_code=0

monitor_check=1
m2_check=1
msata_check=1
sata_check=1
modem_check=1

while [[ $# > 0 ]]
do
key="$1"
case $key in
    --cpu)
    cpu="$2"
    shift
    ;;
    --memory)
    memory="$2"
    shift
    ;;
    --emmc)
    emmc_count=1
    ;;
    --monitor_count)
    monitor_count="$2"
    shift
    ;;
    --no_monitor)
    monitor_check=0
    ;;
    --usb_count)
    usb_count="$2"
    shift
    ;;
    --msata_count)
    msata_count="$2"
    shift
    ;;
    --sata_count)
    sata_count="$2"
    shift
    ;;
    --no_msata)
    msata_check=0
    ;;
    --no_sata)
    sata_check=0
    ;;
    --nic_count)
    nic_count="$2"
    shift
    ;;  
    --nic_name)
    nic_name="$2"
    shift
    ;;
    --m2_count)
    m2_count="$2"
    shift
    ;;
    --no_m2)
    m2_check=0
    ;;
    --modem_count)
    modem_count="$2"
    shift
    ;;
    --no_modem)
    modem_check=0
    ;;
    --sim_count)
    sim_count="$2"
    shift
    ;;
    *)
    # unknown option
    ;;
esac
shift # past argument or value
done

./hwconfig > /tmp/hw_info

cpu_ok=`grep Processors: /tmp/hw_info | grep -e "$cpu" -c`
if [ "$cpu_ok" == "0" ]; then
    echo CPU check fail
    cat /tmp/hw_info | grep Processors
    exit_code=1
else
    echo CPU check ok
fi

#memory_ok=`grep Memory: /tmp/hw_info | grep -e "$memory" -c`
#if [ "$memory_ok" == "0" ]; then
#    echo Memory check
    cat /tmp/hw_info | grep Memory
#   exit_code=1
#else
#    echo Memory check ok
#fi

disk_list=`fdisk -l | grep Disk | grep /dev/ | cut -d' ' -f2 | sed 's/://g'`
rm -f /tmp/disk_devpath_tmp
for disk in $disk_list; do
    udevadm info $disk 2> /dev/null | grep DEVPATH | cut -d/ -f5 >> /tmp/disk_devpath_tmp
done

disk_ok=1
if [ "$emmc_count" != "0" ]; then 
    count=`grep mmc /tmp/disk_devpath_tmp -c`
    if [ $count -lt $emmc_count ]; then
        echo eMMC check fail
        disk_ok=0
    else
        echo eMMC check ok
    fi
fi

detected_count=`grep usb /tmp/disk_devpath_tmp -c`
if [ $detected_count -lt $usb_count ]; then
    echo USB check fail
    disk_ok=0
else
    echo USB check ok
fi

if [ "$msata_check" == "1" ]; then
count=`grep ata1 /tmp/disk_devpath_tmp -c`
if [ $count -lt $msata_count ]; then
    echo mSATA check fail
    disk_ok=0
else
    echo mSATA check ok
fi
fi

if [ "$sata_check" == "1" ]; then
count=`grep ata2 /tmp/disk_devpath_tmp -c`
if [ $count -lt $sata_count ]; then
    echo SATA check fail
    disk_ok=0
else
    echo SATA check ok
fi
fi

if [ "$disk_ok" != "1" ]; then
    cat /tmp/hw_info | grep Disk:
    exit_code=1
fi

rm -f /tmp/disk_devpath_tmp

count=`grep Network: /tmp/hw_info | grep -e "$nic_name" -c`
if [ $count -lt $nic_count ]; then
    echo Network check fail
    grep Network: /tmp/hw_info | grep $nic_name -c
    exit_code=1
else
    echo Network check ok
fi

if [ "$m2_check" == "1" ]; then
count=`lspci | grep 03:00.0 -c`
if [ $count -lt $m2_count ]; then
    echo M.2 check fail
    exit_code=1
else
    echo M.2 check ok
fi
fi

if [ "$modem_check" == "1" ]; then
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
fi

if [ "$monitor_check" == "1" ]; then
count=`xrandr --query | grep HDMI | grep -e ' connected' -c`
if [ $count -lt $monitor_count ]; then
    echo Monitor check fail
    xrandr --query | grep HDMI | grep connected
    exit_code=1
else
    echo Monitor check ok
fi
fi

rm /tmp/hw_info

exit $exit_code
