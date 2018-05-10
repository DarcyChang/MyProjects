#! /bin/bash                                                       

tpm_selftest -l info | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_tpm_status=$( cat /tmp/log_tmp.txt | grep selftest | cut -d " " -f 2)

if [[ $get_tpm_status == "succeeded" ]];then
    echo "TPM_TEST: PASS" >> /root/automation/test_results.txt
else
    echo "TPM_TEST: FAIL" >> /root/automation/test_results.txt
fi

