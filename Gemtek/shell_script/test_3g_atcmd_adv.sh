#!/bin/sh
count=0

#redis-server /usr/local/redis/etc/redis.conf

cat /dev/ttyUSB2 &

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

echo "at-cmd /dev/ttyUSB0 AT"
echo at > /dev/ttyUSB2

echo "at-cmd /dev/ttyUSB0 AT+CGATT=1"
echo AT+CGATT=1 > /dev/ttyUSB2

echo "at-cmd /dev/ttyUSB0 at^dhcp?"
echo at^dhcp? > /dev/ttyUSB2

echo "at-cmd /dev/ttyUSB0 at^ndisdup=1,1,"internet","","""
echo at^ndisdup=1,1,"internet" > /dev/ttyUSB2

echo "***********************************************************************************************"
#3g.sh stop
#cdc_ncm_connect stop

echo "at-cmd /dev/ttyUSB0 AT+CGACT=0"
echo AT+CGATT=0 > /dev/ttyUSB2

done

