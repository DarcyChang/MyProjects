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
count=0
ERROR=0

function is_test_result_exist() {
    if [ -f $test_result_path ];then
        test_item=$(cat $test_result_path | awk '{print $3}' | cut -d ":" -f 1)
    fi
    echo ""                                                                                                                                                              
}


function is_done() {
    for i in $test_item
        do
            if [[ $1 == $i ]];then
                echo "$1 is done."
                return 1
            fi
        done
    return 0
}


function bom_check_result(){
	tmp01=$( cat $test_result_path | grep -a "MSATA_FIRMWARE_CHECK" | awk '{print $2}')
    tmp02=$( cat $test_result_path | grep -a "Wi-Fi_DEVICE_CHECK" | awk '{print $2}')
    tmp03=$( cat $test_result_path | grep -a "TPM_DEVICE_CHECK" | awk '{print $2}')                                                                                 
    tmp04=$( cat $test_result_path | grep -a "ID_EEPROM_DEVICE_CHECK" | awk '{print $2}')
	tmp05=$( cat $test_result_path | grep -a "HW_MONITOR_DEVICE_CHECK" | awk '{print $2}')
	tmp06=$( cat $test_result_path | grep -a "NR_NETWORK_PORTS_COUNT_CHECK" | awk '{print $2}')
	tmp07=$( cat $test_result_path | grep -a "MEMORY_SIZE_CHECK" | awk '{print $2}')
    if [ "$tmp01" != "PASS" ] || [ "$tmp02" != "PASS" ] || [ "$tmp03" != "PASS" ] || [ "$tmp04" != "PASS" ] || [ "$tmp05" != "PASS" ]  || [ "$tmp06" != "PASS" ] || [ "$tmp07" != "PASS" ] ; then
        ERROR=1
    fi
}


function msata_fw_check(){
	iSMART_64 -d /dev/sda | tee -a $log_path | tee $tmp_path
	get_msata_fw=$( cat $tmp_path | grep FW | cut -d " " -f 3)
	if [[ $get_msata_fw == $real_msata_fw ]];then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') MSATA_FIRMWARE_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	else
    	echo "$(date '+%Y-%m-%d %H:%M:%S') MSATA_FIRMWARE_CHECK: FAIL: Wrong MSATA FW version!" >> $test_result_path
	fi
}


function wifi_device_check(){
	t55w=$(/root/automation/T55_MFG/readmfg wg | grep -q "wg: D023" && echo T55-W || echo T55)
	if [[ $t55w == "T55-W" ]] ; then
		/root/automation/T55_MFG/hwinfo.sh | tee -a $log_path | tee $tmp_path
		wifi=$( cat $tmp_path | grep Wi-Fi)
		#echo "[DEBUG] wifi module = $wifi"
		if [[ $wifi == "Wi-Fi check ok" ]];then
    		echo "$(date '+%Y-%m-%d %H:%M:%S') Wi-Fi_DEVICE_CHECK: PASS" >> $test_result_path
			count=$[ count + 1 ]
		else
    		echo "$(date '+%Y-%m-%d %H:%M:%S') Wi-Fi_DEVICE_CHECK: FAIL: Doesn't detect Wi-Fi module." >> $test_result_path
		fi
	else
		echo "[SENAO] No Wi-Fi module $t55w" | tee -a $log_path
		count=$[ count + 1 ]
	fi
}


function tpm_device_check(){
	tpm_selftest -l info | tee -a $log_path | tee $tmp_path
	tpm=$( cat $tmp_path | grep tpm_selftest | cut -d " " -f 2)
	#echo "[DEBUG] tpm status = $tpm"
	if [[ $tpm == "succeeded" ]];then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') TPM_DEVICE_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	else
    	echo "$(date '+%Y-%m-%d %H:%M:%S') TPM_DEVICE_CHECK: FAIL" >> $test_result_path
	fi
}


function id_eeprom_device_check(){
	i2cset -y 0 0x56 0x05 0xff | tee -a $log_path
	i2cset -y 0 0x57 0x05 0xff | tee -a $log_path
	eeprom01=$(i2cget -y 0 0x56 0x05)
	eeprom02=$(i2cget -y 0 0x57 0x05)
	if [[ $eeprom01 == "0xff" ]] && [[ $eeprom02 == "0xff" ]] ; then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') ID_EEPROM_DEVICE_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	else
    	echo "$(date '+%Y-%m-%d %H:%M:%S') ID_EEPROM_DEVICE_CHECK: FAIL" >> $test_result_path
	fi
}


