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

readmfg wg | tee -a $log_path | tee $tmp_path
get_wg=$( cat $tmp_path | cut -d ":" -f 1)
wg_number=$( cat $tmp_path | cut -d ":" -f 2)

readmfg oem | tee -a $log_path | tee $tmp_path
get_oem=$( cat $tmp_path | grep oem: | cut -d " " -f 1)
oem_sn=$( cat $tmp_path | grep oem: | cut -d " " -f 2) 

readmacs | tee -a $log_path | tee $tmp_path
get_mac=$( cat $tmp_path | grep device | cut -d " " -f 3)
mac_address=$( cat $tmp_path | grep device | cut -d " " -f 4)

hwclock -r | tee -a $log_path | tee $tmp_path
get_hwclock=$( cat $tmp_path | awk '{print $7}')
hwclock=$( cat $tmp_path)

if [[ $get_wg == "wg" ]] && [[ $get_oem == "oem:" ]] && [[ $get_mac == "macaddres:" ]] && [[ $get_hwclock == "seconds" ]];then
    echo "$(date '+%Y-%m-%d %H:%M:%S') S/N_OEM_S/N_MAC_Address_CHECK-ONLY: PASS" >> $test_result_path
else
	if [[ $get_wg != "wg" ]] ; then
    	echo "[ERROR] get_wg is $get_wg" | tee -a $log_path
	fi
	if [[ $get_oem != "oem:" ]] ; then
    	echo "[ERROR] get_oem is $get_oem" | tee -a $log_path
	fi
	if [[ $get_mac != "macaddres:" ]] ; then
    	echo "[ERROR] get_mac is $get_mac" | tee -a $log_path
	fi
	if [[ $get_hwclock != "seconds" ]] ; then
    	echo "[ERROR] get_hwclock is $get_hwclock" | tee -a $log_path
	fi
    echo "$(date '+%Y-%m-%d %H:%M:%S') S/N_OEM_S/N_MAC_Address_CHECK-ONLY: FAIL: <wg is $wg_number, oem s/n is $oem_sn, MAC Address is $mac_address, hwclock is $hwclock>" >> $test_result_path
fi 
