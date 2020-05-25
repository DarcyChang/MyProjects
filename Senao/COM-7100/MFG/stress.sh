#!/bin/bash
#Objective:Automatic stress
#Author:Darcy Chang
#Date:2020/05/21
#Version:1.0

loopback_list="eth0:eth1,eth2:eth3,eth5:eth6,eth7:eth8,eth9:eth10,eth11:eth12,eth13:eth14,eth15:eth16,eth17:eth18,eth19:eth20,eth21:eth22"
declare -i x=0

if [ "$1" == "-t" ] ;then
	if [ -n "$2" ] ;then
	        seconds=$2
	else
		echo "[DEBUG] The testing timer can not be empty."	       
		exit
	fi
else
	echo "[DEBUG] wrong paramter"
	echo "./stress.sh"
	echo "             -t  times, unit is second."
	exit
fi

rm /tmp/throughput_* 2>&1
echo "0" > /tmp/throughput_done
killall iperf >/dev/null  2>&1

if [ ! -z "$(echo $loopback_list | grep ,)" ]; then
	loopback_list=$(echo $loopback_list | sed -n 's/,/ /gp')
fi

for pair in $loopback_list;
do
	iface1=$(echo $pair | cut -d: -f1)
	iface2=$(echo $pair | cut -d: -f2)
#	echo "[DEBUG] $iface1 and $iface2"
	/root/MFG/iperf_ns.sh $iface1 $iface2 $seconds &
	x+=1
done

for pair in $loopback_list;
do
	iface1=$(echo $pair | cut -d: -f1)
	iface2=$(echo $pair | cut -d: -f2)
	file_name=throughput_"$iface1"_"$iface2"
#	echo "[DEBUG] $file_name"
#	echo "[DEBUG] x = $x"
	/root/MFG/stress_result.sh $iface1 $iface2 $file_name $seconds $x &
done
