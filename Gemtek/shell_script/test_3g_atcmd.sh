#!/bin/sh
count=0

redis-server /usr/local/redis/etc/redis.conf

while [ 1 ];
do
echo "**********************************************************************************************"
count=`expr $count + 1`
echo "Round" $count
echo ""
date
echo ""
uptime
#echo ""
#ifconfig
echo "***********************************************************************************************"
#3g.sh start
#cdc_ncm_connect start

echo "at-cmd /dev/ttyUSB2 AT"
at-cmd /dev/ttyUSB2 AT

echo "at-cmd /dev/ttyUSB2 AT+CGATT=1"
at-cmd /dev/ttyUSB2 AT+CGATT=1

echo "at-cmd /dev/ttyUSB2 AT"
at-cmd /dev/ttyUSB2 AT

echo "at-cmd /dev/ttyUSB2 at^dhcp?"
at-cmd /dev/ttyUSB2 at^dhcp?

echo "at-cmd /dev/ttyUSB2 at^ndisdup=1,1,"internet","","""
at-cmd /dev/ttyUSB2 at^ndisdup=1,1,"internet","",""

echo "***********************************************************************************************"
#3g.sh stop
#cdc_ncm_connect stop

echo "at-cmd /dev/ttyUSB2 AT+CGACT=0"
at-cmd /dev/ttyUSB2 AT+CGACT=0
done

