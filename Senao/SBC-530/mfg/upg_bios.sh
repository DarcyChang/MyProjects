#!/bin/bash

if (($# < 1)); then
	echo "please specify image file"
	echo "usage: $0 {image_file}"
	exit 1
fi

if [ ! -f $1 ]; then
	echo "image file not exist"
	exit 1
fi

full_img_path=`readlink -f $1`
cmd="cd /root/SBC-1100/bios/InsydeH2OFFT_x86_LINUX64_100.00.08.18/; ./H2OFFTx64.sh $full_img_path -ALL -BIOS -RA -Q -N"
sshpass -p senao ssh root@localhost $cmd
