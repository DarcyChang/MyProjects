#!/bin/sh
COUNT=1050

echo "##############Wait 30 sec to test $num times#############"
sleep 30

ifconfig
objReq sys show

num=`cat /rebootnum`
if [ x"$num" = "x" ]; then
        num=0
fi
if [ $num != $COUNT ]; then
        echo "##############Wait 90 sec for device boot up ready############" 
        sleep 90

	# run set phy mac
	echo run set phy mac
	echo "NODEID = f8 35 dd 88 77 66" > /tmp/8168G.cfg.mac
	cat /tmp/8168G.cfg.mac /etc/8168G.cfg > /tmp/8168GEF.cfg
	cp -f /usr/bin/rtnicpg-i686 /tmp/rtnicpg-i686
	/tmp/rtnicpg-i686 /efuse
	/usr/bin/rtnicpg-i686 /efuse /r > /var/RTL_phy_config

	rm -f /etc/udev/rules.d/70-persistent-net.rules

	# run set base mac
	echo run set base mac
	objReq sys setparam wanMacAddr f8:35:dd:55:44:22

	num=$(expr $num + 1)
	echo $num > /rebootnum
	
	echo "##################### Write MAC time=$num"  

	echo "#####################Prepare to reboot sleep 5" 
	sync
	dmesg -n 7
	sleep 5
	reboot
fi
