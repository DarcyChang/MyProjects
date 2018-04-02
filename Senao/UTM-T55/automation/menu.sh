#!/bin/bash

VERSION=1.1.0


function menu(){
	echo "0. Golden Sample " | tee -a /root/automation/log.txt
	echo "1. All test items (Default)" | tee -a /root/automation/log.txt
	echo "2. BOM CHECK" | tee -a /root/automation/log.txt
	echo "3. RTC TEST" | tee -a /root/automation/log.txt
	echo "4. TPM TEST" | tee -a /root/automation/log.txt
	echo "5. HW MONITOR TEST" | tee -a /root/automation/log.txt
	echo "6. ID EEPROM TEST" | tee -a /root/automation/log.txt
	echo "7. S/N, OEM S/N, MAC ADDRESS CHECK-ONLY" | tee -a /root/automation/log.txt
	echo "8. NETWORK TEST" | tee -a /root/automation/log.txt
	echo "9. MEMORY TESTS" | tee -a /root/automation/log.txt
	echo "10. BURN IN TEST" | tee -a /root/automation/log.txt
	echo "11. SYSTEM LEDS TEST"
	echo "12. LAN speed LED check"
	echo "97. Show Results" | tee -a /root/automation/log.txt
	echo "98. Delete Flag" | tee -a /root/automation/log.txt
	echo "99. Cancel" | tee -a /root/automation/log.txt

	echo "" | tee -a /root/automation/log.txt
	
}

echo "" | tee -a /root/automation/log.txt
echo "###################################" | tee -a /root/automation/log.txt
echo "###### SENAO RMA IMAGE ############" | tee -a /root/automation/log.txt
echo "###### Version $VERSION   ############" | tee -a /root/automation/log.txt
echo "###### Date 2018/04/03 ############" | tee -a /root/automation/log.txt
echo "###################################" | tee -a /root/automation/log.txt
echo "" | tee -a /root/automation/log.txt

menu

read -p "Please select your test item in 10 seconds :  " -t 10 select
echo "" | tee -a /root/automation/log.txt

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
