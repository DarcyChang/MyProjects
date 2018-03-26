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
