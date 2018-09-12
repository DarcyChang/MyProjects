#! /bin/bash                                                       

#source /root/automation/Library/path.sh
test_result_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/T55_MFG/mfg_version | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/T55_MFG/mfg_version | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_path" | awk '{print $2}')
log_folder_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_folder_path" | awk '{print $2}')
time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_golden_path" | awk '{print $2}')   

tpm_selftest -l debug | tee -a $log_path | tee $tmp_path
get_tpm_status=$( cat $tmp_path | grep "succeeded" | cut -d " " -f 2)
get_tpm_success_num=$(grep -c "success" $tmp_path)

/root/automation/T55_MFG/tpmtools/verify_tpm_keys.sh -w | tee $tmp_path
get_tpm_key=$(grep -c "KEY" $tmp_path)

if [[ $get_tpm_status == "succeeded" ]] && [[ $get_tpm_success_num == "7" ]] && [[  $get_tpm_key == "4" ]] ;then
    echo "$(date '+%Y-%m-%d %H:%M:%S') TPM_TEST: PASS" >> $test_result_path
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') TPM_TEST: FAIL" >> $test_result_path
fi

cp -rf /root/automation/T55_MFG/tpmtools/logs $log_folder_path
