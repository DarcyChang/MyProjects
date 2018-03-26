#! /bin/bash

/root/automation/T55_MFG/hwconfig | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_mem_size=$( cat tee /tmp/log_tmp.txt | grep Memory | cut -d " " -f 9)

if [[ $get_mem_size == "2GB" ]];then
    echo "MEMORY_SIZE_CHECK: PASS" >> /root/automation/test_results.txt
else
    echo "MEMORY_SIZE_CHECK: FAIL" >> /root/automation/test_results.txt
fi


