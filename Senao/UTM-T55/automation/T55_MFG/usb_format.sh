#!/bin/bash

sys_disk=$(mount | grep 'on / ' | cut -d' ' -f1 | sed 's/.$//')
sdisk=$(basename $sys_disk)
all_disk="sd[abcdefg]"
extra_disk=$(lsblk|grep sd[abcdefg]|grep disk|grep -v $sdisk |awk '{print $1}')
partition="1 2 3 4 5"
ERR=0
for disk in $extra_disk
do
    for part in $partition
    do
        umount /dev/$disk$part > /dev/null 2>&1
    done

    parted -s /dev/$disk mklabel msdos
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk MS-DOS partition fail"
		echo "BURN_IN_TEST: $disk MS-DOS partition fail" >> /root/automation/testresults-failure.txt
        continue
    fi
    parted -s /dev/$disk mkpart primary ext4 0% 100%
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk partition full volume fail"
		echo "BURN_IN_TEST: $disk partition full volume fail" >> /root/automation/testresults-failure.txt
        continue
    fi
    sleep 1;
    mkfs.ext4 -F /dev/"$disk"1
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk EXT4 format fail"
		echo "BURN_IN_TEST: $disk EXT4 format fail" >> /root/automation/testresults-failure.txt
        continue
    fi
done

if [ "$ERR" == "1" ]; then
    echo Format process is not completed.
else
    echo Format process is completed.
fi
