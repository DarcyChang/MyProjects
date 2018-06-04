#!/bin/bash
#Objective:Automatic Google stress
#Author:Darcy Chang
#Date:2018/06/01


source /root/automation/Library/path.sh


function eth_stat() {
    rate_tmp_file="/tmp/eth_stat"
    sar -n DEV $eth_stat_interval 1 | grep Average > $rate_tmp_file
    eth_idx=0
    eth_stat_msg=""
    while [ "$eth_idx" -lt "$eth_num" ]
    do
		link_state=`ethtool ${eth_name[$eth_idx]} | grep 'Link detected' | awk '{print $3}'`
		if [ "$link_state" != "yes" ]; then
			speed="down"
		else
			speed=`ethtool ${eth_name[$eth_idx]} | grep 'Speed:' | awk '{print $2}' | sed 's/M.*$//g'`
			duplex=`ethtool ${eth_name[$eth_idx]} | grep 'Duplex:' | awk '{print $2}' | sed 's/...$//g' | tr [:upper:] [:lower:]`
			speed="${speed}${duplex}"
		fi
        if [ "$speed" == "1000f" ] ; then
            speed="1g"
        elif [ "$speed" == "down" ]; then
            eth_link_down_count[$eth_idx]=`expr ${eth_link_down_count[$eth_idx]} + 1`
        fi
        rx_rate=`grep "${eth_name[$eth_idx]} " $rate_tmp_file | awk '{print $5}'`
        tx_rate=`grep "${eth_name[$eth_idx]} " $rate_tmp_file | awk '{print $6}'`
        rx_rate=`echo "($rx_rate * 8) / 1000" | bc`
        tx_rate=`echo "($tx_rate * 8) / 1000" | bc`
        eth_rx_rate_sum[$eth_idx]=`expr ${eth_rx_rate_sum[$eth_idx]} + $rx_rate`
        eth_tx_rate_sum[$eth_idx]=`expr ${eth_tx_rate_sum[$eth_idx]} + $tx_rate`
        eth_stat_msg="$eth_stat_msg${eth_name[$eth_idx]}(${speed}):$rx_rate/$tx_rate "
        eth_idx=`expr $eth_idx + 1`
    done
    eth_rate_count=`expr $eth_rate_count + 1`
    rm $rate_tmp_file
}

function cpu_stat() {
    cpu_idle=`sar -u $cpu_stat_interval 1 | grep Average | awk '{ printf $8 }'`
    cpu_load=`echo "scale=1; 100 - $cpu_idle" | bc`
    cpu_tmp=`cat /sys/devices/platform/coretemp.0/temp2_input`
    cpu_tmp=`echo "$cpu_tmp / 1000" | bc`
    cpu_tmp_sum=`expr $cpu_tmp_sum + $cpu_tmp`
    cpu_stat_msg="CPU:$cpu_tmp|${cpu_load}%%"
    cpu_clk_file="/tmp/cpu_clk_stat"
    grep 'cpu MHz' /proc/cpuinfo > $cpu_clk_file
    core_id=0
    while [ "$core_id" -lt "$core_num" ]
    do
        temp_id=`expr $core_id \* 2 + 2`
        core_tmp=`cat /sys/devices/platform/coretemp.0/temp${temp_id}_input`
        core_tmp=`echo "$core_tmp / 1000" | bc`
        core_tmp_sum[$core_id]=`expr ${core_tmp_sum[$core_id]} + $core_tmp`
        line=`expr $core_id + 1`
        clock=`sed -n ${line}p $cpu_clk_file | awk '{ print $4 }' | sed 's/\..*$//g'`
        if [ "$clock" -ge "2000" ]; then
            core_2g_clock_count[$core_id]=`expr ${core_2g_clock_count[$core_id]} + 1`
        elif [ "$clock" -ge "1000" ]; then
            core_1g_clock_count[$core_id]=`expr ${core_1g_clock_count[$core_id]} + 1`
        elif [ "$clock" -ge "490" ]; then
            core_5m_clock_count[$core_id]=`expr ${core_5m_clock_count[$core_id]} + 1`
        else
            core_2m_clock_count[$core_id]=`expr ${core_2m_clock_count[$core_id]} + 1`
        fi
        cpu_stat_msg="$cpu_stat_msg $core_id:${core_tmp}|${clock}"
        core_id=`expr $core_id + 1`
    done
    cpu_stat_count=`expr $cpu_stat_count + 1`
    rm $cpu_clk_file
}

function mem_stat() {
    mem_tmp_file="/tmp/mem_stat"
    cat /proc/meminfo | grep Mem > $mem_tmp_file
    mem_total=`grep MemTotal $mem_tmp_file | awk '{ printf $2 }'`
    mem_free=`grep MemFree $mem_tmp_file | awk '{ printf $2 }'`
    mem_used=`echo "scale=1; ( ($mem_total - $mem_free) * 100 ) / $mem_total" | bc`
    mem_stat_msg="MEM:${mem_used}%%"
    rm $mem_tmp_file
}

