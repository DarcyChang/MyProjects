#!/bin/bash 

VERSION=0.1.2

function help() { 
	echo "usage: sbc530_api.sh <command>"
	echo ""
	echo "Following are commands:"
	echo "		version"
	echo "			Show Linux(Ubuntu) api version."
	echo ""
	echo "		cpu"
	echo "			Show CPU information."
	echo ""
	echo "		wdt	[sec 0-255]"
	echo "			Configure watchdog timer."
	echo "			If timer [sec] is greater than 0, watchdog starts the countdown and resets the deivce once the timer decreases to zero"
	echo "			If timer [sec] is set to 0, watchdog is disabled."
	echo "			If timer [sec] is not given, it shows current watchdog timer."
	echo ""
	echo "		gpio <type io|data> [val 0x0-0xff]"
	echo "			Configure the 8-pins GPIO settings."
	echo "			The <type> is used to specify what kind of the setting to be configured. The following 2 types are available:"
	echo "			io   - GPIO input/output mode (0:output 1:input)"
	echo "			data - GPIO data"
	echo "			If [val] is given, GPIO setting is configured with the given value."
	echo "			If [val] is not given, it shows current GPIO setting."
	echo "			Each bit of the value represents the setting of corresponding gpio pin."
	echo ""
	echo "		smbus <dev 0x0-0x7f> <reg 0x0-0xff> [data 0x0-0xff]"
	echo "			Read/Write data on SMBus."
	echo "			The <dev> is the address of the device on SMBus."
	echo "			The <reg> is the selected register of the device."
	echo "			If [data] is not given, read data from SMBus."
	echo "			If [data] is given, write data to SMBus."
	echo ""
	echo "		hwmon"
	echo "			Read the voltage and tempature from HW Monitor."
	echo ""
	echo "		brightness [val 0-100] [id 1|2]"
	echo "			Configure the brightness of monitor."
	echo "			This command works only when the monitor is connecting to device."
	echo "			If [val] is not given, display the id and brightness of the detected monitor(s)."
	echo "			If [val] is given, set the brightness of the detected monitor(s) with the given value."
	echo "			If [id] is given, set brightness of the monitor of the id specified."
	echo ""
	echo "		backlight [val 0-100]"
	echo "			Configure the backlight of display panel."
	echo "			This command works only when the display panel is connecting to device."
	echo "			If [val] is not given, display the backlight setting of panel."
	echo "			If [val] is given, change the backlight setting with given value."
	echo ""
	echo "		help"
	echo "			Show this usage."
	echo ""
}


function cpu() {
	cpu_speed=$(lscpu | grep -i "MHz")
	cpu_name=$(lscpu | grep "Model name:")
	cpu_core=$(cat /proc/cpuinfo | grep "cpu cores" | head -n 1 | awk '{print $4}')
	echo "$cpu_name"
	echo "cpu cores:	       $cpu_core"
	echo "$cpu_speed"
}


function wdt() {
	if [[ -z "$1" ]] ; then
		echo "$(cat /sys/devices/platform/nct6775.512/wdt/timer) seconds"
	elif [[ "$1" == "0" ]] ; then
		echo "watchdog disable"
		echo 0 > /sys/devices/platform/nct6775.512/wdt/enable
	elif [[ "$1" -gt 0 ]] && [[ "$1" -le 255 ]]; then
		echo "watchdog set $1 seconds"	
		echo 1 > /sys/devices/platform/nct6775.512/wdt/enable
		echo $1 > /sys/devices/platform/nct6775.512/wdt/timer
	else
		echo "[ERROR] Unknown parameter"
		echo "sbc530_api.sh wdt [sec 0-255]"
	fi

}


function gpio() {
#	echo "$1 $2"
	if [[ "$1" == "io"  ]] ; then	
		if [[ -z "$2" ]] ; then
			cat /sys/devices/platform/nct6775.512/gpio/io4
		else
			echo $2 > /sys/devices/platform/nct6775.512/gpio/io4	
		fi
	elif [[ "$1" == "data" ]] ; then
		if [[ -z "$2" ]] ; then
			cat /sys/devices/platform/nct6775.512/gpio/data4
		else
			echo $2 > /sys/devices/platform/nct6775.512/gpio/data4	
		fi
	else 
		echo "[ERROR] Unknown parameter"
		echo "sbc530_api.sh gpio <io|data> [0x0-0xff]"
	fi
}


