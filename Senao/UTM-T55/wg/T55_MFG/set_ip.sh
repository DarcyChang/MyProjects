#!/bin/bash

gold_sample=0

while [[ $# > 0 ]]
do
key="$1"
case $key in
    -g)
    gold_sample=1
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
esac
shift
done

if [ "$gold_sample" == "0" ]; then
	ifconfig eth0 192.168.0.1
	ifconfig eth1 192.168.1.1
	ifconfig eth2 192.168.2.1
	ifconfig eth3 192.168.3.1
	ifconfig eth4 192.168.4.1
else
	ifconfig eth0 192.168.0.2
	ifconfig eth1 192.168.1.2
	ifconfig eth2 192.168.2.2
	ifconfig eth3 192.168.3.2
	ifconfig eth4 192.168.4.2
fi
