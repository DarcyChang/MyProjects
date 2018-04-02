#! /bin/bash 

readmfg wg | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_wg=$( cat /tmp/log_tmp.txt | cut -d ":" -f 1)
wg_number=$( cat /tmp/log_tmp.txt | cut -d ":" -f 2)

readmfg oem | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_oem=$( cat /tmp/log_tmp.txt | grep oem: | cut -d " " -f 1)
oem_sn=$( cat /tmp/log_tmp.txt | grep oem: | cut -d " " -f 2) 

readmacs | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_mac=$( cat /tmp/log_tmp.txt | grep device | cut -d " " -f 3)
mac_address=$( cat /tmp/log_tmp.txt | grep device | cut -d " " -f 4)

hwclock -r | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_hwclock=$( cat /tmp/log_tmp.txt | cut -d " " -f 10)
hwclock=$( cat /tmp/log_tmp.txt)

if [[ $get_wg == "wg" ]] && [[ $get_oem == "oem:" ]] && [[ $get_mac == "macaddres:" ]] && [[ $get_hwclock == "seconds" ]];then
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: PASS" >> /root/automation/test_results.txt
else
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: FAIL: <wg is $wg_number, oem s/n is $oem_sn, MAC Address is $mac_address, hwclock is $hwclock>" >> /root/automation/test_results.txt
fi 
