#!/bin/sh
count=0

redis-server /usr/local/redis/etc/redis.conf
./ulog -i -d /dev/ttyUSB0

while [ 1 ];
do
echo "**********************************************************************************************"
count=`expr $count + 1`
echo $count
date
#ifconfig

echo "***********************************************************************************************"
#3g.sh start
echo "at-cmd /dev/ttyUSB0 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,"
at-cmd /dev/ttyUSB0 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,
echo "at-cmd /dev/ttyUSB1 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,"
at-cmd /dev/ttyUSB1 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,
echo "at-cmd /dev/ttyUSB2 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,"
at-cmd /dev/ttyUSB2 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,
echo "at-cmd /dev/ttyUSB3 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,"
at-cmd /dev/ttyUSB3 AT^SYSCFGEX=\"00\",3fffffff,1,2,7fffffffffffffff,,

echo "at-cmd /dev/ttyUSB0 AT^SYSINFOEX"
at-cmd /dev/ttyUSB0 AT^SYSINFOEX
echo "at-cmd /dev/ttyUSB1 AT^SYSINFOEX"
at-cmd /dev/ttyUSB1 AT^SYSINFOEX
echo "at-cmd /dev/ttyUSB2 AT^SYSINFOEX"
at-cmd /dev/ttyUSB2 AT^SYSINFOEX
echo "at-cmd /dev/ttyUSB3 AT^SYSINFOEX"
at-cmd /dev/ttyUSB3 AT^SYSINFOEX

echo "at-cmd /dev/ttyUSB0 AT+CGATT=1"
at-cmd /dev/ttyUSB0 AT+CGATT=1
echo "at-cmd /dev/ttyUSB1 AT+CGATT=1"
at-cmd /dev/ttyUSB1 AT+CGATT=1
echo "at-cmd /dev/ttyUSB2 AT+CGATT=1"
at-cmd /dev/ttyUSB2 AT+CGATT=1
echo "at-cmd /dev/ttyUSB3 AT+CGATT=1"
at-cmd /dev/ttyUSB3 AT+CGATT=1

echo "at-cmd /dev/ttyUSB0 at^dhcp?"
at-cmd /dev/ttyUSB0 at^dhcp?
echo "at-cmd /dev/ttyUSB1 at^dhcp?"
at-cmd /dev/ttyUSB1 at^dhcp?
echo "at-cmd /dev/ttyUSB2 at^dhcp?"
at-cmd /dev/ttyUSB2 at^dhcp?
echo "at-cmd /dev/ttyUSB3 at^dhcp?"
at-cmd /dev/ttyUSB3 at^dhcp?

echo "at-cmd /dev/ttyUSB0 at^ndisdup=1,1,internet,,"
at-cmd /dev/ttyUSB0 at^ndisdup=1,1,"internet","",""
echo "at-cmd /dev/ttyUSB1 at^ndisdup=1,1,internet,,"
at-cmd /dev/ttyUSB1 at^ndisdup=1,1,"internet","",""
echo "at-cmd /dev/ttyUSB2 at^ndisdup=1,1,internet,,"
at-cmd /dev/ttyUSB2 at^ndisdup=1,1,"internet","",""
echo "at-cmd /dev/ttyUSB3 at^ndisdup=1,1,internet,,"
at-cmd /dev/ttyUSB3 at^ndisdup=1,1,"internet","",""


echo "***********************************************************************************************"
#3g.sh stop
echo "at-cmd /dev/ttyUSB0 AT^NDISDUP=1,0"
at-cmd /dev/ttyUSB0 AT^NDISDUP=1,0
echo "at-cmd /dev/ttyUSB1 AT^NDISDUP=1,0"
at-cmd /dev/ttyUSB1 AT^NDISDUP=1,0
echo "at-cmd /dev/ttyUSB2 AT^NDISDUP=1,0"
at-cmd /dev/ttyUSB2 AT^NDISDUP=1,0
echo "at-cmd /dev/ttyUSB3 AT^NDISDUP=1,0"
at-cmd /dev/ttyUSB3 AT^NDISDUP=1,0

echo "at-cmd /dev/ttyUSB0 AT+CGATT=0"
at-cmd /dev/ttyUSB0 AT+CGATT=0
echo "at-cmd /dev/ttyUSB1 AT+CGATT=0"
at-cmd /dev/ttyUSB1 AT+CGATT=0
echo "at-cmd /dev/ttyUSB2 AT+CGATT=0"
at-cmd /dev/ttyUSB2 AT+CGATT=0
echo "at-cmd /dev/ttyUSB3 AT+CGATT=0"
at-cmd /dev/ttyUSB3 AT+CGATT=0

done

