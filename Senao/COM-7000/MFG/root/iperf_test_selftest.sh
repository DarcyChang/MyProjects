#!/bin/bash

time=0
udp=0
len=1472
bandwidth=1000
gold_sample=0
no_test=0
daemon=0
force=0
vlan=0
throughput_min=0
loss_rate_max=100
max_retries=0
determine_result=0
eid_list=""
shift_poe=0
tcp_arg="-P 5"
loopback_list="eth1:eth2,eth3:eth4"

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
    -v)
    vlan=1
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
    -x)
    test_speed="$2"
    test_speedf="$2f"
    shift
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
esac
shift
done

if [ "$gold_sample" == "0" ]; then
    my_id=1
    ur_id=2
    eth_net[0]=0
    eth_net[1]=1
    eth_net[2]=2
    eth_net[3]=3
    eth_net[4]=4
    eth_net[5]=5
    eth_net[6]=6
    eth_net[7]=7
    dev_role=DUT
else
    my_id=2
    ur_id=1
    eth_net[0]=0
    eth_net[1]=1
    eth_net[2]=2
    eth_net[3]=3
    if [ "$shift_poe" == "1" ]; then
        eth_net[4]=6
        eth_net[5]=7
        eth_net[6]=4
        eth_net[7]=5
    else
        eth_net[4]=4
        eth_net[5]=5
        eth_net[6]=6
        eth_net[7]=7
    fi
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

#eid_list="0 1 2 3"
eid_list="1 2 3 4"

network_manager_running=`service network-manager status | grep 'Active:' | grep running`
if [ "$network_manager_running" != "" ]; then
    eth4_ip=`ifconfig eth4 2> /dev/null | grep 'inet addr' | awk '{printf $2}' | cut -d: -f2`
    eth4_mask=`ifconfig eth4 2> /dev/null | grep 'inet addr' | awk '{printf $4}' | cut -d: -f2`
    eth5_ip=`ifconfig eth5 2> /dev/null | grep 'inet addr' | awk '{printf $2}' | cut -d: -f2`
    eth5_mask=`ifconfig eth5 2> /dev/null | grep 'inet addr' | awk '{printf $4}' | cut -d: -f2`    
    service network-manager stop
    if [ "$eth4_ip" != "" ]; then
        ifconfig eth4 $eth4_ip netmask $eth4_mask
    fi
    if [ "$eth5_ip" != "" ]; then
        ifconfig eth5 $eth5_ip netmask $eth5_mask
    fi
fi

#modprobe -r igb; modprobe igb

ethtool -s eth1 autoneg off speed $test_speed duplex full
ethtool -s eth2 autoneg off speed $test_speed duplex full
#echo "sset $test_speedf" >/proc/driver/igb/0000:04:00.0/test_mode
#echo "vloop" > /proc/driver/igb/0000\:04\:00.0/test_mode
phy_eid_list="1 2 3 4"
vlan_eid_list=""

service network-manager stop 2> /dev/null
iptables --flush -t nat

if [ ! -z "$(echo $loopback_list | grep ,)" ]; then
    loopback_list=$(echo $loopback_list | sed -n 's/,/ /gp')
fi

for pair in $loopback_list;
do
    iface1=$(echo $pair | cut -d: -f1)
    id1=$(grep -n "${iface1}:" /proc/net/dev | awk -F':' '{print $1}')
    iface2=$(echo $pair | cut -d: -f2)
    id2=$(grep -n "${iface2}:" /proc/net/dev | awk -F':' '{print $1}')
    for str in $iface1:$id1:$id2 $iface2:$id2:$id1;
    do
        iface=$(echo $str | awk -F':' '{print $1}')
        if_idx=$(echo $str | awk -F':' '{print $2}')
        peer_idx=$(echo $str | awk -F':' '{print $3}')
        if_ip=10.0.$if_idx.1
        snat_ip=10.1.$if_idx.1
        peer_ip=10.1.$peer_idx.1
        ifconfig $iface down
        ifconfig $iface hw ether 02:00:00:10:10:$if_idx
        ifconfig $iface $if_ip netmask 255.255.255.0 up
        iptables -t nat -A POSTROUTING -s $if_ip -d $peer_ip -j SNAT --to-source $snat_ip
        iptables -t nat -A PREROUTING -d $snat_ip -j DNAT --to-destination $if_ip
        route del $peer_ip 2> /dev/null
        ip route add $peer_ip dev $iface
        arp -i $iface -s $peer_ip 02:00:00:10:10:$peer_idx
        iperf_ip_list="${iperf_ip_list}${peer_ip} "
    done
done

if_count=0
stat_rate_count=0
for iface in $(echo $loopback_list | sed -n 's/[:,]/ /gp');
do
    if_name[if_count]=$iface
    if_rx_rate_sum[if_count]=0
    if_tx_rate_sum[if_count]=0
    if_rx_error[if_count]=$(cat /sys/class/net/$iface/statistics/rx_errors)
    if_tx_error[if_count]=$(cat /sys/class/net/$iface/statistics/tx_errors)
    if_no_link[if_count]=0
    if_count=$(( if_count + 1 ))
done

killall -9 iperf &> /dev/null
iperf -s -w 512k -l 64k -D &> /dev/null
iperf -s -u -D &> /dev/null

if [ "$no_test" == "1" ]; then
    echo "done"
    exit 0
fi

all_link_up=0
wait_link=10
while [ "$all_link_up" != "1" ] && [ "$wait_link" -gt "0" ]
do
    all_link_up=1
    down_eth_list=""
    for eid in $eid_list; do
        phy_eid=`echo $eid | cut -d. -f 1`
        link_state=`ethtool eth$phy_eid | grep 'Link detected' | awk '{print $3}'`
        if [ "$link_state" != "yes" ]; then
            all_link_up=0
            down_eth_list="$down_eth_list eth$eid"
        fi
    done
    if [ "$all_link_up" != "1" ]; then
        echo "[$wait_link] waiting link up for${down_eth_list}..." && sleep 1
        wait_link=`expr $wait_link - 1`
    fi
done

if [ "$force" == "0" ]; then
    read -p "Please Enter to Run..." ps
fi

#echo "ffdb" > /proc/driver/igb/0000\:04\:00.0/test_mode

for eid in $eid_list; do
    phy_eid=`echo $eid | cut -d. -f 1`
    net=`ifconfig eth$eid | grep 'inet addr' | awk '{ print $2 }' | cut -d. -f3`
	my_ip=`ifconfig eth$eid | grep 'inet addr' | awk '{ print $2 }' | cut -d. -f4`
	if [[ $net == "3" ]] ; then
		peer_ip=10.1.4.1
	elif [[ $net == "4" ]] ; then
	    peer_ip=10.1.3.1
	elif [[ $net == "5" ]] ; then
	    peer_ip=10.1.6.1
	elif [[ $net == "6" ]] ; then
	    peer_ip=10.1.5.1
	fi
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
                    if [ "$thrput_pass" == "0" ] || [ "$unit_is_mbit" == "0" ] || [ "$loss_rate_pass" == "0" ]; then
                        result="failed"
                    fi
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
                    if [ "$thrput_pass" == "0" ] || [ "$unit_is_mbit" == "0" ] || [ "$rx_errors" != "0" ] || [ "$tx_errors" != "0" ]; then
                        result="failed"
                    fi
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
        fi
    fi
done
