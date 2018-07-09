#! /bin/bash

#source /root/automation/Library/path.sh
test_result_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/T55_MFG/mfg_version | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/T55_MFG/mfg_version | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_path" | awk '{print $2}')
time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "time_path" | awk '{print $2}')
current_time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "current_time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_golden_path" | awk '{print $2}')   


function get_time(){
	date "+%G-%m-%d %H:%M:%S" > $current_time_path
    CURRENT_TIME=$(cat $current_time_path)
}

get_time

/root/automation/T55_MFG/testRtc.sh set | tee -a $log_path
sleep 2
/root/automation/T55_MFG/testRtc.sh check | tee -a $log_path | tee $tmp_path

rtc=$(cat $tmp_path)

echo "[SENAO] Set current time :" | tee -a $log_path
date -s "$CURRENT_TIME" | tee -a $log_path
echo "[SENAO] Set RTC time :" | tee -a $log_path
hwclock -w
hwclock -r | tee -a $log_path

if [[ $rtc == "pass" ]] ; then                                                                                                                                       
	echo "RTC_TEST: PASS" >> $test_result_path
else
	echo "RTC_TEST: FAIL" >> $test_result_path
fi
