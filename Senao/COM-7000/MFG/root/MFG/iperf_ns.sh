#!/bin/bash
# Author Darcy_Chang<Darcy.Chang@senao.com>
# Date 2020/05/21
# version 1.0

Error=0
DefaultEtherA=eth0
DefaultEtherB=eth1
seconds=10

#input 2 ethernet interface to do namespace iperf test between them.
function iperf_ns()
{
    echo "Iperf test for dev <$1> and <$2>"
#    echo "[DEBUG] $1 $2 $3 $4 $5"
    ip netns add ns_server_$1
    ip netns add ns_client_$2
    ip link set $1 netns ns_server_$1
    ip link set $2 netns ns_client_$2
    ip netns exec ns_server_$1 ip addr add dev $1 10.0.0.1/24
    ip netns exec ns_server_$1 ip link set dev $1 up
    ip netns exec ns_client_$2 ip addr add dev $2 10.0.0.2/24
    ip netns exec ns_client_$2 ip link set dev $2 up
    
#    killall iperf >/dev/null  2>&1
    #run iperf
    ip netns exec ns_server_$1 iperf -s -D -w 512k >/dev/null 2>&1
    ip netns exec ns_client_$2 iperf -c 10.0.0.1 -d -t $3 > /tmp/throughput_$1_$2
    
    #remove ns interface and delete namespace
    ip netns exec ns_server_$1 ip link set $1 netns 1
    ip netns exec ns_client_$2 ip link set $2 netns 1
    
    ip netns del ns_server_$1
    ip netns del ns_client_$2
#    killall iperf >/dev/null  2>&1
	echo "1" >> /tmp/throughput_done
}

#Check requested devices or use default devices

if [ -z "$1" ] && [ -z "$2" ] ;then
	ethA=$DefaultEtherA
	ethB=$DefaultEtherB
else
    ethA=$(grep $1: /proc/net/dev | awk -F':' '{ print $1 }')
    ethB=$(grep $2: /proc/net/dev | awk -F':' '{ print $1 }')

    if [ -z "$ethA" ] || [ -z "$ethB" ];then

        if [ -z "$ethA" ];then
            echo "Invalid devices: [$1] "
        fi
        if [ -z "$ethB" ];then
            echo "Invalid devices: [$2] "
        fi
        exit 1
    fi

fi

if [ -n "$3" ] ;then
	seconds=$3
fi

FIBER_LIST=$(lshw -quiet -C network |grep i40e -B 8|grep 'logical'|awk '{ print $3 }')
COPPER_LIST=$(lshw -quiet -C network |grep " tp " -B 8|grep 'logical name'|awk '{ print $3 }')


link_state_A=$(ethtool $ethA | grep 'Link detected' | awk '{print $3}')
link_speed_A=$(ethtool $ethA | grep 'Speed'|awk '{ print $2 }')

link_state_B=$(ethtool $ethB | grep 'Link detected' | awk '{print $3}')
link_speed_B=$(ethtool $ethB | grep 'Speed'|awk '{ print $2 }')

printf "%-14s" "Copper Ports: " 
echo ${COPPER_LIST[*]}

printf "%-14s" "Fiber Ports: "
echo ${FIBER_LIST[*]}

printf "%-7s LinkStatus:[%3s]\tLinkSpeed:[%10s]\n" $ethA $link_state_A $link_speed_A
printf "%-7s LinkStatus:[%3s]\tLinkSpeed:[%10s]\n" $ethB $link_state_B $link_speed_B

#Check LinkStatus
if [ $link_state_A != "yes" ]; then
    printf "[%7s] Port [%7s]\tLinkStatus[%3s]\n" "ERROR" $ethA $link_state_A
    Error=1
fi
if [ $link_state_B != "yes" ]; then
    printf "[%7s] Port [%7s]\tLinkStatus[%3s]\n" "ERROR" $ethB $link_state_B
    Error=1
fi

if [ $Error -eq 1 ];then
echo "Correct the error before proceeding."
exit 1
fi

#ip_1=$(echo "$ethA" | awk -F "eth" '{print $2}')
#ip_2=$(echo "$ethB" | awk -F "eth" '{print $2}')
#echo "[DEBUG] $ip_1 and $ip_2"

#iperf_ns $ethA $ethB $seconds $ip_1 $ip_2
iperf_ns $ethA $ethB $seconds

