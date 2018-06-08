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

/root/automation/T55_MFG/superIO > /root/showIO
cat /root/showIO | tee -a $log_path
Pass_count=$(grep -c "pass" /root/showIO)
if [ "$Pass_count" == "7" ];
then
	echo "HW monitor Test Pass!!" | tee -a $log_path
	echo "HW_MONITOR_TEST: PASS" >> $test_result_path
else 
	echo "HW monitor Test Fail!!" | tee -a $log_path
	echo "HW_MONITOR_TEST: FAIL" >> $test_result_path
fi

rm /root/showIO
exit 0
