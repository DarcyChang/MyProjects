#!/bin/bash

#source /root/automation/Library/path.sh
test_result_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/T55_MFG/mfg_version | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/T55_MFG/mfg_version | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_path" | awk '{print $2}')
time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_golden_path" | awk '{print $2}')   

extra_disk=$(lsblk|grep sd[bcdefg]|grep disk|awk '{print $1}')
partition="1 2 3 4 5"
ERR=0
usb_num=0

if [[ -z "$extra_disk" ]] ; then
	ERR=1
	echo "BURN_IN_TEST: No USB dongle" >> $test_result_failure_path
else 
	for disk in $extra_disk
	do
		usb_num=`expr $usb_num + 1`	
	done
	
	if [ $usb_num -lt 2 ] ; then
		ERR=1
		echo "BURN_IN_TEST: USB dongle not enough, just only $usb_num" >> $test_result_failure_path
	fi
fi

for disk in $extra_disk
do
	echo "[DEBUG] disk = $disk"
    for part in $partition
    do
        umount /dev/$disk$part > /dev/null 2>&1
    done

    parted -s /dev/$disk mklabel msdos
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk MS-DOS partition fail"
		echo "BURN_IN_TEST: $disk MS-DOS partition fail" >> $test_result_failure_path
        continue
    fi

    parted -s /dev/$disk mkpart primary ext3 0% 100%
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk partition full volume fail"
		echo "BURN_IN_TEST: $disk partition full volume fail" >> $test_result_failure_path
        continue
    fi
    sleep 1;

    for part in $partition
    do
        umount /dev/$disk$part > /dev/null 2>&1
    done

    mke2fs -T ext3 /dev/"$disk"1
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk EXT3 format fail"
		echo "BURN_IN_TEST: $disk EXT3 format fail" >> $test_result_failure_path
        continue
    fi
done

if [ "$ERR" == "1" ]; then
    echo "Format process is not completed."
else
    echo "Format process is completed."
fi
