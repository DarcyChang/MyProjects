#!/bin/bash
#Objective:Automatic stress
#Author:Darcy Chang
#Date:2020/08/05
#Version:1.1.0

loopback_list="eth1:eth2,eth3:eth4"
declare -i x=0

stress_log_file=/root/MFG/logs/log.txt
result_file=/root/MFG/logs/result.txt
tmp_stress_file=/tmp/tmp_stress.txt

if [ "$1" == "-t" ] ;then
	if [ -n "$2" ] ;then
	        seconds=$2
	else
		echo "[DEBUG] The testing timer can not be empty" | tee -a $stress_log_file
		exit
	fi
else
	echo "[DEBUG] wrong paramter" | tee -a $stress_log_file
	echo "./stress.sh" | tee -a $stress_log_file
	echo "             -t  times, unit is second." | tee -a $stress_log_file
	exit
fi

echo "" | tee -a $stress_log_file
echo "[SENAO] Starting Burn-In." | tee -a $stress_log_file

rm /tmp/throughput_* 2>&1
echo "0" > /tmp/throughput_done
killall iperf >/dev/null  2>&1

if [ ! -z "$(echo $loopback_list | grep ,)" ]; then
	loopback_list=$(echo $loopback_list | sed -n 's/,/ /gp')
fi

/root/MFG/BI_led.sh &
mem_size=$(echo "$(free -m | grep Mem | awk -F " " '{print $4}')/1.1"|bc)
#echo "[DEBUG] Memory size = $mem_size"
stressapptest -s $seconds -M $mem_size -v 20 | tee $tmp_stress_file |tee -a $stress_log_file &

for pair in $loopback_list;
do
	iface1=$(echo $pair | cut -d: -f1)
	iface2=$(echo $pair | cut -d: -f2)
#	echo "[DEBUG] $iface1 and $iface2"
	/root/MFG/iperf_ns.sh $iface1 $iface2 $seconds | tee -a $stress_log_file &
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