function show_stat() {
    eth_stat
    cpu_stat
    mem_stat
    cur_time=`cat /proc/uptime | cut -d. -f1`
    if [ $end_time -lt $cur_time ]; then
        remain_time=0
    else
        remain_time=`expr $end_time - $cur_time`
    fi
    hour=`echo "$remain_time / 3600" | bc`
    min=`echo "( $remain_time % 3600 ) / 60 " | bc`
    sec=`echo "( $remain_time % 3600 ) % 60 " | bc`

#    printf "%02d:%02d:%02d ${cpu_stat_msg} ${mem_stat_msg} ${eth_stat_msg}\n" $hour $min $sec
	if [ $dut_id == "1" ] ; then
		printf "[GS] %02d:%02d:%02d ${cpu_stat_msg} ${mem_stat_msg} ${eth_stat_msg}\n" $hour $min $sec
	else                                                                   
		printf "[DUT] %02d:%02d:%02d ${cpu_stat_msg} ${mem_stat_msg} ${eth_stat_msg}\n" $hour $min $sec
	fi
}

# 2 USB + 1 MSATA
no_iperf=0
no_stress=0
no_disk_test=0
#time=28800
time=$(cat /root/automation/config | grep "burn-in time(seconds)" | awk '{print $3}')
dut_id=2 # DUT = 2, GOLDEN = 1
core_num=2
eth_num=5
eth_name[0]="eth0"
eth_name[1]="eth1"
eth_name[2]="eth2"
eth_name[3]="eth3"
eth_name[4]="eth4"
eid_list="0 1 2 3 4"
nic_rate_min=10
swh_rate_min=1
total_rate_min=200
link_down_limit=1
stress_duration=180
stress_interval=600
#free_memory=$(free -m | grep Mem | awk '{print $4}')
#stress_arg="-M $free_memory -W -C 1 -m 1 -i 1 --cc_test -v 20"
stress_arg="-M 100 -W -C 1 -m 1 -i 1 --cc_test -v 20"
iperf_arg="-D"
tcp_parallels=1
extra_disk_error_retries=2
tmp_file="tmp_dd5"
wifi_check=0

while [[ $# > 0 ]]
do
    key="$1"
    case $key in
    -d)
    disk_num="$2"
    shift
    ;;
    --stress_arg)
    stress_arg="$2"
    shift
    ;;
    --stress_duration)
    stress_duration="$2"
    shift
    ;;
    --stress_interval)
    stress_interval="$2"
    shift
    ;;
    --no_iperf)
    no_iperf=1
    ;;
    --no_stress)
    no_stress=1
    ;;
    --no_disk)
    no_disk_test=1
    ;;
    --disk_retries)
    extra_disk_error_retries="$2"
    shift
    ;;
    -t)
    time="$2"
    shift
    ;;
    -i)
	# DUT = 2, GOLDEN = 1
    dut_id="$2"
    shift
    ;;
    -R)
    nic_rate_min="$2"
    shift
    ;;
    -r)
    swh_rate_min="$2"
    shift
    ;;
    -T)
    total_rate_min="$2"
    shift
    ;;
    -s)
    iperf_arg="$iperf_arg -s"
    ;;
    -e)
    eid_list="$2"
    shift
    ;;
    -P)
    tcp_parallels="$2"
    shift
    ;;    
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
    esac
    shift # past argument or value
done

echo "Stress Test v1.2"


eth_num=5

if [ "$no_iperf" == "1" ]; then
    eth_num=1
fi

if [ "$no_iperf" == "1" ] && [ "$no_stress" == "1" ]; then
    echo "No test to run"
    exit 0
fi

eid_list="0 1 2 3 4"

if [ "$no_stress" == "0" ] && [ "$no_disk_test" == "0" ]; then
	disk_num=$(lsblk | grep -v "NAME" | grep "-" | awk '{print $1}' |  cut -d "-" -f 2 | wc -l)
	for ((i=2; i<=disk_num; i++)) ; do # Skip sda1. Because sda1 is boot partition.
		disk_array[$i]=$(lsblk | grep -v "NAME" | grep "-" | awk '{print $1}' |  cut -d "-" -f 2 | awk 'NR=='$i'{print}')
        umount /dev/${disk_array[$i]} 2> /dev/null
        fsck -M /dev/${disk_array[$i]} -p
		mkdir -p /tmp/${disk_array[$i]}
        mount /dev/${disk_array[$i]} /tmp/${disk_array[$i]}
        if [ $? -ne 0 ]; then
            echo "Failed to mount /dev/${disk_array[$i]}"
            exit 1
        fi
        stress_arg="$stress_arg -f /tmp/${disk_array[$i]}/${tmp_file}"
	done
