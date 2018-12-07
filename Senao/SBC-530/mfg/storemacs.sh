#!/bin/bash

if [ -z "$2" ]; then
    echo "uasge: $0 <ethx> <mac>"
    exit
fi

IF=$1
MAC=$2

ifconfig $IF hw ether $MAC 2> /dev/null
if [ "$?" != "0" ]; then
    echo "Invalid MAC Address"
    exit
fi
if [ "$IF" == "eth0" ]; then
    echo mac $MAC > /proc/driver/igb/0000\:01\:00.0/test_mode
elif [ "$IF" == "eth1" ]; then
    echo mac $MAC > /proc/driver/igb/0000\:02\:00.0/test_mode
fi
rmmod igb
modprobe igb mfg_mac=0

IF_list=$(ifconfig -a | grep eth | awk '{print $1}')
for IF1 in $IF_list; do
    ifconfig $IF1 up
done

