#!/bin/bash

model=$(pwd | cut -d/ -f 3)
case $model in
ENA-1011)
    loopback_list="po1:po5,po2:po6,po3:po7,po4:po8,po9:po10"
    ;;
ENA-1200)
    loopback_list="eth0:eth1,eth2:eth3"
    ;;
ENA-3010)
    loopback_list="eth0:eth1,eth2:eth3,eth4:eth5,eth6:eth7"
    ;;
SBC-530)
    loopback_list="eth0:eth1"
    ;;
SBC-1100)
    loopback_list="eth0:eth1"
    ;;
esac
iperf_arg="-w 512k"
parallel=2

function get_iface_link {
    get_iface_link_ret=$(ethtool $1 | grep -c 'Link detected: yes')
}

function wait_iface_link_up {
    local timeout=$2
    while (( timeout > 0 ));
    do
        get_iface_link $1
        if [ "$get_iface_link_ret" != "0" ]; then
            wait_iface_link_up_ret=1
            return
        fi
        sleep 1
        timeout=$(( timeout - 1 ))
    done
    wait_iface_link_up_ret=0
}

while [[ $# > 0 ]]
do
    key="$1"
    case $key in
    --iperf_arg)
    iperf_arg="$2"
    shift
    ;;
    -l)
    loopback_list="$2"
    shift
    ;;
    -P)
    parallel="$2"
    shift
    ;;
    -t)
    time="$2"
    shift
    ;;
    -T)
    rate_criteria="$2"
    shift
    ;;
    -d)
    direction="$2"
    shift
    ;;
    -m)
    mtu="$2"
    shift
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
    esac
    shift # past argument or value
done

if [ -z "$time" ]; then
    read -p "Enter runtime: " time
fi

day=$(echo $time | grep -o -e '[0-9]\+[Dd]' | sed -n 's/[Dd]*//gp')
[ -z "$day" ] && day=0
hour=$(echo $time | grep -o -e '[0-9]\+[Hh]' | sed -n 's/[Hh]*//gp')
[ -z "$hour" ] && hour=0
min=$(echo $time | grep -o -e '[0-9]\+[Mm]' | sed -n 's/[Mm]*//gp')
[ -z "$min" ] && min=0
sec=$(echo $time | grep -o -e '[0-9]\+[Ss]\|^[0-9]\+$' | sed -n 's/[Ss]*//gp')
[ -z "$sec" ] && sec=0
time=$(echo "( $day * 3600 * 24 ) + ( $hour * 3600 ) + ( $min * 60 ) + $sec " | bc)

service network-manager stop 2> /dev/null
iptables --flush -t nat

if [ ! -z "$(echo $loopback_list | grep ,)" ]; then
    loopback_list=$(echo $loopback_list | sed -n 's/,/ /gp')
fi

iperf_count=0
for pair in $loopback_list;
do
    iface1=$(echo $pair | cut -d: -f1)
    id1=$(grep -n "${iface1}:" /proc/net/dev | awk -F':' '{print $1}')
    iface2=$(echo $pair | cut -d: -f2)
    id2=$(grep -n "${iface2}:" /proc/net/dev | awk -F':' '{print $1}')
    for str in $iface1:$id1:$id2:tx $iface2:$id2:$id1:rx;
    do
        iface=$(echo $str | awk -F':' '{print $1}')
        if_idx=$(echo $str | awk -F':' '{print $2}')
        peer_idx=$(echo $str | awk -F':' '{print $3}')
        dir=$(echo $str | awk -F':' '{print $4}')
        if_ip=10.0.$if_idx.1
        snat_ip=10.1.$if_idx.1
        peer_ip=10.1.$peer_idx.1
        ifconfig $iface down
        ifconfig $iface hw ether 02:00:00:10:10:$if_idx
        if [ ! -z "$mtu" ]; then
            ifconfig $iface mtu $mtu
        fi
        ifconfig $iface $if_ip netmask 255.255.255.0 up
        iptables -t nat -A POSTROUTING -s $if_ip -d $peer_ip -j SNAT --to-source $snat_ip
        iptables -t nat -A PREROUTING -d $snat_ip -j DNAT --to-destination $if_ip
        route del $peer_ip 2> /dev/null
        ip route add $peer_ip dev $iface
        arp -i $iface -s $peer_ip 02:00:00:10:10:$peer_idx
        if [ -z "$direction" ] || [ "$direction" == "$dir" ]; then
            iperf_dest_ip[iperf_count]=$peer_ip
            iperf_iface[iperf_count]=$iface
            iperf_count=$(( iperf_count + 1 ))
        fi
    done
