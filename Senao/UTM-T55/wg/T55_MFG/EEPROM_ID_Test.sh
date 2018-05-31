#!/bin/bash

source /root/automation/Library/path.sh

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
