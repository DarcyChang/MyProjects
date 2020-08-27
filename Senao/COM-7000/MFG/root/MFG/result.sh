#!/bin/bash
# Author Darcy.Chang
# Date 2020.08.31
# Version 1.2.0

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
echo "[DEBUG] CPU serial number $cpu_sn" | tee -a $stress_log_file
cp -rf /root/MFG/logs /root/MFG/$cpu_sn_$timestamp


if [[ $pass_num -eq 6 ]] ;then
	/root/MFG/ctl_led.sh bi off
else
	/root/MFG/ctl_led.sh bi on
fi

exit 0
