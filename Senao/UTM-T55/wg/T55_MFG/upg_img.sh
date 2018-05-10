#!/bin/bash

if (($# < 2)); then
    echo "please specify image file and sha1sum file"
    echo "usage: $0 {image_file } {sha1sum_file}"
    exit 1
fi

if [ ! -f $1 ]; then
    echo "image file not exist"
    exit 1
fi

if [ ! -f $2 ]; then
    echo "sha1sum file not exist"
    exit 1
fi

sha1sum=`sha1sum $1 | cut -d " " -f 1`
cmp_res=`cat $2 | grep $sha1sum -c`
if [ "$cmp_res" == "0" ]; then
    echo "sha1sum comparison failed"
    exit 1
fi

cp $1 /tmp/img.cf.gz
cp img_copy /tmp/img_copy
echo "copy_exec /tmp/img.cf.gz /" >> /tmp/img_copy
cp /tmp/img_copy /usr/share/initramfs-tools/hooks/
chmod 775 /usr/share/initramfs-tools/hooks/img_copy
cp do_upg /usr/share/initramfs-tools/scripts/init-bottom/
chmod 775 /usr/share/initramfs-tools/scripts/init-bottom/do_upg
update-initramfs -u -v
reboot
