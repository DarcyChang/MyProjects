#! /bin/bash

/root/automation/T55_MFG/hwconfig 2> /dev/null | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_mem_size=$( cat /tmp/log_tmp.txt | grep Memory: | awk '{print $2}' )

if [[ $get_mem_size == "1.8GB" ]];then
    echo "MEMORY_SIZE_CHECK: PASS" >> /root/automation/test_results.txt
else
    echo "MEMORY_SIZE_CHECK: FAIL: <Memory size is $get_mem_size>" >> /root/automation/test_results.txt
fi


