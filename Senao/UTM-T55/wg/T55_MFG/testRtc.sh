#!/bin/bash

TESTTIME="080808082030"
CHECKTIME="2030-08-08 08:08:00"

case $1 in
"set")
#	timedatectl set-ntp 0
	echo "rtc set date ${TESTTIME}"
	str=`date ${TESTTIME}; hwclock -w`
	datestr1=$(date +%s)
	;;
"get")
	echo "rtc get"
	datestr=`date +%s`
	echo $datestr
	;;
"check")
    datestr2=`hwclock -s;date +%s`
 	datestr1=`date --date="${CHECKTIME}" +%s`
	if [[ $datestr2 -gt $datestr1 ]] ; then
		echo "pass"
	else
		echo "fail"
	fi
#	timedatectl set-ntp 1	
	;;
*)
	echo "Usge:$0 <command>"
	echo "Available command"
	echo "set"
	echo "get"
	echo "check"
	exit
esac
