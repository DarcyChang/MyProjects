#!/bin/bash

if [ -z "$1" ]; then
    echo "usage $0 <speed>"
    exit
fi

if [ "$1" != "10" ] && [ "$1" != "100" ] && [ "$1" != "1000" ]; then
    echo "only support speed 10, 100, 1000"
    exit
fi

SPEED=$1

if_list=$(ifconfig | grep eth | cut -d' ' -f1)

for IF in $if_list; do
    ethtool -s $IF autoneg off speed $SPEED duplex full
done
