#! /bin/bash 

for entry in /media/*
do
#	echo "$entry"
		if [[ "$entry" != @(/media/ext-cap-hdd|/media/preloaded|/media/uploaded|/media/usbhd-SD) ]]; then 
			echo "rm $entry"
			rm -rf $entry
		fi
done

