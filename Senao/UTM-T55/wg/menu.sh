#!/bin/bash

source /root/automation/Library/path.sh 

VERSION=2.2.0

function menu(){
	echo "0. Golden Sample " | tee -a $log_path
	echo "1. All test items (Default)" | tee -a $log_path
	echo "2. BOM CHECK" | tee -a $log_path
	echo "3. RTC TEST" | tee -a $log_path
	echo "4. TPM TEST" | tee -a $log_path
	echo "5. HW MONITOR TEST" | tee -a $log_path
	echo "6. ID EEPROM TEST" | tee -a $log_path
	echo "7. S/N, OEM S/N, MAC ADDRESS CHECK-ONLY" | tee -a $log_path
	echo "8. NETWORK TEST" | tee -a $log_path
	echo "9. MEMORY TEST" | tee -a $log_path
	echo "10. BURN IN TEST" | tee -a $log_path
	echo "11. SYSTEM LEDS TEST"
	echo "12. LAN speed LED check"
	echo "13. Force to retest all"
	echo "97. Show Results" | tee -a $log_path
	echo "98. Delete Flag" | tee -a $log_path
	echo "99. Cancel" | tee -a $log_path

	echo "" | tee -a $log_path
	
}


echo "" | tee -a $log_path 
echo "###################################" | tee -a $log_path
echo "###### SENAO RMA IMAGE ############" | tee -a $log_path
echo "###### Version $VERSION   ############" | tee -a $log_path
echo "###### Date 2018/05/21 ############" | tee -a $log_path
echo "###################################" | tee -a $log_path
echo "" | tee -a $log_path

menu

#device=$(cat /root/automation/config | grep Device | awk '{print $2}')        
#if [ "$device" == "2" ] ; then                                     
#	echo "[SENAO] Golden Sample mode"
#	/root/automation/T55_MFG/set_ip.sh -g                     
#	exit 1        
#else
#	echo "[SENAO] DUT mode"                          
#fi

read -p "Please select your test item in 10 seconds :  " -t 10 select
echo "" | tee -a $log_path

if [ "$select" == "" ] ; then
	select=1
fi

case $select in 
	"0")
		echo "[SENAO] Be a golden sample."
		/root/automation/T55_MFG/set_ip.sh -g
		;;
	"1")
		echo "[SENAO] You select All test items."
		/root/automation/autotest.sh all
		;;
	"2")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh bom
		;;
	"3")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh rtc
		;;
	"4")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh tpm
		;;
	"5")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh hw-monitor
		;;
	"6")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh eeprom
		;;
	"7")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh sn-mac
		;;
	"8")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh network
		;;
	"9")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh mem-test
		;;
	"10")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh burn-in
		;;
	"11")
		echo "[SENAO] You select item $select"
		/root/automation/T55_MFG/SysLEDTest.sh
		;;
	"12")
		echo "[SENAO] You select item $select"
		/root/automation/T55_MFG/LanLEDTest.sh
		;;
	"13")
		echo "[SENAO] You select item $select"
		/root/automation/autotest.sh del-flag
		/root/automation/autotest.sh all
		;;
	"97")
		echo "[SENAO] Show test results."
		/root/automation/autotest.sh fetch-results
		;;
	"98")
		echo "[SENAO] Move all flag and results into backup folder.."
		/root/automation/autotest.sh del-flag
		;;
	"99")
		echo "[SENAO] Cancel"
		exit 0
		;;
	*)
		echo "[ERROR] You enter a wrong number $select !"
		;;
esac		