fi


if [ "$no_iperf" == "0" ]; then
    if [ "$dut_id" == "1" ]; then # Golden Sample
        iperf_arg="$iperf_arg -g"
    fi
#	echo "[DEBUG] /root/automation/T55_MFG/iperf_test.sh $iperf_arg -e $eid_list -a -P $tcp_parallels -f" | tee -a $log_path
    /root/automation/T55_MFG/iperf_test.sh $iperf_arg -e "$eid_list" -a "-P $tcp_parallels" -f
fi

cpu_stat_interval=1
mem_stat_interval=1
eth_stat_interval=2

echo "[SENAO] Stress test running $time seconds"
if [ "$no_stress" == "0" ] && [ "$no_iperf" == "0" ]; then
    echo "[SENAO] Run stress and iperf test"
elif [ "$no_stress" == "0" ]; then
    echo "[SENAO] Run stress test"
else
    echo "[SENAO] Run iperf test"
fi

eth_rate_count=0
eth_idx=0
while [ "$eth_idx" -lt "$eth_num" ]
do
    eth_rx_rate_sum[$eth_idx]=0
    eth_tx_rate_sum[$eth_idx]=0
    eth_link_down_count[$eth_idx]=0
    eth_idx=`expr $eth_idx + 1`
done

cpu_stat_count=0
core_id=0
while [ "$core_id" -lt "$core_num" ]
do
    core_2g_clock_count[$core_id]=0
    core_1g_clock_count[$core_id]=0
    core_5m_clock_count[$core_id]=0
    core_2m_clock_count[$core_id]=0
    core_org_throttle_count[$core_id]=`cat /sys/devices/system/cpu/cpu${core_id}/thermal_throttle/core_throttle_count`
    core_tmp_sum[$core_id]=0
    core_id=`expr $core_id + 1`
done
cpu_tmp_sum=0

trap 'killall stressapptest; killall -9 iperf; echo "Test is stopped by user"; exit 0' SIGINT

killall -9 stressapptest &> /dev/null

cur_time=`cat /proc/uptime | cut -d. -f1`
end_time=`expr $cur_time + $time`
stress_fail=0
while [ "$cur_time" -lt "$end_time" ] && [ "$stress_fail" == "0" ]
do
    if [ "$no_stress" == "1" ]; then
        show_stat
    else
        remaining_time=`expr $end_time - $cur_time`
        if [ "$remaining_time" -lt "$stress_duration" ]; then
            stress_time=$remaining_time
            if [ "$stress_time" -lt "30" ]; then
                stress_time=0
            fi
        else
            stress_time=$stress_duration
        fi
        if [ "$stress_time" != "0" ]; then
            res_file=/tmp/stress_res
            /root/automation/T55_MFG/stressapptest $stress_arg -s $stress_time > $res_file &
#			echo "[DEBUG] $stress_arg"
#			echo "[DEBUG] /root/automation/T55_MFG/stressapptest $stress_arg -s $stress_time > $res_file &"
            sleep 3
            stress_running=1
            while [ "$stress_running" != "0" ]
            do
                show_stat
                stress_running=`ps aux | grep stressapptest | grep -vc grep`
            done
            res=`grep 'Status: FAIL' $res_file`
            if [ "$res" != "" ]; then
                res=`grep 'Report Error:' $res_file | grep -v ${tmp_file}`
                if [ "$res" == "" ]; then
					for ((i=2; i<=disk_num; i++)) ; do
                        res=`grep 'Report Error:' $res_file | grep "/tmp/${disk_array[$i]}"`
                        if [ "$res" != "" ]; then
                            echo "Found Disk ${disk_array[$i]} error"
        					umount /dev/${disk_array[$i]} 2> /dev/null
					        fsck -M /dev/${disk_array[$i]} -p
					        mount /dev/${disk_array[$i]} /tmp/${disk_array[$i]}
                            extra_disk_error_retries=`expr $extra_disk_error_retries - 1`
                            [ "$extra_disk_error_retries" -lt "0" ] && stress_fail=1
                        fi
					done
                else
                    stress_fail=1
                fi
            fi
        fi
        if [ "$stress_fail" == "0" ]; then
            cur_time=`cat /proc/uptime | cut -d. -f1`
            next_time=`expr $cur_time + $stress_interval`
            while [ "$cur_time" -lt "$next_time" ] && [ "$cur_time" -lt "$end_time" ]
            do
                show_stat
                cur_time=`cat /proc/uptime | cut -d. -f1`
            done
        fi
    fi
    cur_time=`cat /proc/uptime | cut -d. -f1`
done

