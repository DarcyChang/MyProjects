#! /bin/bash

source /root/automation/Library/path.sh

/root/automation/T55_MFG/hwconfig 2> /dev/null | tee -a $log_path | tee $tmp_path
get_mem_size=$( cat $tmp_path | grep Memory: | awk '{print $2}' )

if [[ $get_mem_size == "1.8GB" ]];then
    echo "MEMORY_SIZE_CHECK: PASS" >> $test_result_path
else
    echo "MEMORY_SIZE_CHECK: FAIL: <Memory size is $get_mem_size>" >> $test_result_path
fi


