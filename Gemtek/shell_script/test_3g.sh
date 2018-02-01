#!/bin/sh
count=0

redis-server /usr/local/redis/etc/redis.conf

while [ 1 ];
do
echo "**********************************************************************************************"
count=`expr $count + 1`
echo $count
date
ifconfig
echo "***********************************************************************************************"
#3g.sh start
cdc_ncm_connect start
echo "***********************************************************************************************"
#3g.sh stop
cdc_ncm_connect stop
done

