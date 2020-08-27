#!/bin/bash
# Author:Darcy Chang
# Date:2020/08/10
# Version:1.2.0

criteria=3

stress_log_file=/root/MFG/logs/log.txt
result_file=/root/MFG/logs/result.txt
ping_result_file=/root/MFG/logs/ping_result.txt


echo "" | tee -a $stress_log_file
echo "[SENAO] Starting I210 ping." | tee -a $stress_log_file

dhclient eth0

domain_ip=$(ifconfig eth0 | grep 'inet ' | awk 'BEGIN{FS=" "} {print $2} ' | awk 'BEGIN{FS=":"} {print $2}' | cut -d'.' -f1,2,3)
server_ip=1
server_ip="$domain_ip.$server_ip"
echo "[DEBUG] domain name IP address $domain_ip" | tee -a $stress_log_file
echo "[DEBUG] server IP address $server_ip" | tee -a $stress_log_file
ping $server_ip -c 30 | tee $ping_result_file | tee -a $stress_log_file

eth0_received=$(cat $ping_result_file | grep  "received" | awk -F " " '{print $4}')

echo "[SENAO] I210 Packet received $eth0_received" | tee -a $stress_log_file

if [[ $eth0_received -ge $criteria ]] ; then
	echo "[SENAO] I210 ping PASS" | tee -a $result_file | tee -a $stress_log_file
else
	echo "[SENAO] I210 ping FAIL" | tee -a $result_file | tee -a $stress_log_file
fi
