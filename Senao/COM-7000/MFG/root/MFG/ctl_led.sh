#!/bin/bash
# Author Darcy.Chang
# Date 2020.08.06
# Version 1.0.0

echo_led_on=ef
sys_led_on=df
bi_led_on=bf
eth_led_on=7f

echo_led_off=10
sys_led_off=20
bi_led_off=40
eth_led_off=80

stress_log_file=/root/MFG/logs/log.txt

function help()
{
	echo "" | tee -a #stress_log_file
	echo "./ctl_led.sh [echo|sys|bi|eth] [on|off]" | tee -a #stress_log_file
}


tmp=$(i2cget -y 0 0x21 0x03 | awk -F "x" '{print $2}' )
#echo "[DEBUG] tmp $tmp $((16#$tmp))"

if [ $# -eq 2 ];then
	case $1 in
		"echo")
			if [[ "$2" == "on" ]] ;then
				value=$(( $((16#$tmp)) & $((16#$echo_led_on)) ))
			elif [[ "$2" == "off" ]] ;then
				value=$(( $((16#$tmp)) | $((16#$echo_led_off)) ))
			else
				help
				exit 1
			fi
			;;
		"sys")
			if [[ "$2" == "on" ]] ;then
				value=$(( $((16#$tmp)) & $((16#$sys_led_on)) ))
			elif [[ "$2" == "off" ]] ;then
				value=$(( $((16#$tmp)) | $((16#$sys_led_off)) ))
			else
				help
				exit 1
			fi
			;;
		"bi")
			if [[ "$2" == "on" ]] ;then
				value=$(( $((16#$tmp)) & $((16#$bi_led_on)) ))
			elif [[ "$2" == "off" ]] ;then
				value=$(( $((16#$tmp)) | $((16#$bi_led_off)) ))
			else
				help
				exit 1
			fi
			;;
		"eth")
			if [[ "$2" == "on" ]] ;then
				value=$(( $((16#$tmp)) & $((16#$eth_led_on)) ))
			elif [[ "$2" == "off" ]] ;then
				value=$(( $((16#$tmp)) | $((16#$eth_led_off)) ))
			else
				help
				exit 1
			fi
			;;
	esac
else
	help
	exit 1
fi

#echo "[DEBUG] before value $value $((16#$value))"
value=$(echo "obase=16;$value"|bc)
#echo "[DEBUG] after value $value $((16#$value))"
i2cset -y 0 0x21 0x03 0x$value
