#!/bin/bash

function blink()
{
    while [ 1 ]; do
        echo 0 > $GPIO_DATA_PATH
        sleep $DELAY
        echo 0xff > $GPIO_DATA_PATH
        sleep $DELAY
    done
}

GPIO_DIR_PATH=$(find /sys/devices/ -name "io4")
GPIO_DATA_PATH=$(find /sys/devices/ -name "data4")

if [ -z $GPIO_DIR_PATH ] || [ -z $GPIO_DATA_PATH ]; then
    echo "nct driver not support gpio"
    exit 
fi

ROUND=20
DELAY=0.5
#LED_DATA="1 2 4 8 16 32 64 128 0"

#init 
echo 0xff > $GPIO_DIR_PATH
sleep 0.5

#change direction 
echo 0 > $GPIO_DIR_PATH

blink &

read -p "press enter to stop" ps
echo 0 > $GPIO_DATA_PATH
disown $!
kill $!
