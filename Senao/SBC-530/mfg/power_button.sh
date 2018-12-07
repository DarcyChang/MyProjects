#!/bin/bash

Power_res="/tmp/power_button"
TIME=0.5

function detect_btn()
{
    while [ 1 ]; do
	state=$(cat $Power_res 2> /dev/null)
	if [ "$state" == "1" ] ;then
	    echo ""
	    echo "Power button is press"
	    rm -rf $Power_res
	    killall power_button.sh
	    state=0
	    echo 0 > $Power_res
	fi	
	sleep $TIME
    done
}

rm -rf $Power_res
sleep $TIME

detect_btn &
