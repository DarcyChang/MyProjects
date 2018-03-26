#! /bin/bash 

readmfg wg | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_wg=$( cat /tmp/log_tmp.txt | cut -d ":" -f 1)

readmfg oem | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_oem=$( cat /tmp/log_tmp.txt | grep oem: | cut -d " " -f 1)                                                                                                                          

readmacs | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_mac=$( cat /tmp/log_tmp.txt | grep device | cut -d " " -f 3)

hwclock -r | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_hwclock=$( cat /tmp/log_tmp.txt | cut -d " " -f 10)

if [[ $get_wg == "wg" ]] && [[ $get_oem == "oem:" ]] && [[ $get_mac == "macaddres:" ]] && [[ $get_hwclock == "seconds" ]];then
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: PASS" >> /root/automation/test_results.txt
else
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: FAIL" >> /root/automation/test_results.txt
fi 
