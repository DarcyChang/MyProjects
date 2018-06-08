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

echo "MEMORY_TEST: FAIL: Not terminated normally." >> $test_result_path

free_memory=$(free -m | grep Mem | awk '{print $4}')
memory_loop=$(cat /root/automation/T55_MFG/mfg_version | grep "Memory Test loop number" | awk '{print $5}')
#echo "[DEBUG] free memory : $free_memory , memory test loop : $memory_loop"
echo "Memory test start..." | tee -a $log_path
#echo "This could take 4 hours, so wait for it." | tee -a $log_path
time memtester $free_memory $memory_loop | tee -a $log_path | tee -a $memory_stress_test_path

failure_count=$(grep -c "FAILURE" $memory_stress_test_path)
#echo "[DEBUG] FAILURE number $failure_count"
sed -i '$d' $test_result_path
if [ "$failure_count" == "0" ]; then
	echo "MEMORY_TEST: PASS" >> $test_result_path
else
	echo "MEMORY_TEST: FAIL" >> $test_result_path
fi