done

sleep 1
for iface in $(echo $loopback_list | sed -n 's/[:,]/ /gp');
do
    wait_iface_link_up $iface 10
    if [ "$wait_iface_link_up_ret" != "1" ]; then
        echo "$iface is not link up"
        exit 1
    fi
done

trap 'killall -9 iperf; echo "Test is stopped by user"; exit 0' SIGINT

killall iperf 2> /dev/null

iperf -s -D -w 512k
iperf -s -D -u -w 512k

rm /tmp/*.iperf_res 2> /dev/null
for (( i = 0; i < iperf_count; i++ ));
do
    iperf -c ${iperf_dest_ip[$i]} $iperf_arg -P $parallel -t $time > /tmp/$i.iperf_res &
done

echo "-------------------------------------------------------"

iperf_running=1
timeout=$(( time + 10 ))
while [ "$iperf_running" != "0" ]
do
    if (( timeout == 0 )); then
        pid_list=$(ps aux | grep 'iperf -c' | grep -v grep | awk '{printf $2" "}')
        for pid in $pid_list;
        do
            kill $pid
        done
        echo error: connection timeout
        break
    fi
    sleep 1
    iperf_running=$(ps aux | grep 'iperf -c' | grep -vc grep)
    timeout=$(( timeout - 1 ))
done

for (( i = 0; i < iperf_count ; i++ ));
do
    is_tcp=$(grep Client /tmp/$i.iperf_res | grep -c TCP)
    if [ "$is_tcp" == "1" ]; then
        if (( parallel > 1 )); then
            number=$(grep SUM /tmp/$i.iperf_res | awk '{print $(NF-1)}')
            unit=$(grep SUM /tmp/$i.iperf_res | awk '{print $NF}')
        else
            number=$(grep '/sec' /tmp/$i.iperf_res | awk '{print $(NF-1)}')
            unit=$(grep '/sec' /tmp/$i.iperf_res | awk '{print $NF}')
        fi
        if [ -n "$(echo $unit | grep Gbits)" ]; then
            rate[i]=$(echo "$number * 1000" | bc)
        elif [ -n "$(echo $unit | grep Kbits)" ]; then
            rate[i]=$(echo "scale=3; $number / 1000" | bc)
        else
            rate[i]=$number
        fi
    else
        speed_list=$(grep % /tmp/0.iperf_res | awk '{for(i=1;i<=NF;i++)if(match($i,"/sec")){print $(i-1)":"$i}}')
        rate[i]=0
        for speed in $speed_list
        do
            number=$(echo $speed | cut -d: -f1)
            unit=$(echo $speed | cut -d: -f2)
            if [ -n "$(echo $unit | grep Gbits)" ]; then
                rate[i]=$(echo "$number * 1000 + ${rate[$i]}" | bc)
            elif [ -n "$(echo $unit | grep Kbits)" ]; then
                rate[i]=$(echo "scale=3; $number / 1000 + ${rate[$i]}" | bc)
            else
                rate[i]=$(echo "$number + ${rate[$i]}" | bc)
            fi
        done
    fi
done

total_rate=0
if [ -n "$rate_criteria" ]; then
    result="[PASS]"
fi
for (( i = 0; i < iperf_count; i++ ))
do
    if [ -n "$rate_criteria" ]; then
        if [ "$(echo "${rate[$i]} < $rate_criteria" | bc)" == "1" ]; then
            result="[FAIL]"
        else
            result="[PASS]"
        fi
    fi
    echo ${iperf_iface[$i]} Throughput: ${rate[$i]} Mbps $result
    total_rate=$(echo "$total_rate + ${rate[$i]}" | bc)
done

echo Total Throughput: $total_rate Mbps

