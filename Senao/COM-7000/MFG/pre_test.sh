#!/bin/bash
#Objective: Before stress item, we do pre-test for HW detection.
#Author:Darcy Chang
#Date:2018/12/11

disk_count=4
port_count=5
hdd_size_criteria=100
hdd_speed_criteria=50
fail=0

function i2c_detect {
        bus_num=$(/root/i2c_bus.sh)
        if [ "$bus_num" == 2 ] ; then
                echo "0"
        elif [ "$bus_num" == 14 ] ; then
                echo "12"
        else
		i2cdetect -l
        fi
}


function is_link {
        port_num=$(ifconfig -a | grep eth | wc -l)
	if [ $port_num -ne $port_count ] ; then
		echo "[ERROR] Port number is $port_num"
		ifconfig -a
		echo "Pre-test status: FAIL"
		exit
	fi
        for ((eid=0; eid<$port_num; eid++))
	do
        	link_state=$(ethtool eth$eid | grep 'Link detected' | awk '{print $3}')
		echo "[DEBUG] eth$eid $link_state"
		if [ $link_state != "yes" ] ; then
			echo "[ERROR] Port eth$eid link status $link_state" 
			lspci
			lspci -v
			ifconfig -a
			echo "Pre-test status: FAIL"
			exit
		fi
	done
}


function detect_disk {
	sys_disk=$(mount | grep 'on / ' | cut -d' ' -f1 | cut -d/ -f3 | sed 's/.$//')

	if [ -z "$disk_list" ]; then
		disk_list=$(lsblk | grep "mmc" -v | grep "disk" | awk '{print $1}')
		if [ -z "$no_mmc" ] && [ -n "$(lsblk | grep "disk" | grep '$mmc_disk')" ]; then
			disk_list="${disk_list} ${mmc_disk}"
		fi
	else
		disk_list=$(echo $disk_list | sed -n 's/,/ /gp')
	fi

	extra_disk_count=0
	for disk in $disk_list; do
		echo "[DEBUG] Detect $disk"
		hdd_test $disk
		if [ "$disk" != "$sys_disk" ]; then
			extra_disk_list="${extra_disk_list}${disk} "
			extra_disk_count=$(expr $extra_disk_count + 1)
		fi
	done

	if [ "$extra_disk_count" -lt "$disk_count" ]; then
		echo "Disk number is $extra_disk_count, Disk resource not enough $disk__
count"
		lsusb
		lsblk
		lsusb -v
		echo "Pre-test status: FAIL"
		exit
	fi
}


function hdd_test(){
	hdd=$(smartctl -i /dev/$1 | grep -c "User Capacity")
	if [ $hdd == "0" ] ; then
		return
	fi
	size=$(smartctl -i /dev/$1 | grep "User Capacity" | awk '{print $5}' | cut -d "[" -f 2)
	if [ $(echo "$size > $hdd_size_criteria" | bc) -eq 1 ] ; then
		hdparm -t --direct /dev/$1 | tee /tmp/hdd.txt
		hdd_speed=$(cat /tmp/hdd.txt | grep "MB/sec" | awk '{print $11}')
		if [ $(echo "$hdd_speed > $hdd_speed_criteria" | bc) -ne 1 ] ; then
			echo "[ERROR] SSD/HDD transfer rate $hdd_speed is too low. "
			fail=1
		fi
	fi
}

rm /tmp/hdd.txt

echo ""
echo "FW Version: "$(cat /etc/version)
echo ""

i2c_num=$(i2c_detect)
i2cdetect -y $i2c_num
i2cset -y $i2c_num 0x25 0x02 0x00
i2cset -y $i2c_num 0x25 0x06 0x00

is_link
echo ""
detect_disk

if [ -f /tmp/hdd.txt ] ; then
	fail=$(cat /tmp/hdd.txt | grep -c "failed")
else
	echo "[ERROR] SSD/HDD has not detected."
	fail=1
fi
echo ""
if [[ $fail == "1" ]] ; then
	echo "Pre-test status: FAIL"
else
	echo "Pre-test status: PASS"
fi
echo ""
