#!/bin/bash

time=0
udp=0
len=1472
bandwidth=1000
gold_sample=0
no_test=0
daemon=0
force=0
v_loop=0
throughput_min=0
loss_rate_max=100
max_retries=0
determine_result=0
eid_list=""
shift_poe=0
tcp_arg="-P 5"


while [[ $# > 0 ]]
do
key="$1"
case $key in
    -a)
    tcp_arg="$2"
    shift
    ;;
    -g)
    gold_sample=1
    ;;
    -u)
    udp=1
    ;;
    -t)
    time="$2"
    shift
    ;;
    -l)
    len="$2"
    shift
    ;;
    -D)
    daemon=1
    ;;
    -n)
    no_test=1
    ;;
    -b)
    bandwidth="$2"
    shift
    ;;
    -f)
    force=1
    ;;
    -e)
    eid_list="$2"
    shift
    ;;
    -r)
    max_retries="$2"
    shift
    ;;
    -T)
    throughput_min="$2"
    shift
    ;;
    -L)
    loss_rate_max="$2"
    shift
    ;;
    -s)
    shift_poe=1
    ;;
    -V)
    v_loop=1
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
esac
shift
done

for (( i = 0; i < 10; i ++)); do
    Driver_Path="/proc/driver/igb/0000:0$i:00.0/test_mode"
    if [ -f "$Driver_Path" ]; then
	break  
    fi
done

eth_net=(0 1 2 3 4)

if [ "$gold_sample" == "0" ]; then
    my_id=1
    ur_id=2
    dev_role=DUT
else
    my_id=2
    ur_id=1
    dev_role=GS
fi

if [ "$udp" == "1" ]; then
    if [ "$throughput_min" != "0" ] || [ "$loss_rate_max" != "100" ]; then
        determine_result=1
    fi
else
    if [ "$throughput_min" != "0" ]; then
        determine_result=1
    fi
fi

if [ "$time" == "0" ]; then
    if [ "$daemon" == "1" ]; then
        time=999999
    else
        time=10
    fi
fi

# T55 has 5 vlan port
if [ $v_loop == "1" ]; then
    eid_list="0"
else
    eid_list="0.3 0.4 0.5 0.6 0.7"
fi

modprobe -r igb; modprobe igb
if [ $v_loop == "1" ]; then 
    echo "vloop" > $Driver_Path
else
    echo "v1q" > $Driver_Path
fi
sleep 1

if [ $v_loop == "1" ]; then
    for eid in $eid_list; do
	mac=`expr $eid + 1`
	ifconfig eth$eid down
	ifconfig eth$eid hw ether 02:0$my_id:00:00:00:$mac
	ifconfig eth$eid 192.168.${eth_net[$eid]}.$my_id netmask 255.255.255.0
	ethtool -G eth$eid tx 4096
	ethtool -G eth$eid rx 4096
	ifconfig eth$eid up
    done
else
    ifconfig eth0 up
    for eid in $eid_list; do
    	vid=`echo $eid | cut -d. -f2`
    	mac=`expr $vid + 2`
    	vconfig add eth0 $vid &> /dev/null
    	ifconfig eth$eid down
    	ifconfig eth$eid hw ether 02:0$my_id:00:00:00:$mac
    	vid=`expr $vid - 3`
    	ifconfig eth$eid 192.168.${eth_net[$vid]}.$my_id netmask 255.255.255.0
    	ifconfig eth$eid up
    done
fi

killall -9 iperf &> /dev/null
iperf -s -w 512k -l 64k -D &> /dev/null
iperf -s -u -D &> /dev/null

if [ "$no_test" == "1" ]; then
    echo "done"
    exit 0
fi

link_state="no"
wait_link=10
while [ "$wait_link" -gt "0" ] && [ "$link_state" != "yes" ]
do
    link_state=`ethtool eth0 | grep 'Link detected' | awk '{print $3}'`
    echo "[$wait_link] waiting link up for eth0..." && sleep 1
    wait_link=`expr $wait_link - 1`
done 

if [ $wait_link -le "0" ]; then
    echo "please check eth0"
    exit 0
fi

if [ "$force" == "0" ]; then
    read -p "Please Enter to Run..." ps
fi

echo "ffdb" >$Driver_Path 

