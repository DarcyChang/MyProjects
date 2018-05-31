#! /bin/bash 

source /root/automation/Library/path.sh

real_msata_fw="L17606"

iSMART_64 -d /dev/sda | tee -a $log_path | tee $tmp_path
get_msata_fw=$( cat $tmp_path | grep FW | cut -d " " -f 3)
#echo "[DEBUG] GET MSATA FW = $get_msata_fw"
if [[ $get_msata_fw == $real_msata_fw ]] ; then
	echo "MSATA_FIRMWARE_CHECK: PASS" >> $test_result_path
else
	echo "MSATA_FIRMWARE_CHECK: FAIL: Wrong MSATA FW version!" >> $test_result_path
fi

