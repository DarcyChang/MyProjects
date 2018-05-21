#! /bin/bash

ERROR=0

/root/automation/T55_MFG/usb_format.sh | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
usb_format=$( cat /tmp/log_tmp.txt | grep "Format process is completed.")
#echo "[DEBUG] usb_format = $usb_format" | tee -a /root/automation/log.txt
if [ "$usb_format" != "Format process is completed." ]; then
	echo "BURN_IN_TEST: FAIL: USB format is not complete." >> /root/automation/test_results.txt
	ERROR=1
fi

echo "BURN_IN_TEST: FAIL: USB/CPU/Memory test not terminated normally." >> /root/automation/test_results.txt
/root/automation/T55_MFG/stress.sh --no_iperf | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
stress_cpu=$( cat /tmp/log_tmp.txt | grep "Status:" | awk '{print $3}' )
sed -i '$d' /root/automation/test_results.txt
#echo "[DEBUG] stress_cpu = $stress_cpu" | tee -a /root/automation/log.txt
if [ "$stress_cpu" == "PASS" ]; then
	echo "BURN_IN_TEST: PASS: USB/CPU/Memory" >> /tmp/test_results.txt
else
	echo "BURN_IN_TEST: FAIL: USB/CPU/Memory test failed." >> /root/automation/test_results.txt
	ERROR=1	
fi

echo "BURN_IN_TEST: FAIL: iperf not terminated normally." >> /root/automation/test_results.txt
sshpass -p readwrite ssh -o ServerAliveInterval=60 -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/burn_in_test_golden.sh" | tee -a /root/automation/log.txt | tee /tmp/log_tmp_golden.txt &
sleep 1
/root/automation/T55_MFG/stress.sh --no_stress --no_disk | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
sleep 2
stress_iperf=$( cat /tmp/log_tmp.txt | grep "check total" | awk '{ print $5 }' )
sed -i '$d' /root/automation/test_results.txt
if [ "$stress_iperf" == "[pass]" ]; then
	echo "BURN_IN_TEST: PASS: DUT iperf." >> /tmp/test_results.txt
else
	ERROR=1
	eid_list="0 1 2 3 4"
	for eid in $eid_list; do
		tmp=$( cat /tmp/log_tmp.txt | grep "eth$eid check average" | awk '{ print $6 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a /root/automation/log.txt
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: eth$eid average rx/tx rate failed." >> /root/automation/test_results.txt
		fi
		tmp=$( cat /tmp/log_tmp.txt | grep "eth$eid check link" | awk '{ print $5 }' )
#		echo "[DEBUG] eth$eid = $tmp" | tee -a /root/automation/log.txt
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: eth$eid link status failed." >> /root/automation/test_results.txt
		fi
	done
fi
sleep 1
stress_iperf_golden=$( cat /tmp/log_tmp_golden.txt | grep "total" | awk '{ print $5 }' )
if [ "$stress_iperf_golden" == "[pass]" ]; then
	echo "BURN_IN_TEST: PASS: Golden iperf." >> /tmp/test_results.txt
else
#	ERROR=1
	eid_list="0 1 2 3 4"
	for eid in $eid_list; do
		tmp=$( cat /tmp/log_tmp_golden.txt | grep "eth$eid check average" | awk '{ print $6 }' )
#		echo "[DEBUG] golden eth$eid = $tmp" | tee -a /root/automation/log.txt
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: Golden sample eth$eid average rx/tx rate failed." >> /root/automation/test_results.txt
		fi
		tmp=$( cat /tmp/log_tmp_golden.txt | grep "eth$eid check link" | awk '{ print $5 }' )
#		echo "[DEBUG] golden eth$eid = $tmp" | tee -a /root/automation/log.txt
		if [ "$tmp" == "[failed]" ]; then
			echo "BURN_IN_TEST: FAIL: Golden sample eth$eid link status failed." >> /root/automation/test_results.txt
		fi
	done
fi

echo "[DEBUG] stress ERROR =  $ERROR" | tee -a /root/automation/log.txt
if [ "$ERROR" == "0" ]; then
	echo "BURN_IN_TEST: PASS" >> /root/automation/test_results.txt
fi
