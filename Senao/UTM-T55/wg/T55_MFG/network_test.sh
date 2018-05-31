#! /bin/bash

source /root/automation/Library/path.sh

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
	link_error=0 # connection
	port_num=$(ifconfig -a | grep eth | wc -l)
	echo "[SENAO] Detecting DUT $port_num ports link status." | tee -a $log_path
	for ((eid=0; eid<$port_num; eid++))
	do
		link_state=$(ethtool eth$eid | grep 'Link detected' | awk '{print $3}')
		if [ $link_state != "yes" ] ; then
			echo "[WARNING] DUT port eth$eid link status $link_state" | tee -a $log_path | tee -a $test_result_failure_path 
			link_error=1 # disconnection
		fi		
	done

	echo "[SENAO] Detecting Golden sample $port_num ports link status." | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/golden_networking.sh" | tee $tmp_golden_path
	golden_link_state=$(grep -c "no" $tmp_golden_path)
	if [ $golden_link_state -gt 0 ] ; then
		cat $tmp_golden_path | tee -a $log_path | tee -a $test_result_failure_path
		link_error=1 # disconnection
	fi

	return $link_error
}


function is_ping(){
	port_num=$(ifconfig -a | grep eth | wc -l)
	for ((eid=0; eid<$port_num; eid++))
	do
		echo "[DEBUG] ping 192.168.$eid.2"
		ping_working=$(ping -c5 192.168.$eid.2 |grep transmitted |awk '{print $4}')
		if [ $ping_working -eq 0 ] ; then
			echo "[ERROR] 192.168.$eid.1 ping 192.168.$eid.2 is not working." | tee -a $log_path | tee -a $test_result_failure_path
			return 1
		fi
	done
	return 0
}


function throughput_tcp(){
	echo "[SENAO] iPerf Test with Throughput start..." | tee -a $log_path
	echo "" | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_tcp.sh" | tee -a $log_path | tee $tmp_golden_path &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -T 900 -f | tee -a $log_path | tee $tmp_path
	tcp=$(grep -c "failed" $tmp_path)
	tcp_golden=$(grep -c "failed" $tmp_golden_path)
	echo "[DEBUG] DUT failed count $tcp"
	echo "[DEBUG] Golden sample failed count $tcp_golden"
	if [ "$tcp" == "0" ] && [ "$tcp_golden" == "0" ]; then
	    echo "TCP_Throughput: PASS" >> $test_result_path
	elif [ "$tcp" != "0" ] && [ "$tcp_golden" != "0" ]; then 
    	echo "TCP_Throughput: FAIL: <Both of DUT and Golden sample failed.>" >> $test_result_path
	elif [ "$tcp" != "0" ] ; then 
    	echo "TCP_Throughput: FAIL: <DUT failed.>" >> $test_result_path
	elif [ "$tcp_golden" != "0" ] ; then
    	echo "TCP_Throughput: FAIL: <Golden sample failed.>" >> $test_result_path
	fi
	sleep 1
}

function throughput_udp_high(){
	echo "[SENAO] iPerf Test with Packet loss start..." | tee -a $log_path
	echo "" | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_udp_high.sh" | tee -a $log_path | tee $tmp_golden_path &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -u -T 800 -L 3 -r 1 -f | tee -a $log_path | tee $tmp_path
	udp_high=$(grep -c "failed" $tmp_path)
	udp_high_golden=$(grep -c "failed" $tmp_golden_path)
	echo "[DEBUG] DUT failed count $udp_high"
	echo "[DEBUG] Golden sample failed count $udp_high_golden"
	if [ "$udp_high" == "0" ] && [ "$udp_high_golden" == "0" ] ; then
    	echo "UDP_packet_loss_high_rate: PASS" >> $test_result_path
	elif [ "$udp_high" != "0" ] && [ "$udp_high_golden" != "0" ]; then 
    	echo "UDP_packet_loss_high_rate: FAIL: <Both of DUT and Golden sample failed.>" >> $test_result_path
	elif [ "$udp_high" != "0" ] ; then
    	echo "UDP_packet_loss_high_rate: FAIL: <DUT failed.>" >> $test_result_path
	elif [ "$udp_high_golden" != "0" ] ; then 
    	echo "UDP_packet_loss_high_rate: FAIL: <Golden sample failed.>" >> $test_result_path
	fi
	sleep 1
}


function throughput_udp_low(){
	echo "[SENAO] iPerf Test with Packet loss start..." | tee -a $log_path
	echo "" | tee -a $log_path
	sshpass -p readwrite ssh -p 4118 root@192.168.1.2 "/root/automation/T55_MFG/network_test_golden_udp_low.sh" | tee -a $log_path | tee $tmp_golden_path &
	sleep 2
	/root/automation/T55_MFG/iperf_test.sh -u -l 64 -b 30 -T 25 -L 3 -r 1 -f | tee -a $log_path | tee $tmp_path
	udp_low=$(grep -c "failed" $tmp_path)
	udp_low_golden=$(grep -c "failed" $tmp_golden_path)
	echo "[DEBUG] DUT failed count $udp_low"
	echo "[DEBUG] Golden sample failed count $udp_low_golden"
	if [ "$udp_low" == "0" ] && [ "$udp_low_golden" == "0" ]; then
    	echo "UDP_packet_loss_low_rate: PASS" >> $test_result_path
	elif [ "$udp_low" != "0" ] && [ "$udp_low_golden" != "0" ]; then 
    	echo "UDP_packet_loss_low_rate: FAIL: <Both of DUT and Golden sample failed.>" >> $test_result_path
	elif [ "$udp_low" != "0" ] ; then
    	echo "UDP_packet_loss_low_rate: FAIL: <DUT failed.>" >> $test_result_path
	elif [ "$udp_low_golden" != "0" ] ; then 
    	echo "UDP_packet_loss_low_rate: FAIL: <Golden sample failed.>" >> $test_result_path
	fi
	sleep 1
}

echo "[SENAO] Setting DUT network configuration." | tee -a $log_path
/root/automation/T55_MFG/set_ip.sh
sleep 3

is_etherphy_connection
if [ $? -eq 1 ] ; then
   	echo "NETWORK_TEST: FAIL: <RJ-45 disconnection>" >> $test_result_path
	exit 1	
fi	

is_ping
if [ $? -eq 1 ] ; then
   	echo "NETWORK_TEST: FAIL: <Network is not working.>" >> $test_result_path
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
   	echo "NETWORK_TEST: PASS" >> $test_result_path
else
   	echo "NETWORK_TEST: FAIL" >> $test_result_path
fi
