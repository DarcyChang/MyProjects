#!/bin/bash
#Objective:Automatic Google stress
#Author:Darcy Chang
#Date:2018/03/20


function eth_stat() {
    rate_tmp_file="/tmp/eth_stat"
    sar -n DEV $eth_stat_interval 1 | grep Average > $rate_tmp_file
    swh_tmp_file="/tmp/swh_stat"
    cat $Driver_Path > $swh_tmp_file
    eth_idx=0
    eth_stat_msg=""
    while [ "$eth_idx" -lt "$eth_num" ]
    do
        is_vlan_eth=`echo ${eth_name[$eth_idx]} | grep -c '\.'`
        if [ "$is_vlan_eth" == "0" ]; then
            link_state=`ethtool ${eth_name[$eth_idx]} | grep 'Link detected' | awk '{print $3}'`
            if [ "$link_state" != "yes" ]; then
                speed="down"
            else
                speed=`ethtool ${eth_name[$eth_idx]} | grep 'Speed:' | awk '{print $2}' | sed 's/M.*$//g'`
                duplex=`ethtool ${eth_name[$eth_idx]} | grep 'Duplex:' | awk '{print $2}' | sed 's/...$//g' | tr [:upper:] [:lower:]`
                speed="${speed}${duplex}"
            fi
        else
            vid=`echo ${eth_name[$eth_idx]} | cut -d. -f2`
            num=`expr $vid - 2`
            link_state=`grep Port$num $swh_tmp_file | awk '{print $2}'`
            if [ "$link_state" != "UP" ]; then
                speed="down"
            else
                speed=`grep Port$num $swh_tmp_file | awk '{print $3}'`
            fi
        fi
        if [ "$speed" == "1000f" ]; then
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
    rm $swh_tmp_file
}

function cpu_stat() {
    cpu_idle=`sar -u $cpu_stat_interval 1 | grep Average | awk '{ printf $8 }'`
    cpu_load=`echo "scale=1; 100 - $cpu_idle" | bc`
    cpu_tmp=`cat /sys/devices/platform/nct6779.656/temp2_input`
    cpu_tmp=`echo "$cpu_tmp / 1000" | bc`
    cpu_tmp_sum=`expr $cpu_tmp_sum + $cpu_tmp`
    cpu_stat_msg="CPU:$cpu_tmp|${cpu_load}%%"
    cpu_clk_file="/tmp/cpu_clk_stat"
    grep 'cpu MHz' /proc/cpuinfo > $cpu_clk_file
    core_id=0
    while [ "$core_id" -lt "$core_num" ]
    do
        temp_id=`expr $core_id \* 2 + 2`
        core_tmp=`cat /sys/class/hwmon/hwmon1/temp${temp_id}_input`
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

    printf "%02d:%02d:%02d ${cpu_stat_msg} ${mem_stat_msg} ${eth_stat_msg}\n" $hour $min $sec
    #if [ "$HOSTNAME" == "T55-wifi" ]; then
    #    wifi_stat
    #fi                         remove to avoid invalid argument problem
}

# 2 USB + 1 MSATA
disk_num=3
no_iperf=0
no_stress=0
no_disk_test=0
time=28800
dut_id=1 # DUT = 2, GOLDEN = 1
core_num=2
eth_num=5
vlan=1
eth_name[0]="eth0.3"
eth_name[1]="eth0.4"
eth_name[2]="eth0.5"
eth_name[3]="eth0.6"
eth_name[4]="eth0.7"
eid_list=""
nic_rate_min=10
swh_rate_min=1
total_rate_min=200
link_down_limit=1
stress_duration=180
stress_interval=600
stress_arg="-M 1450 -W -C 1 -m 1 -i 1 --cc_test -v 4"
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

echo "Stress Test v1.1"

for (( i = 0; i < 10; i ++)); do
    Driver_Path="/proc/driver/igb/0000:0$i:00.0/test_mode"
    if [ -f "$Driver_Path" ]; then
        break
    fi
done

vlan=1
eth_num=5

if [ "$no_iperf" == "1" ]; then
    eth_num=1
    vlan=0
fi

if [ "$no_iperf" == "1" ] && [ "$no_stress" == "1" ]; then
    echo "No test to run"
    exit 0
fi

:<<SKIP
if [ "$time" == "0" ]; then
    read -p "Enter runtime(sec): " time
    if [ "$time" == "" ]; then
        time=43200
    fi
fi
SKIP

eid_list="0.3 0.4 0.5 0.6 0.7"