function smbus() {
#	echo "$1 $2 $3"
	
	if [ -z "$1" ] || [ -z "$2" ] ; then
		echo "sbc530_api.sh smbus <dev 0x0-0x7f> <reg 0x0-0xff> [data 0x0-0xff]"
		echo ""
		i2cdetect -l | grep smbus
		echo ""
		i2cdetect -y 4
		exit 1
	fi
	if [[ -z "$3" ]] ; then
		echo "i2cget -y 4 $1 $2"
		i2cget -y 4 $1 $2
	else
		echo "i2cset -y 4 $1 $2 $3"
		i2cset -y 4 $1 $2 $3
	fi
}


function hw_monitor() {
	echo "VCC:		$(sensors | grep "VCC:" | awk '{print $2}' | cut -d "+" -f 2)"
	echo "P1V35_VDDQ:	$(sensors | grep "P1V35_VDDQ:" | awk '{print $2}' | cut -d "+" -f 2)"
	echo "P5V_A:		$(sensors | grep "P5V_A:" | awk '{print $2}' | cut -d "+" -f 2)"
	echo "DC_IN:		$(sensors | grep "DC_IN(P12V_A):" | awk '{print $2}' | cut -d "+" -f 2)"
	echo "CPU_TEMP:	$(sensors | grep "CPU_TEMP:" | awk '{print $2}' | cut -d "+" -f 2)"
}


function brightness() {
#	echo "$1 $2"
	if [[ -z "$1" ]] ; then
		temp1=$(xrandr --verbose | grep -A 6 "HDMI-1" | grep "Brightness" | cut -f2 -d ' ')
		temp2=$(xrandr --verbose | grep -A 6 "HDMI-2" | grep "Brightness" | cut -f2 -d ' ')
		if [[ -n "$temp1" ]] ; then
			hdmi1=$(echo "$temp1 * 100" | bc)
			echo "id 1 : HDMI-1 brightness $hdmi1"
		else
			echo "id 1 : HDMI-1 brightness $temp1"
		fi
		if [[ -n "$temp2" ]] ; then
			hdmi2=$(echo "$temp2 * 100" | bc)
			echo "id 2 : HDMI-2 brightness $hdmi2"
		else
			echo "id 2 : HDMI-2 brightness $temp2"
		fi
		exit 0
	fi
	
	if [ $(echo $1/1|bc) == "$1" ] && [ $1 -ge 0 ]  && [ $1 -le 100 ] ; then
		value=$(echo "scale=2; $1/100" | bc)
#		echo "value $value"
		if [[ -z "$2" ]] ; then
			monitor=$(xrandr --current | grep " connected" | grep -v "eDP-1" | awk '{print $1}' | head -n 1)
			xrandr --output $monitor --brightness $value
		else
			xrandr --output HDMI-$2 --brightness $value
		fi
	else
		echo "[ERROR] Unknown parameter"
		echo "sbc530_api.sh brightness [val 0-100] [id 1|2]"
	fi
}


function backlight() {
#	echo "$1"
	if [[ -z "$1" ]] ; then
		temp=$(cat /sys/class/backlight/intel_backlight/actual_brightness)
		value=$(echo "$temp / 960" | bc)
		echo "$value"
		exit 0
	fi
	if [ $(echo $1/1|bc) == "$1" ] && [ $1 -ge 0 ]  && [ $1 -le 100 ] ; then
		value=$(echo "$1 * 960" | bc)
#		echo "value $value"
		echo $value > /sys/class/backlight/intel_backlight/brightness
	else
		echo "[ERROR] Unknown parameter"
		echo "sbc530_api.sh backlight [val 0-100]"
	fi
}


case $1 in
	"")
		help # prepare for menu
		;;
	"version")
		echo "sbc530_api_version v$VERSION"
		;;
	"cpu")
		cpu
		;;
	"wdt")
		wdt $2
		;;
	"gpio")
		gpio $2 $3
		;;
	"smbus")
		smbus $2 $3 $4
		;;
	"hwmon")
		hw_monitor
		;;
	"brightness")
		brightness $2 $3
		;;
	"backlight")
		backlight $2
		;;
	"help")
		help
		;;
	*)
		help
		exit 1
		;;
esac
