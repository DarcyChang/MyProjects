#!/bin/bash

function writehdd()
{
    while [ 1 ]; do
	dd if=/dev/zero of=/tmp/${SATA}/tmp_file bs=4M count=1 2> /dev/null
        sleep 0.3
    done
}

disk_list=`fdisk -l 2> /dev/null| grep Disk | grep /dev/ | cut -d' ' -f2 | sed 's/://g'`
for disk in $disk_list; do
    udevadm info $disk 2> /dev/null | grep DEVPATH  >> /tmp/disk_devpath_tmp
done
SATA=$(grep ata2 /tmp/disk_devpath_tmp | cut -d/ -f10)
rm /tmp/disk_devpath_tmp

if [ -z "$SATA" ]; then 
    echo "No detect SATA HDD"
    exit 0
fi 

umount /dev/${SATA}1 > /dev/null 2>&1

mkdir /tmp/$SATA -p
mount /dev/${SATA}1 /tmp/$SATA > /dev/null 2>&1
if [ "$?" != "0" ]; then
    parted -s /dev/${SATA} mklabel msdos > /dev/null
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk MS-DOS partition fail"
        exit
    fi
    parted -s /dev/${SATA} mkpart primary ext4 4096b 1.5G > /dev/null 2>&1
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk partition full volume fail"
        exit
    fi
    sleep 1
    mkfs.ext4 -F /dev/${SATA}1 > /dev/null 2>&1
    if [ "$?" != "0" ]; then
        ERR=1
        echo "Error: $disk EXT4 format fail"
        exit
    fi
    mount /dev/${SATA}1 /tmp/${SATA} > /dev/null 2>&1
fi

writehdd &

read -p "press enter to stop" ps
umount /dev/${SATA}1
disown $!
kill $!
