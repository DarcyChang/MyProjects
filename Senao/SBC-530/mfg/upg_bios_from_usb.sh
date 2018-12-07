#!/bin/bash

if (($# == 0)); then
    FILE_NAME=default
elif (($# == 1)); then
    FILE_NAME=$1
else
     echo "please specify image file"
     echo "usage: $0 {image_file} or"
     echo "       $0 (default option)"
     exit 1
fi

sys_disk=$(mount | grep 'on / ' | cut -d' ' -f1 | cut -d/ -f3 | sed 's/.$//')
disk_list=$(fdisk -l | grep Disk | grep -v mmc| grep -v $sys_disk | grep /dev/ | cut -d' ' -f2 | sed 's/://g')

if [ -z "$disk_list" ]; then
    echo "No USB Insert"
    exit 1
fi

disk_list=$(basename -a $disk_list)

for disk in $disk_list; do
   mkdir -p /tmp/$disk
   mount /dev/${disk}1 /tmp/$disk > /dev/null 2>&1
done

if [ "$FILE_NAME" == "default" ]; then
    for disk in $disk_list; do
        BIOS_FOLDER="/tmp/$disk/bios/"
        if [ -d "$BIOS_FOLDER" ]; then
	    break
	fi
    done
    if [ ! -d "$BIOS_FOLDER" ]; then
        echo "Can't find BIOS folder"
        exit 1
    else
        BIOS_FILE="${BIOS_FOLDER}*.bin"
    fi
else
    BIOS_FILE=$(find /tmp/* -name $FILE_NAME)
    BIOS_FILE=$(echo $BIOS_FILE | cut -d' ' -f1)
    if [ -z "$BIOS_FILE" ]; then
        echo "Can't find BIOS file"
        exit 1
    fi
fi
echo $BIOS_FILE
MD5_cal=$(md5sum $BIOS_FILE | cut -d' ' -f1)
MD5_PATH=$(dirname ${BIOS_FILE})/md5sum
MD5_file=$(cat $MD5_PATH | tr '[:upper:]' '[:lower:]')
if [ "$MD5_cal" == "$MD5_file" ]; then
    echo "MD5 check ok"
else
    echo "MD5 check filed"
    exit 1
fi
./upg_bios.sh $BIOS_FILE

for disk in $disk_list; do
   umount /dev/${disk}1 > /dev/null 2>&1
#   rm /tmp/$disk -rf
done

echo "Flash BIOS done"
