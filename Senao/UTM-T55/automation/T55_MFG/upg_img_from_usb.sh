#!/bin/bash

usb_dev=`fdisk -l | grep /dev/sdb1 | cut -d " " -f 1`
if [ "$usb_dev" == "" ]; then
    echo "no USB inserted"
    exit 1
fi

mkdir -p /mnt${usb_dev}
umount ${usb_dev} 2> /dev/null
mount /dev/sdb1 /mnt${usb_dev}

img_file=`ls /mnt${usb_dev}/wg_img -l | grep ".cf.gz" | awk '{print $9}'`
if [ "$img_file" == "" ]; then
    echo "no image file found in USB"
    exit 1
fi
img_file="/mnt${usb_dev}/wg_img/$img_file"
sha1_file=`ls /mnt${usb_dev}/wg_img -l | grep "sha1sums.txt" | awk '{print $9}'`
if [ "$sha1_file" == "" ]; then
    echo "no SHA1 file found in USB"
    exit 1
fi
sha1_file="/mnt${usb_dev}/wg_img/$sha1_file"
echo $img_file
echo $sha1_file

./upg_img.sh $img_file $sha1_file
