#!/bin/bash
# Author Darcy.Chang
# Date 2020.09.18
# Version 1.3.0

result_file=/root/MFG/logs/result.txt
stress_log_file=/root/MFG/logs/log.txt
tmp_stress_file=/root/MFG/logs/tmp_stress.txt

rm /root/MFG/logs/*

#timedatectl set-timezone Asia/Taipei
#timestamp=$(date +%Y%m%d%H%M%S)
echo "" | tee -a $stress_log_file
echo "[SENAO]" $(date) | tee $result_file |tee -a $stress_log_file

#mv $result_file /root/MFG/logs/result_$timestamp.txt
#mv $stress_log_file /root/MFG/logs/log_$timestamp.txt
rm $result_file
rm $stress_log_file

echo "10" > /proc/suio_gpio | tee -a $stress_log_file
i2cset -y 0 0x21 0x07 0x00
/root/MFG/ctl_led.sh echo off
/root/MFG/ctl_led.sh sys off
/root/MFG/ctl_led.sh bi off
/root/MFG/ctl_led.sh eth off

