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


function kill_iperf(){
	killall -9 iperf &> /dev/null
	sleep 1
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "killall -9 iperf &> /dev/null" &
	sleep 1
}


function ps_iperf(){
	echo "" | tee -a $log_path
	echo "[SENAO] DUT ps -ax" | tee -a $log_path
	ps -ax | tee -a $log_path
	echo "" | tee -a $log_path
	echo "[SENAO] GS ps -ax" | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "ps -ax" | tee -a $log_path
}


/root/automation/T55_MFG/usb_format.sh | tee -a $log_path | tee $tmp_path
usb_format=$( cat $tmp_path | grep "Format process is completed.")
#echo "[DEBUG] usb_format = $usb_format" | tee -a $log_path
if [ "$usb_format" != "Format process is completed." ]; then
	echo "BURN_IN_TEST: FAIL: USB format is not complete." >> $test_result_path
fi

echo "BURN_IN_TEST: FAIL: Burn-in test not terminated normally." >> $test_result_path
kill_iperf
sleep 1
sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/iperf_server.sh" | tee -a $log_path | tee $tmp_golden_path &
sleep 1
/root/automation/T55_MFG/iperf_server.sh | tee -a $log_path | tee $tmp_path
#sleep 1
#ps_iperf
sleep 10
sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/stress_iperf.sh" | tee -a $log_path | tee $tmp_golden_path &
sleep 1
/root/automation/T55_MFG/stress.sh | tee -a $log_path | tee $tmp_path 
sleep 2
stress_cpu=$( cat $tmp_path | grep "Status:" | awk '{print $3}' )
#echo "[DEBUG] stress_cpu = $stress_cpu" | tee -a $log_path
stress_iperf=$( cat $tmp_path | grep "check total" | awk '{ print $6 }' )
sed -i '/BURN_IN_TEST: FAIL: Burn-in test not terminated normally/d' $test_result_path
if [ "$stress_cpu" == "PASS" ]; then
	echo "BURN_IN_TEST: PASS: USB/CPU/Memory PASS" >> $test_result_path
else
	echo "BURN_IN_TEST: FAIL: USB/CPU/Memory test failed." >> $test_result_path
fi
if [ "$stress_iperf" == "[pass]" ]; then
	echo "BURN_IN_TEST: PASS: iperf PASS" >> $test_result_path
else
    port_num=$(ifconfig -a | grep eth | wc -l)                                                                                                                           
    for ((eid=0; eid<$port_num; eid++))
	do
		tmp=$( cat $tmp_path | grep "eth$eid check average" | awk '{ print $7 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: [DUT] eth$eid average rx/tx rate failed." >> $test_result_path
		fi
		tmp=$( cat $tmp_path | grep "eth$eid check link" | awk '{ print $6 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a $log_path
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: [DUT] eth$eid link status failed." >> $test_result_path
		fi
	done
fi
sleep 1

kill_iperf
#ps_iperf
