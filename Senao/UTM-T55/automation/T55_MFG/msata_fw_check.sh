#! /bin/bash 

real_msata_fw="L17606"

iSMART_64 -d /dev/sda | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
get_msata_fw=$( cat /tmp/log_tmp.txt | grep FW | cut -d " " -f 3)
#echo "[DEBUG] GET MSATA FW = $get_msata_fw"
if [[ $get_msata_fw == $real_msata_fw ]] ; then
	echo "MSATA_FIRMWARE_CHECK: PASS" >> /root/automation/test_results.txt
else
	echo "MSATA_FIRMWARE_CHECK: FAIL: Wrong MSATA FW version!" >> /root/automation/test_results.txt
fi

