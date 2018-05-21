#! /bin/bash

test_result_path="/root/automation/test_results.txt"
ERROR=0


function is_test_result_exist() {
    if [ -f $test_result_path ];then
        test_item=$(cat $test_result_path | cut -d ":" -f 1)
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


function network_test_result(){
#	echo "[DEBUG] ERROR $ERROR"
	tmp01=$( cat $test_result_path | grep -a "TCP_Throughput" | awk '{print $2}')
	tmp02=$( cat $test_result_path | grep -a "UDP_packet_loss_high_rate" | awk '{print $2}')
	tmp03=$( cat $test_result_path | grep -a "UDP_packet_loss_low_rate" | awk '{print $2}')
	echo "[DEBUG] TCP Throughput $tmp01"
	echo "[DEBUG] UDP packet loss high rate $tmp02"
	echo "[DEBUG] UDP packet loss low rate $tmp03"
	if [ "$tmp01" != "PASS" ] || [ "$tmp02" != "PASS" ] || [ "$tmp03" != "PASS" ] ; then
		ERROR=1
	fi
	echo "[DEBUG] ERROR number $ERROR"
}


function is_etherphy_connection(){
	echo "[SENAO] Detecting DUT five ports link status." | tee -a /root/automation/log.txt
	igb=$(ls /proc/driver/igb/)
	link_state=$(cat /proc/driver/igb/$igb/test_mode | grep -c "DOWN")
	if [ $link_state -gt 0 ] ; then
		echo "[ERROR] Some ports link down." >> /root/automation/testresults-failure.txt
		cat /proc/driver/igb/$igb/test_mode | tee -a /root/automation/log.txt | tee -a /root/automation/testresults-failure.txt
		return 1
	fi
	
	echo "[SENAO] Detecting Golden sample five ports link status." | tee -a /root/automation/log.txt
	sshpass -p readwrite ssh -o ServerAliveInterval=60 -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/golden_networking.sh" | tee /tmp/log_tmp_golden.txt
	golden_link_state=$(grep -c "DOWN" /tmp/log_tmp_golden.txt)
	if [ $golden_link_state -gt 0 ] ; then
		echo "[ERROR] Golden sample's some ports link down." >> /root/automation/testresults-failure.txt
		cat /tmp/log_tmp_golden.txt | tee -a /root/automation/log.txt | tee -a /root/automation/testresults-failure.txt
		return 1
	fi

	return 0
}


function is_ping(){
    eid_list="0 1 2 3 4"
    for eid in $eid_list; do
		ping_working=$(ping -c5 192.168.$eid.2 |grep transmitted |awk '{print $4}')
		if [ $ping_working -eq 0 ] ; then
			echo "[ERROR] 192.168.$eid.1 ping 192.168.$eid.2 is not working." >> /root/automation/testresults-failure.txt
			return 1
		fi
    done
	return 0
}


function throughput_tcp(){
	echo "[SENAO] iPerf Test with Throughput start..." | tee -a /root/automation/log.txt
	echo "" | tee -a /root/automation/log.txt
	sshpass -p readwrite ssh -o ServerAliveInterval=60 -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_tcp.sh" | tee -a /root/automation/log.txt | tee /tmp/log_tmp_golden.txt &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -T 900 -f | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
	tcp=$(grep -c "failed" /tmp/log_tmp.txt)
	tcp_golden=$(grep -c "failed" /tmp/log_tmp_golden.txt)
	echo "[DEBUG] DUT failed count $tcp"
	echo "[DEBUG] Golden sample failed count $tcp_golden"
	if [ "$tcp" == "0" ] && [ "$tcp_golden" == "0" ]; then
	    echo "TCP_Throughput: PASS" >> /root/automation/test_results.txt
	elif [ "$tcp" != "0" ] && [ "$tcp_golden" != "0" ]; then 
    	echo "TCP_Throughput: FAIL: <Both of DUT and Golden sample failed.>" >> /root/automation/test_results.txt
	elif [ "$tcp" != "0" ] ; then 
    	echo "TCP_Throughput: FAIL: <DUT failed.>" >> /root/automation/test_results.txt
	elif [ "$tcp_golden" != "0" ] ; then
    	echo "TCP_Throughput: FAIL: <Golden sample failed.>" >> /root/automation/test_results.txt
	fi
	sleep 1
}

function throughput_udp_high(){
	echo "[SENAO] iPerf Test with Packet loss start..." | tee -a /root/automation/log.txt
	echo "" | tee -a /root/automation/log.txt
	sshpass -p readwrite ssh -o ServerAliveInterval=60 -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_udp_high.sh" | tee -a /root/automation/log.txt | tee /tmp/log_tmp_golden.txt &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -u -T 800 -L 3 -r 1 -f | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
	udp_high=$(grep -c "failed" /tmp/log_tmp.txt)
	udp_high_golden=$(grep -c "failed" /tmp/log_tmp_golden.txt)
	echo "[DEBUG] DUT failed count $udp_high"
	echo "[DEBUG] Golden sample failed count $udp_high_golden"
	if [ "$udp_high" == "0" ] && [ "$udp_high_golden" == "0" ] ; then
    	echo "UDP_packet_loss_high_rate: PASS" >> /root/automation/test_results.txt
	elif [ "$udp_high" != "0" ] && [ "$udp_high_golden" != "0" ]; then 
    	echo "UDP_packet_loss_high_rate: FAIL: <Both of DUT and Golden sample failed.>" >> /root/automation/test_results.txt
	elif [ "$udp_high" != "0" ] ; then
    	echo "UDP_packet_loss_high_rate: FAIL: <DUT failed.>" >> /root/automation/test_results.txt
	elif [ "$udp_high_golden" != "0" ] ; then 
    	echo "UDP_packet_loss_high_rate: FAIL: <Golden sample failed.>" >> /root/automation/test_results.txt
	fi
	sleep 1
}


function throughput_udp_low(){
	echo "[SENAO] iPerf Test with Packet loss start..." | tee -a /root/automation/log.txt
	echo "" | tee -a /root/automation/log.txt
	sshpass -p readwrite ssh -o ServerAliveInterval=60 -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_udp_low.sh" | tee -a /root/automation/log.txt | tee /tmp/log_tmp_golden.txt &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -u -l 64 -b 30 -T 25 -L 3 -r 1 -f | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt
	udp_low=$(grep -c "failed" /tmp/log_tmp.txt)
	udp_low_golden=$(grep -c "failed" /tmp/log_tmp_golden.txt)
	echo "[DEBUG] DUT failed count $udp_low"
	echo "[DEBUG] Golden sample failed count $udp_low_golden"
	if [ "$udp_low" == "0" ] && [ "$udp_low_golden" == "0" ]; then
    	echo "UDP_packet_loss_low_rate: PASS" >> /root/automation/test_results.txt
	elif [ "$udp_low" != "0" ] && [ "$udp_low_golden" != "0" ]; then 
    	echo "UDP_packet_loss_low_rate: FAIL: <Both of DUT and Golden sample failed.>" >> /root/automation/test_results.txt
	elif [ "$udp_low" != "0" ] ; then
    	echo "UDP_packet_loss_low_rate: FAIL: <DUT failed.>" >> /root/automation/test_results.txt
	elif [ "$udp_low_golden" != "0" ] ; then 
    	echo "UDP_packet_loss_low_rate: FAIL: <Golden sample failed.>" >> /root/automation/test_results.txt 
	fi
	sleep 1
}

echo "[SENAO] Setting DUT network configuration." | tee -a /root/automation/log.txt
/root/automation/T55_MFG/set_ip.sh
sleep 3

#is_etherphy_connection
#if [ $? -eq 1 ] ; then
#   	echo "NETWORK_TEST: FAIL: <RJ-45 disconnection>" >> /root/automation/test_results.txt
#	exit 1	
#fi	

is_ping
if [ $? -eq 1 ] ; then
   	echo "NETWORK_TEST: FAIL: <Network is not working.>" >> /root/automation/test_results.txt
	exit 1	
fi	

is_test_result_exist

is_done TCP_Throughput
if [ $? -eq 0 ] ; then
	throughput_tcp
fi


is_done UDP_packet_loss_high_rate
if [ $? -eq 0 ] ; then
	throughput_udp_high
fi


is_done UDP_packet_loss_low_rate
if [ $? -eq 0 ] ; then
	throughput_udp_low
fi


network_test_result
if [ "$ERROR" == "0" ]; then
   	echo "NETWORK_TEST: PASS" >> /root/automation/test_results.txt
else
   	echo "NETWORK_TEST: FAIL" >> /root/automation/test_results.txt
fi