:<<SKIP
while [ "$no_iperf" == "0" -a "$dut_id" != "1" -a "$dut_id" != "2" ]
do
    read -p "Enter DUT ID (1/2): " dut_id
done
SKIP

if [ "$no_stress" == "0" ] && [ "$no_disk_test" == "0" ]; then
    disk_list=`fdisk -l 2>/dev/null | grep Disk | grep -v ram |grep /dev/ | awk '{print $2}' | cut -d/ -f3 | sed 's/://'`
    sys_disk=`mount | grep 'on / ' | cut -d' ' -f1 | cut -d/ -f3 | sed 's/.$//'`
    detected_disk_count=0
    extra_disk_list=""
    for disk in $disk_list; do
        if [ "$disk" != "$sys_disk" ]; then
            extra_disk_list="${extra_disk_list}${disk} "
        fi
        detected_disk_count=`expr $detected_disk_count + 1`
    done

    if [ "$detected_disk_count" -lt "$disk_num" ]; then
        fdisk -l 2>/dev/null | grep Disk | grep /dev/
        echo "Detected disk number is not enough"
        exit 1
    fi

    count=0
    extra_test_disk_count=`expr $disk_num - 1`
    extra_test_disk_list=""
    for disk in $extra_disk_list; do
        if [ "$count" -lt "$extra_test_disk_count" ]; then
            extra_test_disk_list="${extra_test_disk_list}${disk} "
            count=`expr $count + 1`
        fi
    done
    test_disk_list="${extra_test_disk_list}${sys_disk}"
    
    echo System Disk: ${sys_disk}
    echo Other Disks: ${extra_disk_list}

    mkdir -p /tmp/${sys_disk}
    stress_arg="$stress_arg -f /tmp/${sys_disk}/${tmp_file}"
    for disk in $extra_test_disk_list; do
        disk_part=${disk}1
        umount /dev/$disk_part 2> /dev/null
        fsck /dev/$disk_part -p
        mkdir -p /tmp/$disk
        mount /dev/$disk_part /tmp/$disk
        if [ $? -ne 0 ]; then
            echo "Failed to mount /dev/$disk_part"
            exit 1
        fi
        stress_arg="$stress_arg -f /tmp/${disk}/${tmp_file}"
    done
fi


if [ "$no_iperf" == "0" ]; then
    if [ "$dut_id" == "1" ]; then
        iperf_arg="$iperf_arg -g"
    fi
    /root/automation/T55_MFG/iperf_test.sh $iperf_arg -e "$eid_list" -a "-P $tcp_parallels" -f
fi

cpu_stat_interval=1
mem_stat_interval=1
eth_stat_interval=2
if [ "$no_stress" == "0" ] && [ "$no_iperf" == "0" ]; then
    echo "Running stress and iperf test"
elif [ "$no_stress" == "0" ]; then
    echo "Running stress test"
else
    echo "Running iperf test"
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
            echo "Stress test running"
            /root/automation/T55_MFG/stressapptest $stress_arg -s $stress_time > $res_file &
            sleep 3
            stress_running=1
            while [ "$stress_running" != "0" ]
            do
                show_stat
                stress_running=`ps aux | grep stressapptest | grep -vc grep`
            done
            echo "Stress test end"
            res=`grep 'Status: FAIL' $res_file`
            if [ "$res" != "" ]; then
                res=`grep 'Report Error:' $res_file | grep -v ${tmp_file}`
                if [ "$res" == "" ]; then
                    for disk in $test_disk_list; do
                        res=`grep 'Report Error:' $res_file | grep "/tmp/${disk}/${tmp_file}"`
                        if [ "$res" != "" ]; then
                            echo "Found Disk $disk error"
                            if [ "$disk" == "$sys_disk" ]; then
                                stress_fail=1
                            else
                                disk_part=${disk}1
                                umount /dev/$disk_part 2> /dev/null
                                fsck /dev/$disk_part -p
                                mount /dev/$disk_part /tmp/$disk
                                extra_disk_error_retries=`expr $extra_disk_error_retries - 1`
                                [ "$extra_disk_error_retries" -lt "0" ] && stress_fail=1
                            fi
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
        rm -rf /tmp/${sys_disk}
        for disk in $extra_test_disk_list; do
            disk_part=${disk}1
            rm -f /tmp/$disk/${tmp_file}
            umount /dev/$disk_part
            rm -rf /tmp/$disk
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

#    read -p "Press Enter to stop iperf" ps

    client_pids=`ps aux | grep iperf | grep -v grep | grep -v 'iperf -s' | awk '{print $2}'`
    for pid in $client_pids; do
        kill -9 $pid
    done
fi
