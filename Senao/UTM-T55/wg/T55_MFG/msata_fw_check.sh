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

real_msata_fw="L17606"

iSMART_64 -d /dev/sda | tee -a $log_path | tee $tmp_path
get_msata_fw=$( cat $tmp_path | grep FW | cut -d " " -f 3)
#echo "[DEBUG] GET MSATA FW = $get_msata_fw"
if [[ $get_msata_fw == $real_msata_fw ]] ; then
	echo "MSATA_FIRMWARE_CHECK: PASS" >> $test_result_path
else
	echo "MSATA_FIRMWARE_CHECK: FAIL: Wrong MSATA FW version!" >> $test_result_path
fi

