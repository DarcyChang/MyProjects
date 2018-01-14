#! /bin/sh

if [ "$1" == "" ]; then
	echo "parameter is none" 
	exit 1
else
	echo "***** $1 *****"
fi

mounted=`mount | grep $1 | wc -l`
#echo "$ACTION" >> /tmp/mount_log
#echo "first mounted = $mounted" >> /tmp/mount_log

# mounted, assume we umount
if [ "$ACTION" == "remove" ]; then
	echo "R/media/$1" 
	echo "R/media/$1" 
	if [ $mounted -eq 0 ] ; then
		op_notify 400 1 "/media/$1"	
	else
		if ! umount "/media/$1"; then
			exit 1
		else
			op_notify 400 1 "/media/$1"	
		fi
	fi 

	if ! rm -r "/media/$1"; then
		exit 1
	fi
# not mounted, lets mount under /media
else
	if ! mkdir -p "/media/$1"; then
		exit 1
fi

mounted=`mount | grep $1 | wc -l`
num=3

if [ "$ACTION" == "add" ]; then
	echo "Enter while loop"
	mount "/dev/$1" "/media/$1"	
	op_notify 400 0 "/media/$1"	
	if [ -f /etc_ro/sdcard_mount.log ]; then
		echo "/media/$1" >> /etc_ro/sdcard_mount.log 
	fi
	echo "/media/$1" > /tmp/sdcard_path
fi
mounted=`mount | grep $1 | wc -l`

while [ $mounted -lt 1 -a $num -lt 3 ]
do
	ntfs-3g "/dev/$1" "/media/$1" -o force
	mounted=`mount | grep $1 | wc -l`
	num=`expr $num + 1`
done

if [ $mounted -lt 1 ]; then
	rm -r "/media/$1"
	exit 1
fi
echo "A/media/$1" 
echo "A/media/$1" 
fi

# Goahead need to know the event happened.
killall -SIGTTIN goahead
exit 0

