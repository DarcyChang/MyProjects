#! /bin/bash

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

/root/automation/T55_MFG/hwconfig 2> /dev/null | tee -a $log_path | tee $tmp_path
get_mem_size=$( cat $tmp_path | grep Memory: | awk '{print $2}' )

if [[ $get_mem_size == "1.8GB" ]];then
    echo "$(date '+%Y-%m-%d %H:%M:%S') MEMORY_SIZE_CHECK: PASS" >> $test_result_path
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') MEMORY_SIZE_CHECK: FAIL: <Memory size is $get_mem_size>" >> $test_result_path
fi