for eid in $eid_list; do
    net=`ifconfig eth$eid | grep 'inet addr' | awk '{ print $2 }' | cut -d. -f3`
    peer_ip=192.168.$net.$ur_id
    res_file=/tmp/iperf_res_eth$eid
    run=1
    retries=0
    if [ "$udp" == "1" ]; then
        echo "[$dev_role] Start testing UDP on eth$eid..."
        command="iperf -c $peer_ip -u -b ${bandwidth}M -l $len -t $time"
        if [ "$daemon" == "1" ]; then
            rm -f $res_file
            $command &> $res_file &
        else
            while [ "$run" == "1" ]
            do
                $command &> $res_file
                res_str=`grep '%' $res_file`
                result="pass"
                if [ "$res_str" == "" ]; then
                    msg="No response from peer $peer_ip\n"
                    result="failed"
                else
                    word=`echo $res_str | awk '{print $4}'`
                    if [ "$word" == "sec" ]; then
                        thrput=`echo $res_str | awk '{print $7}'`
                        unit=`echo $res_str | awk '{print $8}'`
                        loss_rate=`echo $res_str | awk '{print $12}' | sed 's/[(%)]//g'`
                    else
                        thrput=`echo $res_str | awk '{print $8}'`
                        unit=`echo $res_str | awk '{print $9}'`
                        loss_rate=`echo $res_str | awk '{print $13}' | sed 's/[(%)]//g'`
                    fi
                    thrput_pass=`echo "$throughput_min <= $thrput" | bc`
                    unit_is_mbit=`echo $unit | grep -c Mbits`
                    loss_rate_pass=`echo "$loss_rate < $loss_rate_max" | bc`
                    if [ "$thrput_pass" == "0" ] ; then
						err_msg="[ERROR] eth$eid UDP Throughput too low."
                        result="failed"
					elif [ "$unit_is_mbit" == "0" ] ; then 
						err_msg="[ERROR] eth$eid UDP Unit error."
                        result="failed"
					elif [ "$loss_rate_pass" == "0" ] ; then
						err_msg="[ERROR] eth$eid UDP loss rate too high."
                        result="failed"
                    fi
:<<SKIP
                    if [ "$thrput_pass" == "0" ] || [ "$unit_is_mbit" == "0" ] || [ "$loss_rate_pass" == "0" ]; then
                        result="failed"
                    fi
SKIP
                    msg="Throughput: $thrput $unit\nLoss Rate:  ($loss_rate%%)\n"
                fi
                if [ "$determine_result" == "0" ] || [ "$result" == "pass" ] || [ "$retries" -ge "$max_retries" ]; then
                    run=0
                    printf "$msg"
                    [ "$determine_result" == "1" ] && echo "Result:     [$result] [$retries]"
                else
                    retries=`expr $retries + 1`
                    sleep 1
                fi
            done
            rm -f $res_file
			if [ $result == "failed" ] ; then
				echo $err_msg >> /root/automation/testresults-failure.txt
			fi
        fi
    else
        echo "[$dev_role] Start testing TCP on eth$eid..."
        command="iperf -c $peer_ip -t $time $tcp_arg"
        if [ "$daemon" == "1" ]; then
            rm -f $res_file
            $command &> $res_file &
        else
            while [ "$run" == "1" ]
            do
                $command &> $res_file
                res_str=`grep 'SUM' $res_file`
                [ "$res_str" == "" ] && res_str=`grep '/sec' $res_file | tail -1`
                result="pass"
                if [ "$res_str" == "" ]; then
                    run=0
                    echo "No response from peer $peer_ip"
                    [ "$determine_result" == "1" ] && echo "Result:     [failed]"
                else
                    word=`echo $res_str | awk '{print $4}'`
                    if [ "$word" == "sec" ]; then
                        thrput=`echo $res_str | awk '{print $7}'`
                        unit=`echo $res_str | awk '{print $8}'`
                    else
                        thrput=`echo $res_str | awk '{print $6}'`
                        unit=`echo $res_str | awk '{print $7}'`
                    fi
                    thrput_pass=`echo "$throughput_min <= $thrput" | bc`
                    unit_is_mbit=`echo $unit | grep -c Mbits`
                    rx_errors=`ifconfig eth$phy_eid | grep 'RX packets' | awk '{print $3}' | cut -d: -f2`
                    tx_errors=`ifconfig eth$phy_eid | grep 'TX packets' | awk '{print $3}' | cut -d: -f2`
                    if [ "$thrput_pass" == "0" ] ; then
						err_msg="[ERROR] eth$eid TCP Throughput too low."
                        result="failed"
					elif [ "$unit_is_mbit" == "0" ] ; then
						err_msg="[ERROR] eth$eid TCP Unit error."
                        result="failed"
					elif [ "$rx_errors" != "0" ] ; then
						err_msg="[ERROR] eth$eid TCP RX error."
                        result="failed"
					elif [ "$tx_errors" != "0" ] ; then
						err_msg="[ERROR] eth$eid TCP TX error."
                        result="failed"
                    fi
:<<SKIP
                    if [ "$thrput_pass" == "0" ] || [ "$unit_is_mbit" == "0" ] || [ "$rx_errors" != "0" ] || [ "$tx_errors" != "0" ]; then
                        result="failed"
                    fi
SKIP
                    if [ "$determine_result" == "0" ] || [ "$result" == "pass" ] || [ "$retries" -ge "$max_retries" ]; then
                        run=0
                        echo "Throughput:  $thrput $unit"
                        echo "Rx/Tx Error: $rx_errors/$tx_errors"
                        if [ "$rx_errors" != "0" ] || [ "$tx_errors" != "0" ]; then
                            ethtool -S eth$phy_eid | grep errors | grep -v 'errors: 0'
                        fi
                        [ "$determine_result" == "1" ] && echo "Result:      [$result] [$retries]"
                    else
                        retries=`expr $retries + 1`
                        sleep 1
                    fi
                fi
                rm -f $res_file
            done
			if [ $result == "failed" ] ; then
				echo $err_msg >> /root/automation/testresults-failure.txt
			fi
        fi
    fi
done
