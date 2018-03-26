#!/bin/bash

WLAN_DEV=$(ifconfig -a | grep UNSPEC | awk '{print $1}')
Country=US
MODE=11ACVHT80
ESSID=""
CHANNEL=149
NUM=1
MCS=9
REMOVE=0

service network-manager stop
LAN_DRIVER=$(find /proc/driver/igb/* -name test_mode)
echo vdef > $LAN_DRIVER

while [[ $# > 0 ]]
do
key="$1"
case $key in
    -ap)
    ID="ap"
    ;;
    -sta)
    ID="sta"
    ;;
    -2G)
    CHANNEL=6
    MODE=11NGHT40
    ;;
    -5G)
    CHANNEL=149
    MODE=11ACVHT80
    ;;
    -r)
    REMOVE=1
    ;;
    -M)
    MCS=$2
    shift
    ;;
    -n)
    NUM=$2
    shift
    ;;
    -c)
    CHANNEL=$2
    shift
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
esac
shift
done

ath0_detect=$(ifconfig -a | grep ath0)
br0_detect=$(ifconfig -a | grep br0)
if [ -n "$ath0_detect" ]; then
    wlanconfig ath0 destroy
    if [ -n "$br0_detect" ]; then
	ifconfig br0 down
	brctl delbr br0	
    fi
fi

if [ "$REMOVE" == "1" ]; then
        ifconfig $WLAN_DEV up
        exit 1
fi

if [ -e $NUM ]; then
	echo "enter -n <NUM>"
	exit 1
fi

ESSID="T55_MFG_$NUM"
myid=$NUM
urid=$(expr $NUM + 1)

if [ "$ID" == "ap" ]; then
	wlanconfig ath0 create wlandev $WLAN_DEV wlanmode ap wlanaddr 00:00:33:45:67:1$myid
	iwpriv $WLAN_DEV setCountry $Country
	iwpriv ath0 mode $MODE
	iwpriv ath0 wds 1
	iwpriv ath0 shortgi 1
	iwconfig ath0 essid $ESSID
	iwconfig ath0 channel $CHANNEL
elif [ "$ID" == "sta" ]; then
	wlanconfig ath0 create wlandev $WLAN_DEV wlanmode sta wlanaddr 00:00:33:45:67:2$urid 
	iwpriv ath0 wds 1
	iwpriv ath0 shortgi 1
	iwconfig ath0 essid $ESSID
else
	echo "please enter -ap or -sta"
	exit 1
fi

brctl addbr br0
brctl addif br0 ath0 eth0
if [[ "$ID" == "ap" ]]; then
    ifconfig br0 192.168.10.0$myid
else 
    ifconfig br0 192.168.10.0$urid
fi

ifconfig ath0 up
