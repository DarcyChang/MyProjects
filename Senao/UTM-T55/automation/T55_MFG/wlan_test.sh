#!/bin/bash

gold_sample=0
UDP=0
TCP=0
time=11
SSID=T55_mfg
MHz=5G

if [ $# -lt 2 ]; then
    echo "usage: ./wlan_test.sh [-g] -S <num 0-9>"
    echo "       ./wlan_test.sh -u    -> UDP"
    echo "       ./wlan_test.sh -t    -> TCP"
    echo "       ./wlan_test.sh -M <2G/5G>"
    exit 1
fi 

while [[ $# > 0 ]]
do
key="$1"
case $key in
    -g)
    gold_sample=1
    ;;
    -S)
    Board_num="$2"
    echo -n "Board num:$Board_num, "
    shift
    ;;
    -M)
    MHz="$2"
    echo "${MHz} MHz"
    shift
    ;;
    -u)
    UDP=1
    ;;
    -t)
    TCP=1
    ;;
    -T)
    time="$2"
    shift
    ;;
    *)
    echo "unknown option '$key'"
    ;;
esac
shift
done

if [ "$TCP" == "0" ] && [ "$UDP" == "0" ]; then
    echo "Please add -t or -u to choice TCP or UDP"
    exit 1	
fi

if [ -z "$Board_num" ]; then
    echo "Please add -S <num 0-9> to identify board"
fi

#change 2G/5G setting
cp /etc/hostapd/hostapd_${MHz}.conf /etc/hostapd/hostapd.conf
echo "ssid=T55_mfg${Board_num}" >> /etc/hostapd/hostapd.conf

if [ "$gold_sample" == 0 ]; then
    my_id=1
    ur_id=2
else
    my_id=2
    ur_id=1
fi

ifconfig eth0 down
service network-manager stop
sleep 1
ifconfig wlan0 192.168.$Board_num.$my_id
ifconfig wlan0 down
ifconfig wlan0 hw ether 00:11:22:33:${Board_num}0:0$my_id
if [ "$gold_sample" == 0 ]; then
    ifconfig wlan0 up
    service hostapd stop
    echo "Station Mode Ready"
else
#   change SSID in config file
    ifconfig wlan0 up
#   master mode detect
    Base=$(echo $MHz | cut -c 1)   #2 or 5
    AP_detect=""
    while [ -z "$AP_detect" ] || [ "$AP_detect" != "$Base" ]
    do
        AP_detect=$(iw wlan0 info | grep channel | awk '{print $3}' | cut -c 2)
	service hostapd stop
	sleep 3
        service hostapd start
        sleep 3
    done
    echo "AP Mode Ready"
fi
killall -9 iperf &> /dev/null
iperf -s -w 512k -l 64k > /tmp/iperf_res_TCP1 &
iperf -s -u > /tmp/iperf_res_UDP1 & 


read -p "Press Enter to Connect" ps

if [ "$gold_sample" == 0  ]; then
    echo "connect to AP"
else 
    echo "wait station connect"
fi
 
check_connect=""
while [ -z "$check_connect" ]
do
    if [ "$gold_sample" == 0  ]; then
        iwconfig wlan0 essid $SSID$Board_num
    fi
    check_connect=$(cat /sys/kernel/debug/ieee80211/phy0/ath10k/fw_stats | grep "00:11:22:33:${Board_num}0:0$ur_id" )
    if [ -n "check_connect" ]; then
        echo -n ""
    else
  	echo "connect ok"
    fi
    sleep 1
done
 
peer_ip=192.168.$Board_num.$ur_id

read -p "Press Enter to Run..." ps

finish_time=$(expr $time + 10)
res_str1=""
res_str2=""
wait_time=0

if [ "$TCP" == 1 ]; then
    iperf -c $peer_ip -P 50 -t $time > /tmp/iperf_res_TCP2 2>&1 & 

    while [ -z "$res_str1" ] || [ -z "$res_str2" ]
    do
        res_str1=$(grep 'SUM' /tmp/iperf_res_TCP1)
        res_str2=$(grep 'SUM' /tmp/iperf_res_TCP2) 
   	sleep 1
        wait_time=$(expr $wait_time + 1)
 	if [ $wait_time -gt $finish_time ]; then
 	    echo Time out, failed.
	    exit 1
	fi
    done

    TCP_RX=$(echo $res_str1 | awk '{print $6}')
    TCP_TX=$(echo $res_str2 | awk '{print $6}')
    RX_unit=$(echo $res_str1 | awk '{print $7}')
    TX_unit=$(echo $res_str2 | awk '{print $7}')
    
    echo RX: $TCP_RX $RX_unit
    echo TX: $TCP_TX $TX_unit
elif [ "$UDP" == 1 ]; then
    iperf -c $peer_ip -u -b 1500M -t $time > /tmp/iperf_res_UDP2 2>&1 &

    while [ -z "$res_str1" ] || [ -z "$res_str2" ]
    do
        res_str1=$(grep '%' /tmp/iperf_res_UDP1)
        res_str2=$(grep '%' /tmp/iperf_res_UDP2)
        sleep 1
        wait_time=$(expr $wait_time + 1)
        if [ $wait_time -gt $finish_time ]; then
            echo Time out, failed.
            exit 1
        fi
    done

    UDP_RX=$(echo $res_str1 | awk '{print $7}')
    UDP_TX=$(echo $res_str2 | awk '{print $7}')
    RX_unit=$(echo $res_str1 | awk '{print $8}')
    TX_unit=$(echo $res_str2 | awk '{print $8}')

    echo RX: $UDP_RX $RX_unit
    echo TX: $UDP_TX $TX_unit
fi

rx_errors=$(ifconfig wlan0 | grep 'RX packets' | awk '{print $3}' | cut -d: -f2)
tx_errors=$(ifconfig wlan0 | grep 'TX packets' | awk '{print $3}' | cut -d: -f2)
echo "Rx/Tx Error: $rx_errors/$tx_errors"



if [ "$TCP" == "1" ]; then
    TX_PASS=$(echo "100 <= $TCP_TX" | bc)
    RX_PASS=$(echo "100 <= $TCP_RX" | bc)
elif [ "$UDP" == "1" ]; then
    TX_PASS=$(echo "200 <= $UDP_TX" | bc)
    RX_PASS=$(echo "200 <= $UDP_RX" | bc)
fi

if [ "$TX_PASS" == "1" ] && [ "$RX_PASS" == "1" ] && [ "$rx_errors" -lt 3 ] && [ "$tx_errors" -lt 3 ]; then
    echo "[PASS]"
else
    echo "[FAIL]"
fi


if [ "$gold_sample" == "0" ]; then 
     iwconfig wlan0 essid test_done
     ifconfig wlan0 down
     sleep 1
     ifconfig wlan0 hw ether 00:00:00:00:00:10
     ifconfig wlan0 up
fi
