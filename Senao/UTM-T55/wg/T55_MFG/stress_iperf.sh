#!/bin/bash 

/root/automation/T55_MFG/set_ip.sh -g

port_num=$(ifconfig -a | grep eth | wc -l)
for ((eid=0; eid<$port_num; eid++))
do
	iperf -c 192.168.$eid.1 -t 999999 -P 1 &
done

sleep 1
#echo "[SENAO] GS ps -ax" | tee -a $log_path
#ps -ax | grep iperf

