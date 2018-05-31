#! /bin/bash 

source /root/automation/Library/path.sh

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
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: PASS" >> $test_result_path
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
    echo "S/N_OEM_S/N_MAC_Address_CHECK-ONLY: FAIL: <wg is $wg_number, oem s/n is $oem_sn, MAC Address is $mac_address, hwclock is $hwclock>" >> $test_result_path
fi 
