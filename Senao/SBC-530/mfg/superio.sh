#!/bin/bash

res_file="/tmp/sensors_res"
detectV_list="VCC P1V35_VDDQ P5V_A DC_IN(P12V_A)"
detectT_list="CPU_TEMP"
T_max=80
T_min=20

cp ./sensors3.conf /etc/
sensors -s
sleep 0.5
sensors > $res_file


function usage()
{
    echo "   $0 --h                  	this page"
    echo "   $0 --list			check voltage num list"
    echo "   $0 --VL <list>		input list of voltage"
    echo "   $0 --TL <list>		input list of temperature"
    echo "   $0 --auto			auto detect all items"
    echo "   $0 --min <num> <value>  	setting <num>'s min value"
    echo "   $0 --max <num> <value>  	setting <num>'s max value"
    echo "   $0 --Tmin <value>	  	setting Temp's min value"
    echo "   $0 --Tmax <value>	  	setting Temp's max value"
    exit
}

function auto_detect()
{
    detectV_list=$(sensors | grep V | grep -v Adapter | awk '{print $1}' | sed 's/.$//')
    detectT_list=$(sensors | grep TEMP | awk '{print $1}' | sed 's/.$//')
}

count=0
while [[ $# > 0 ]]
do
   key="$1"
   case $key in
   --auto)
   auto_detect
   ;;
   --VL)
   detectV_list=$2
   shift
   ;;
   --TL)
   detectT_list=$2
   shift
   ;;
   --min)
   min_max[$count]="min"
   colum[$count]=$2
   data[$count]=$3
   shift
   shift
   count=$(expr $count + 1)
   ;;
   --max)
   min_max[$count]="max"
   colum[$count]=$2
   data[$count]=$3
   shift
   shift
   count=$(expr $count + 1)
   ;;
   --Tmin)
   T_min=$2
   shift
   ;;
   --Tmax)
   T_max=$2
   shift
   ;;
   --list)
   i=0
   for V in $detectV_list; do
        echo "[$i]: $V"
	i=$(expr $i + 1)
   done
   exit
   ;;
   --h)
   usage
   ;;
   *)
   echo "unknown option '$key'"
   ;;
   esac
   shift
done

i=0
for V in $detectV_list; do
    V_value[$i]=$(cat $res_file | grep $V: | cut -d':' -f2 | awk '{print $1}' | cut -d'+' -f2)
    V_min[$i]=$(cat $res_file | grep $V: | cut -d'=' -f2 | awk '{print $1}' | cut -d'+' -f2)
    V_max[$i]=$(cat $res_file | grep $V: | cut -d'=' -f3 | awk '{print $1}' | cut -d'+' -f2)
    i=$(expr $i + 1)
done

i=0
for T in $detectT_list; do
    T_value[$i]=$(cat $res_file | grep "$T" | cut -d':' -f2 | awk '{print $1}' | sed 's/^.//' | sed 's/..$//')
    i=$(expr $i + 1)
done

# Detect custom setting MIN and MAX
for (( i = 0; i < $count; i++ )); do
    if [ "${min_max[$i]}" == "min" ]; then
        V_min[${colum[$i]}]=${data[$i]}
    elif [ "${min_max[$i]}" == "max" ]; then
	V_max[${colum[$i]}]=${data[$i]}
    fi
done

i=0
for V in $detectV_list; do
    if [ `echo "${V_value[$i]} < ${V_min[$i]}" | bc` -eq 1 ] || [ `echo "${V_value[$i]} > ${V_max[$i]}" | bc` -eq 1 ]; then
	echo "$V FAILED"
        echo "$V: ${V_value[$i]}  min: ${V_min[$i]}  max: ${V_max[$i]}"
    else
	echo "$V PASS"
    fi
    #echo "$V: ${V_value[$i]}  min: ${V_min[$i]}  max: ${V_max[$i]}" 
    i=$(expr $i + 1)
done

i=0
for T in $detectT_list; do
if [ `echo "${T_value[$i]} < $T_min" | bc` -eq 1 ] || [ `echo "${T_value[$i]} > $T_max" |bc` -eq 1 ]; then
    echo $T FAILED
    echo "$T: ${T_value[$i]}°C  min: $T_min  max: $T_max"
else
    echo "$T PASS"
    i=$(expr $i + 1)
fi
done
