#!/bin/bash
# Author Darcy.Chang
# Date 2020.09.16 (Darcy's Birthday)
# Version 1.3.0

result_file=/root/MFG/logs/result.txt
stress_log_file=/root/MFG/logs/log.txt

status=0
fiber=0

while [[ $status -ne 1 ]]
do
	status=$(grep -c "Status:" /tmp/tmp_stress.txt)
	sleep 10
done

while [[ $fiber -ne 4 ]]
do
	fiber=$(grep -c "Fiber" $result_file)
	sleep 10
done

echo "[SENAO] Stopping B/I LED." | tee -a $stress_log_file
killall BI_led.sh
/root/MFG/ctl_led.sh bi off

cpu_mem_stress=$(grep -c "PASS" /tmp/tmp_stress.txt)
echo "[DEBUG] status=$status, fiber=$fiber, cpu_mem_stress=$cpu_mem_stress " | tee -a $stress_log_file
if [[ $cpu_mem_stress -eq 1 ]] ;then
        echo "[SENAO] CPU and DDR stress PASS." >> $result_file
fi

pass_num=$(grep -c "PASS" $result_file)
echo "[DEBUG] pass number $pass_num" | tee -a $stress_log_file

timedatectl set-timezone Asia/Taipei
timestamp=$(date +%Y%m%d_%H%M%S)
cpu_sn=$(i2cdump -y 1 0x56 b | grep "10:" | awk -F " " '{print $18}' | awk -F "." '{print $1}')
if [ ! -n "$cpu_sn" ] ; then
	cpu_sn=sn
fi
filename="$cpu_sn"_"$timestamp".tar.gz
echo "[DEBUG] filename = $filename"

echo "[DEBUG] CPU serial number $cpu_sn" | tee -a $stress_log_file
cp /tmp/throughput_done /root/MFG/logs/
cp /tmp/throughput_eth1_eth2 /root/MFG/logs/
cp /tmp/throughput_eth3_eth4 /root/MFG/logs/
cp /tmp/tmp_stress.txt /root/MFG/logs/
tar -czvPf "$filename" /root/MFG/logs
server_ip=$(cat $stress_log_file | grep "server IP address" | awk -F " " '{print $5}')

ls -al "$filename"
tftp -v "$server_ip" -c put "$filename" &> /tmp/tftp.txt
cp /tmp/tftp.txt /root/MFG/logs/
transmit_timeout=$(grep -c "Transfer timed out" /tmp/tftp.txt)
transmit_no_file=$(grep -c "No such file or directory" /tmp/tftp.txt)
transmit_violation=$(grep -c "Access violation" /tmp/tftp.txt)

if [[ $transmit_timeout -eq 1 ]] || [[ $transmit_no_file -eq 1 ]] || [[ $transmit_violation -eq 1 ]]; then
	/root/MFG/ctl_led.sh bi on
	echo "[DEBUG] tftp transmit failed."
	cat /tmp/tftp.txt | tee -a /root/MFG/logs/result.txt
	tar -czvPf "$filename" /root/MFG/logs
	mv "$filename" /root/MFG/backup/
	exit
fi
mv "$filename" /root/MFG/backup/

if [[ $pass_num -eq 6 ]] ;then
	/root/MFG/ctl_led.sh bi off
else
	/root/MFG/ctl_led.sh bi on
fi

exit 0
