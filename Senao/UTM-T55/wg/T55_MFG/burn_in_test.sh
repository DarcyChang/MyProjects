#! /bin/bash

source /root/automation/Library/path.sh

ERROR=0

/root/automation/T55_MFG/usb_format.sh | tee -a $log_path | tee $tmp_path
usb_format=$( cat $tmp_path | grep "Format process is completed.")
#echo "[DEBUG] usb_format = $usb_format" | tee -a $log_path
if [ "$usb_format" != "Format process is completed." ]; then
	echo "BURN_IN_TEST: FAIL: USB format is not complete." >> $test_result_path
	ERROR=1
fi

echo "BURN_IN_TEST: FAIL: USB/CPU/Memory test not terminated normally." >> $test_result_path
/root/automation/T55_MFG/stress.sh --no_iperf | tee -a $log_path | tee $tmp_path
stress_cpu=$( cat $tmp_path | grep "Status:" | awk '{print $3}' )
sed -i '$d' $test_result_path
#echo "[DEBUG] stress_cpu = $stress_cpu" | tee -a $log_path
if [ "$stress_cpu" == "PASS" ]; then
	echo "BURN_IN_TEST: PASS: USB/CPU/Memory" >> $test_result_path
else
	echo "BURN_IN_TEST: FAIL: USB/CPU/Memory test failed." >> $test_result_path
	ERROR=1	
fi

echo "BURN_IN_TEST: FAIL: iperf not terminated normally." >> $test_result_path
sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/burn_in_test_golden.sh" | tee -a $log_path | tee $tmp_golden_path &
sleep 1
/root/automation/T55_MFG/stress.sh --no_stress --no_disk | tee -a $log_path | tee $tmp_path
sleep 2
stress_iperf=$( cat $tmp_path | grep "check total" | awk '{ print $5 }' )
sed -i '$d' $test_result_path
if [ "$stress_iperf" == "[pass]" ]; then
	echo "BURN_IN_TEST: PASS" >> $test_result_path
else
	ERROR=1
	eid_list="0 1 2 3 4"
	for eid in $eid_list; do
		tmp=$( cat $tmp_path | grep "eth$eid check average" | awk '{ print $6 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: eth$eid average rx/tx rate failed." >> $test_result_path
		fi
		tmp=$( cat $tmp_path | grep "eth$eid check link" | awk '{ print $5 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: eth$eid link status failed." >> $test_result_path
		fi
	done
fi
sleep 1
stress_iperf_golden=$( cat $tmp_golden_path | grep "total" | awk '{ print $5 }' )
if [ "$stress_iperf_golden" == "[pass]" ]; then
	echo "BURN_IN_TEST: PASS: Golden iperf pass." >> $test_result_path
else
#	ERROR=1
	eid_list="0 1 2 3 4"
	for eid in $eid_list; do
		tmp=$( cat $tmp_golden_path | grep "eth$eid check average" | awk '{ print $6 }' )
#		echo "[DEBUG] golden eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: Golden sample eth$eid average rx/tx rate failed." >> $test_result_path
		fi
		tmp=$( cat $tmp_golden_path | grep "eth$eid check link" | awk '{ print $5 }' )
#		echo "[DEBUG] golden eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: Golden sample eth$eid link status failed." >> $test_result_path
		fi
	done
fi

echo "[DEBUG] stress ERROR =  $ERROR" | tee -a $log_path
if [ "$ERROR" == "0" ]; then
	echo "BURN_IN_TEST: PASS" >> $test_result_path
fi

killall -9 iperf &> /dev/null
sleep 1
sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "killall -9 iperf &> /dev/null" &
