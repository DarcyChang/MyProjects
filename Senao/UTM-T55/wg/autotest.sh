#!/bin/bash

source /root/automation/Library/path.sh

function help() {
	echo "usage: autotest.sh <command>"
	echo ""
	echo "Following are commands:"
	echo "    all              Do all item automation."
	echo "    retest           Force to retest all."
	echo "    fetch-results    Prints out the results."
	echo "    del-flag         Deltet all results and flag files."
	echo "    msata-fw         MSATA firmware check."
	echo "    bom              BOM check."	
	echo "    rtc              RTC test."	
	echo "    mem-size         Memory size check."	
	echo "    tpm              TPM test."	
	echo "    hw-monitor       Hardware monitor test."	
	echo "    eeprom           ID EEPROM test."	
	echo "    sn-mac           S/N, OEM S/N, MAC address check-only."	
	echo "    network          Network_test, include iPerf Test with Throughput and iPerf Test with Packet loss."	
	echo "    mem-test         Memory stress test."	
	echo "    burn-in          Burn in test."	
}


function fetch-results() {
	if [ -f $test_result_path ];then
		cat $test_result_path
		echo ""
		cat $test_result_failure_path
		exit 0
	else
		echo "No test results!"	
		exit 0
	fi
}


function del-flag() {
	if [ ! -d "$log_backup_path" ]; then
    	echo "Directory $log_backup_path does not exists. Creating it."
		mkdir $log_backup_path
	fi
	
	dir=$(date +%Y%m%d%H%M%S)
	mkdir $log_backup_path/$dir
	mv $test_result_path $log_backup_path/$dir
	mv $test_result_failure_path $log_backup_path/$dir
	mv $all_test_done_path $log_backup_path/$dir
	mv $memory_stress_test_path $log_backup_path/$dir
	mv $log_path $log_backup_path/$dir
	mv $time_path $log_backup_path/$dir
}


function is_test_result_exist() {
	if [ -f $test_result_path ];then
		test_item=$(cat $test_result_path | cut -d ":" -f 1)
#		echo "[DEBUG] $test_item"
	else
		echo "[DEBUG] File $test_result_path not found!"
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


function memory_stess_pass() {
	if [ -f $test_result_path ];then
		tmp=$(cat $test_result_path | grep "MEMORY_TEST" |awk '{print $2}')
#		echo "[DEBUG] Memory test $tmp"
	else
		echo "$test_result_path isn't exist."
	fi

	if [[ $tmp == "PASS" ]];then
		return 0
	else 
		return 1
	fi
}

function hw_version(){
	hw_ver=$(cat /sys/class/dmi/id/board_version)
	if [ $hw_ver == "1.0" ] ; then
		echo "[SENAO] EVT board (Hardware version $hw_ver)" | tee -a $log_path
	elif [ $hw_ver == "1.1" ] ; then
		echo "[SENAO] DVT board (Hardware version $hw_ver)" | tee -a $log_path
	elif [ $hw_ver == "1.2" ] ; then
		echo "[SENAO] PVT/MP board (Hardware version $hw_ver)" | tee -a $log_path
	else
		echo "[ERROR] Unknown Hardware version $hw_ver" | tee -a $log_path 
	fi
}
	
function all() {
#	echo "START TIME $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $time_path
	echo "" | tee -a $log_path
	hw_version
	echo "[SENAO] All test items automation start......" | tee -a $log_path
	echo "" | tee -a $log_path

	is_test_result_exist

	is_done BOM_CHECK 
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/bom_check.sh
	fi

	is_done RTC_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/rtc_test.sh
	fi

	is_done MEMORY_SIZE_CHECK
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/mem_size_check.sh  
	fi

	is_done TPM_TEST 
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/tpm_test.sh
	fi

	is_done HW_MONITOR_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/superIO.sh
	fi

	is_done ID_EEPROM_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/EEPROM_ID_Test.sh
	fi

	is_done S/N_OEM_S/N_MAC_Address_CHECK-ONLY
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/sn_mac_check.sh
	fi

	is_done NETWORK_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/network_test.sh
	fi

	echo "MEMORY TEST TIME $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $time_path
	is_done MEMORY_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/memory_test.sh
	fi

	memory_stess_pass
	if [ $? -eq 1 ] ; then
		echo "BURN_IN_TEST: FAIL: Memory test failure, skip this step." >> $test_result_path
		exit 1
	fi	

	echo "BURN-IN TIME $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $time_path
	is_done BURN_IN_TEST
	if [ $? -eq 0 ] ; then
		/root/automation/T55_MFG/burn_in_test.sh
	fi

	echo "" | tee -a $log_path
	echo "[SENAO] All test items automation finished......" | tee -a $log_path
	echo "" | tee -a $log_path
	echo "END TIME $(date '+%Y-%m-%d %H:%M:%S')" | tee -a $time_path
}



if [ $# -eq 1 ];then
	case $1 in
		"all")
			if [ -f $all_test_done_path ];then
				echo "[SENAO] ALL TEST DONE!"
				exit 0
			fi
			all
			date > $all_test_done_path
			;;
		"retest")
			del-flag
			all
		;;
		"fetch-results")
			fetch-results
			;;
		"del-flag")	
			del-flag
			;;
		"msata-fw")	
			/root/automation/T55_MFG/msata_fw_check.sh
			;;
		"bom")	
			/root/automation/T55_MFG/bom_check.sh
			;;
		"rtc")	
			/root/automation/T55_MFG/rtc_test.sh
			;;
		"mem-size")	
		/root/automation/T55_MFG/mem_size_check.sh  
			;;
		"tpm")	
			/root/automation/T55_MFG/tpm_test.sh
			;;
		"hw-monitor")	
			/root/automation/T55_MFG/superIO.sh
			;;
		"eeprom")	
			/root/automation/T55_MFG/EEPROM_ID_Test.sh
			;;
		"sn-mac")	
			/root/automation/T55_MFG/sn_mac_check.sh
			;;
		"network")	
			/root/automation/T55_MFG/network_test.sh
			;;
		"mem-test")	
			/root/automation/T55_MFG/memory_test.sh
			;;
		"burn-in")	
			/root/automation/T55_MFG/burn_in_test.sh
			;;
		*)
			echo "[ERROR] Wrong command."
			echo ""
			help
			exit 1
			;;
	esac
else
	echo "[ERROR] Mismatch number of parameters."
	echo ""
	help
	exit 1
fi

