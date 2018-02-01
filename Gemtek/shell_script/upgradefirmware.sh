#!/bin/sh
FWNAME="package_1.2.21-KENYA_rooted.tgz"
COUNT=1050
MODE="USB"
FWPATH="/tmp/$FWNAME"

echo "##############Wait 30 sec to test $num times#############"
sleep 30

num=`cat /rebootnum`
if [ x"$num" = "x" ]; then
        num=0
fi
if [ $num != $COUNT ]; then
        echo "##############Wait 60 sec for device boot up ready############" 
        sleep 60
	echo "##############Copy firmware to system############"
	echo "####################Copy firmware /home//$FWNAME to $FWPATH"
	cp /home/$FWNAME $FWPATH

	if [ -f "$FWPATH" ]; then
		echo "#############Get firmware start to upgrade firmware############"
		fw_upgrade.sh $FWPATH
	else
		echo "####################No firmware $FWPATH, just reboot"
	fi

        num=$(expr $num + 1)
        echo $num > /rebootnum
	echo "#####################Upgrade firmware time=$num"  

	echo "#####################Prepare to reboot sleep 5" 
	dmesg -n 7
	sync
	sleep 5
	cp /home/rc.local /etc/rc.local
	reboot
fi
