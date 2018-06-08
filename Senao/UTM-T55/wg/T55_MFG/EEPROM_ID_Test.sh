#!/bin/bash

#source /root/automation/Library/path.sh
test_result_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/T55_MFG/mfg_version | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/T55_MFG/mfg_version | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_path" | awk '{print $2}')
time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_golden_path" | awk '{print $2}')   

SMBUS=$(i2cdetect -l | grep smbus | cut -c 5)
PASS=1
num_list=(0 127 255)
check_num=(0x00 0x7f 0xff)
add_list="0x56 0x57"

for addr in $add_list; do
    for((num = 0; num < 3; num ++)); do 
        echo "[DEBUG] Set SMBUS $addr to ${num_list[$num]}"
    	i2cset -y $SMBUS $addr 0x05 ${num_list[$num]}
    	result=$(i2cget -y $SMBUS $addr 0x05)
    	echo "[DEBUG] Get: $result"
        if [ "$result" != "${check_num[$num]}" ]; then
			PASS=0
    	fi
    done
done

if [ $PASS == "1" ]; then 
    echo EEPROM ID Test Pass!!
    echo "ID_EEPROM_TEST: PASS" >> $test_result_path
else
    echo EEPROM ID Test Fail!!
    echo "ID_EEPROM_TEST: FAIL: <Result is $result>" >> $test_result_path
fi