average_cpu_tmp=`echo "$cpu_tmp_sum / $cpu_stat_count" | bc`
echo "CPU Average Temperature: $average_cpu_tmp degree"
core_id=0
while [ "$core_id" -lt "$core_num" ]
do
    average_core_tmp=`echo "${core_tmp_sum[$core_id]} / $cpu_stat_count" | bc`
    echo "Core${core_id} Average Temperature: $average_core_tmp degree"
    percent_2g=`echo "( ${core_2g_clock_count[$core_id]} * 100 ) / $cpu_stat_count" | bc`
    percent_1g=`echo "( ${core_1g_clock_count[$core_id]} * 100 ) / $cpu_stat_count" | bc`
    percent_5m=`echo "( ${core_5m_clock_count[$core_id]} * 100 ) / $cpu_stat_count" | bc`
    percent_2m=`echo "( ${core_2m_clock_count[$core_id]} * 100 ) / $cpu_stat_count" | bc`
    echo "Core${core_id} Clock Ratio: 2GHz ${percent_2g}% 1GHz ${percent_1g}% 500MHz ${percent_5m}% 250MHz ${percent_2m}%"
    new_throttle_count=`cat /sys/devices/system/cpu/cpu${core_id}/thermal_throttle/core_throttle_count`
    throttle_count=`expr $new_throttle_count - ${core_org_throttle_count[$core_id]}`
    echo "Core${core_id} Throttle Count: $throttle_count"
    core_id=`expr $core_id + 1`
done

if [ "$no_stress" == "0" ]; then
    cat $res_file
    if [ "$no_disk_test" == "0" ]; then
		for ((i=2; i<=disk_num; i++)) ; do
			umount /dev/${disk_array[$i]}
			rm -rf /tmp/${disk_array[$i]}/${tmp_file}
		done
    fi
fi

if [ "$no_iperf" == "0" ]; then
    eth_idx=0
    total_rx_rate=0
    total_tx_rate=0
    while [ "$eth_idx" -lt "$eth_num" ]
    do
        average_rx_rate=`echo "${eth_rx_rate_sum[$eth_idx]} / $eth_rate_count" | bc`
        average_tx_rate=`echo "${eth_tx_rate_sum[$eth_idx]} / $eth_rate_count" | bc`
		is_vlan_eth=`echo ${eth_name[$eth_idx]} | grep -c '\.'`
        if [ "$is_vlan_eth" == "0" ]; then
            rate_min=$nic_rate_min
            total_rx_rate=`expr $total_rx_rate + $average_rx_rate`
            total_tx_rate=`expr $total_tx_rate + $average_tx_rate`
        else
            rate_min=$swh_rate_min
            total_rx_rate=`expr $total_rx_rate + $average_rx_rate`
            total_tx_rate=`expr $total_tx_rate + $average_tx_rate`
        fi
        if [ "$average_rx_rate" -lt "$rate_min" ] || [ "$average_tx_rate" -lt "$rate_min" ]; then
            result="failed"
        else
            result="pass"
        fi
        echo "${eth_name[$eth_idx]} check average rx/tx rate: [$result] [$average_rx_rate/$average_tx_rate Mbits/sec]"
        if [ "$is_vlan_eth" == "0" ]; then
            rx_errors=`ifconfig ${eth_name[$eth_idx]} | grep 'RX packets' | awk '{print $3}' | cut -d: -f2`
            tx_errors=`ifconfig ${eth_name[$eth_idx]} | grep 'TX packets' | awk '{print $3}' | cut -d: -f2`
            if [ "$rx_errors" != "0" ] || [ "$tx_errors" != "0" ]; then
                result="failed"
            else
                result="pass"
            fi
            echo "${eth_name[$eth_idx]} check error counter:      [$result] [RX:$rx_errors TX:$tx_errors]"
            if [ "$rx_errors" != "0" ] || [ "$tx_errors" != "0" ]; then
                ethtool -S ${eth_name[$eth_idx]} | grep errors | grep -v 'errors: 0'
            fi
        fi
        if [ "${eth_link_down_count[$eth_idx]}" -gt "$link_down_limit" ]; then
            result="failed"
        else
            result="pass"
        fi
        echo "${eth_name[$eth_idx]} check link status:        [$result] [detected ${eth_link_down_count[$eth_idx]} time(s) of port link down]"
        eth_idx=`expr $eth_idx + 1`
    done
    if [ "$total_rx_rate" -lt "$total_rate_min" ] || [ "$total_tx_rate" -lt "$total_rate_min" ]; then
        result="failed"
    else
        result="pass"
    fi
    echo "check total rx/tx rate: [$result] [$total_rx_rate/$total_tx_rate Mbits/sec]"

    client_pids=`ps aux | grep iperf | grep -v grep | grep -v 'iperf -s' | awk '{print $2}'`
    for pid in $client_pids; do
        kill -9 $pid
    done
fi
