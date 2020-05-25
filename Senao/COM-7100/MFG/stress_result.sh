#!/bin/bash
#Author:Darcy Chang
#Date:2020/05/21
#Version:1.0

count=0

sleep $4
while [ $count != $5 ]
do
	count=$(grep -c "1" /tmp/throughput_done)
#	echo "[DEBUG] count = $count"
done

result1=$(cat /tmp/$3 | grep "bits/sec" | grep "5]" | awk -F " " '{print $7}')
result2=$(cat /tmp/$3 | grep "bits/sec" | grep "4]" | awk -F " " '{print $7}')
unit=$(cat /tmp/$3 | grep "bits/sec" | grep "4]" | awk -F " " '{print $8}')

#echo "[DEBUG] $1 $result1 $unit"
#echo "[DEBUG] $2 $result2 $unit"

if [ $unit == "Gbits/sec" ] ;then
	if [[ `echo "$result1 > 0.1"|bc` -eq 1 ]] ; then
		echo "[PASS] $1 $result1 $unit"
	else
		echo "[FAILED] $1 $result1 $unit"
	fi

	if [[ `echo "$result2 > 0.1"|bc` -eq 1  ]] ; then
		echo "[PASS] $2 $result2 $unit"
	else
		echo "[FAILED] $2 $result2 $unit"
	fi
        
elif [ $unit == "Mbits/sec" ] ;then
	if [[ $result1 -ge 100 ]] ; then
		echo "[PASS] $1 $result1 $unit"
	else
		echo "[FAILED] $1 $result1 $unit"
	fi

	if [[ $result2 -ge 100 ]] ; then
		echo "[PASS] $2 $result2 $unit"
	else
		echo "[FAILED] $2 $result2 $unit"
	fi

else
	echo "[DEBUG] unknown error unit $unit"
fi

