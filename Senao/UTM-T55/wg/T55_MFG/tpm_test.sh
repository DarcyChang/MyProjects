#! /bin/bash                                                       

source /root/automation/Library/path.sh

tpm_selftest -l info | tee -a $log_path | tee $tmp_path
get_tpm_status=$( cat $tmp_path | grep selftest | cut -d " " -f 2)

if [[ $get_tpm_status == "succeeded" ]];then
    echo "TPM_TEST: PASS" >> $test_result_path
else
    echo "TPM_TEST: FAIL" >> $test_result_path
fi