function hw_monitor_device_check(){
	/root/automation/T55_MFG/superIO > /root/showIO
	pass_num=$(grep -c "pass" /root/showIO)
	if [ "$pass_num" == "7" ]; then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') HW_MONITOR_DEVICE_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	else
    	echo "$(date '+%Y-%m-%d %H:%M:%S') HW_MONITOR_DEVICE_CHECK: FAIL" >> $test_result_path
	fi
	rm /root/showIO
}


function nr_network_ports_count_check(){
	port_num=$(ifconfig -a | grep eth | wc -l)
	port_num_criteria=5
	#echo "[DEBUG] Total port number = $port_num"
	link_error=0 # connection
	
	echo "[SENAO] Setting DUT network configuration." | tee -a $log_path
	/root/automation/T55_MFG/set_ip.sh                                                                                                                                 
	sleep 3

    echo "[SENAO] Detecting DUT $port_num ports link status." | tee -a $log_path
    for ((eid=0; eid<$port_num; eid++))
    do
        link_state=$(ethtool eth$eid | grep 'Link detected' | awk '{print $3}')
        if [ $link_state != "yes" ] ; then
            echo "[WARNING] DUT port eth$eid link status $link_state" | tee -a $log_path | tee -a $test_result_failure_path 
            link_error=1 # disconnection
        fi      
    done

	echo "[SENAO] Detecting Golden Sample $port_num ports link status." | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/golden_networking.sh" | tee $tmp_golden_path
	golden_link_state=$(grep -c "no" $tmp_golden_path)
	if [ $golden_link_state -gt 0 ] ; then
		cat $tmp_golden_path | tee -a $log_path | tee -a $test_result_failure_path
		link_error=1 # disconnection
	fi

	if [[ $link_error == "1" ]] ;then
		echo "$(date '+%Y-%m-%d %H:%M:%S') NR_NETWORK_PORTS_COUNT_CHECK: FAIL: <RJ-45 disconnection>" >> $test_result_path
	elif [[ $port_num -ne $port_num_criteria ]] ;then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') NR_NETWORK_PORTS_COUNT_CHECK: FAIL: <Total port number is $port_num>" >> $test_result_path
	else
		echo "$(date '+%Y-%m-%d %H:%M:%S') NR_NETWORK_PORTS_COUNT_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	fi
}


function memory_size_check(){
	memory=$(/root/automation/T55_MFG/hwinfo.sh | grep Memory | cut -d " " -f 3)
	#echo "[DEBUG] Memory size = $memory"
	if [[ $memory == "ok" ]];then
    	echo "$(date '+%Y-%m-%d %H:%M:%S') MEMORY_SIZE_CHECK: PASS" >> $test_result_path
		count=$[ count + 1 ]
	else
    	echo "$(date '+%Y-%m-%d %H:%M:%S') MEMORY_SIZE_CHECK: FAIL" >> $test_result_path
	fi
}

is_test_result_exist

is_done MSATA_FIRMWARE_CHECK
if [ $? -eq 0 ] ; then
    msata_fw_check
fi

is_done Wi-Fi_DEVICE_CHECK
if [ $? -eq 0 ] ; then
    wifi_device_check
fi

is_done TPM_DEVICE_CHECK
if [ $? -eq 0 ] ; then
    tpm_device_check
fi

is_done ID_EEPROM_DEVICE_CHECK
if [ $? -eq 0 ] ; then
    id_eeprom_device_check
fi

is_done HW_MONITOR_DEVICE_CHECK
if [ $? -eq 0 ] ; then
    hw_monitor_device_check
fi

is_done NR_NETWORK_PORTS_COUNT_CHECK
if [ $? -eq 0 ] ; then
    nr_network_ports_count_check
fi

is_done MEMORY_SIZE_CHECK
if [ $? -eq 0 ] ; then
	memory_size_check
fi

bom_check_result
if [ "$ERROR" == "0" ] || [ "$count" == "7" ]; then
	echo "$(date '+%Y-%m-%d %H:%M:%S') BOM_CHECK: PASS" >> $test_result_path
else
	echo "$(date '+%Y-%m-%d %H:%M:%S') BOM_CHECK: FAIL" >> $test_result_path
fi
