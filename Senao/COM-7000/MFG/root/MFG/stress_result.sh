#!/bin/bash
# Author:Darcy Chang
# Date:2020/08/06
# Version:1.2.0

count=0
criteria=100
giga_criteria=0.1

stress_log_file=/root/MFG/logs/log.txt
result_file=/root/MFG/logs/result.txt

sleep $4
while [ $count != $5 ]
do
	count=$(grep -c "1" /tmp/throughput_done)
#	echo "[DEBUG] count = $count"
done

result1=$(cat /tmp/$3 | grep "bits/sec" | sed -n 1p | awk -F " " '{print $7}')
result2=$(cat /tmp/$3 | grep "bits/sec" | sed -n 2p | awk -F " " '{print $7}')
unit=$(cat /tmp/$3 | grep "bits/sec" | sed -n 1p | awk -F " " '{print $8}')

#echo "[DEBUG] $1 $result1 $unit"
#echo "[DEBUG] $2 $result2 $unit"

if [[ $unit == "Gbits/sec" ]] ;then
	if [[ `echo "$result1 > $giga_criteria"|bc` -eq 1 ]] ; then
		echo "[SENAO] Fiber $1 $result1 $unit PASS" | tee -a $result_file | tee -a $stress_log_file
	else
		echo "[SENAO] Fiber $1 $result1 $unit FAILED" | tee -a $result_file | tee -a $stress_log_file
	fi

	if [[ `echo "$result2 > $giga_criteria"|bc` -eq 1  ]] ; then
		echo "[SENAO] Fiber $2 $result2 $unit PASS" | tee -a $result_file | tee -a $stress_log_file
	else
		echo "[SENAO] Fiber $2 $result2 $unit FAILED" | tee -a $result_file | tee -a $stress_log_file
	fi
        
elif [[ $unit == "Mbits/sec" ]] ;then
	if [[ $result1 -ge $criteria ]] ; then
		echo "[SENAO] Fiber $1 $result1 $unit PASS" | tee -a $result_file | tee -a $stress_log_file
	else
		echo "[SENAO] Fiber $1 $result1 $unit FAILED" | tee -a $result_file | tee -a $stress_log_file
	fi

	if [[ $result2 -ge $criteria ]] ; then
		echo "[SENAO] Fiber $2 $result2 $unit PASS" | tee -a $result_file | tee -a $stress_log_file
	else
		echo "[SENAO] Fiber $2 $result2 $unit FAILED" | tee -a $result_file | tee -a $stress_log_file
	fi

else
	echo "[DEBUG] Fiber unknown error unit $unit" | tee -a $result_file |tee -a $stress_log_file
fi

