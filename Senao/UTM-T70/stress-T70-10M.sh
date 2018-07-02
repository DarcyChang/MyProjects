#!/bin/bash

model=$(pwd | cut -d/ -f 3)
model=ENA-1200
case $model in
ENA-1011)
    loopback_list="po1:po5,po2:po6,po3:po7,po4:po8,po9:po10"
    ;;
ENA-1200)
    loopback_list="eth0:eth1,eth2:eth3"
    ;;
ENA-3010)
    loopback_list="eth0:eth1,eth2:eth3,eth4:eth5,eth6:eth7"
    ;;
SBC-530)
    loopback_list="eth0:eth1"
    ;;
SBC-1100)
    loopback_list="eth0:eth1"
    ;;
esac
mmc_disk='mmcblk0'
stress_cpu_arg="-W -C 1 --cc_test -m 1 -i 1"
iperf_arg="-w 512k -P 2"
stat_timer=3
rate_criteria=10
disk_count=0

while [[ $# > 0 ]]
do
    key="$1"
    case $key in
    -M)
    stress_mem_arg="-M $2"
    shift
    ;;
    -u)
    disk_count=$2
    shift
    ;;
    --filesize)
    stress_filesize_arg="--filesize ${2}M"
    shift
    ;;
    --iperf_arg)
    iperf_arg="$2"
    shift
    ;;
    -l)
    loopback_list="$2"
    shift
    ;;
    -d)
    disk_list="$2"
    shift
    ;;
    --stat_timer)
    stat_timer="$2"
    shift
    ;;
    -t)
    time="$2"
    shift
    ;;
    -T)
    rate_criteria="$2"
    shift
    ;;
    --no_iperf)
    no_iperf=1
    ;;
    --no_disk)
    no_disk=1
    ;;
    --no_mmc)
    no_mmc=1
    ;;
    --no_sensor_stat)
    no_sensor_stat=1
    ;;
    --no_cpu_stat)
    no_cpu_stat=1
    ;;
    --no_mem_stat)
    no_mem_stat=1
    ;;
    --no_disk_stat)
    no_disk_stat=1
    ;;
    --no_err_pkt_stat)
    no_err_pkt_stat=1
    ;;
    *)
    # unknown option
    echo "unknown option '$key'"
    ;;
    esac
    shift # past argument or value
done

function get_iface_link {
    if [ "$model" == "ENA-1011" ]; then
        local port_num=$(echo $1 | sed 's/^po//g')
        if (( port_num < 9 )); then
            get_iface_link_ret=$(swh_ctl link_status $port_num | grep -c 'link:1')
        else
            get_iface_link_ret=$(ethtool $1 | grep -c 'Link detected: yes')
        fi
    else
        get_iface_link_ret=$(ethtool $1 | grep -c 'Link detected: yes')
    fi
}

function wait_iface_link_up {
    local timeout=$2
    while (( timeout > 0 ));
    do
        get_iface_link $1
        if [ "$get_iface_link_ret" != "0" ]; then
            wait_iface_link_up_ret=1
            return
        fi
        sleep 1
        timeout=$(( timeout - 1 ))
    done
    wait_iface_link_up_ret=0
}

function show_stat() {
    if [ -z "$no_sensor_stat" ]; then
        sar -m CPU,FAN,IN,TEMP $stat_timer 1 | grep Average 1> /tmp/1.stat.tmp &
    fi
    if [ -z "$no_cpu_stat" ]; then
        sar -P ALL $stat_timer 1 | grep Average | grep -v all 1> /tmp/2.stat.tmp &
    fi
    if [ -z "$no_mem_stat" ]; then
        sar -r $stat_timer 1 | sed -n 3,4p 1> /tmp/3.stat.tmp &
        sar -S $stat_timer 1 | sed -n 3,4p 1> /tmp/4.stat.tmp &
    fi
    if [ -z "$no_disk_stat" ]; then
        sar -d -p $stat_timer 1 | grep Average 1> /tmp/5.stat.tmp &
    fi
    if [ -z "$no_err_pkt_stat" ]; then
        sar -n EDEV $stat_timer 1 | grep Average | grep -v lo 1> /tmp/6.stat.tmp &
    fi
    if [ -z "$no_nic_stat" ]; then
        sar -n DEV $stat_timer 1 | grep Average | grep -v lo 1> /tmp/7.stat.tmp
    fi
    local sar_running=1
    while [ "$sar_running" != "0" ]
    do
        sar_running=$(ps aux | grep 'sar -' | grep -vc grep)
        sleep 1
    done

    local cur_time=$(cat /proc/uptime | cut -d. -f1)
    local elapsed_time=$(expr $cur_time - $start_time)
    [ $end_time -lt $cur_time ] && time_left=0 || time_left=$(expr $end_time - $cur_time)
    local el_hour=$(echo "$elapsed_time / 3600" | bc)
    local el_min=$(echo "( $elapsed_time % 3600 ) / 60 " | bc)
    local el_sec=$(echo "( $elapsed_time % 3600 ) % 60 " | bc)
    local le_hour=$(echo "$time_left / 3600" | bc)
    local le_min=$(echo "( $time_left % 3600 ) / 60 " | bc)
    local le_sec=$(echo "( $time_left % 3600 ) % 60 " | bc)

    echo "-------------------------------------------------------"
    printf "elapsed time %02d:%02d:%02d\n" $el_hour $el_min $el_sec
    printf "time left    %02d:%02d:%02d\n" $le_hour $le_min $le_sec

    if [ -z "$no_iperf" ]; then
        for (( i = 0; i < $if_count; i++));
        do
            local rx_rate=$(grep "${if_name[$i]} " /tmp/7.stat.tmp | awk '{print $5}')
            local tx_rate=$(grep "${if_name[$i]} " /tmp/7.stat.tmp | awk '{print $6}')
            if_rx_rate_sum[i]=$(echo "${if_rx_rate_sum[$i]} + ($rx_rate * 8) / 1000" | bc)
            if_tx_rate_sum[i]=$(echo "${if_tx_rate_sum[$i]} + ($tx_rate * 8) / 1000" | bc)
            get_iface_link ${if_name[$i]}
            if [ "$get_iface_link_ret" == "0" ]; then
                if_no_link[i]=$(( if_no_link[i] + 1 ))
                echo "warning: ${if_name[$i]} link down"
            fi
            
        done
        stat_rate_count=$(( stat_rate_count + 1 ))
    fi

    if [ -z "$no_cpu_stat" ]; then
        cores_speed=$(grep MHz /proc/cpuinfo | awk '{print $4}')
        local i=0
        printf "CPU Speed:"
        for speed in $cores_speed;
        do
            printf "%d:%.0f " $i $speed
            i=$(( i + 1 ))
        done
        printf "\n"
    fi
    cat /tmp/*.stat.tmp
    rm /tmp/*.stat.tmp
}

ethtool -s eth0 autoneg off speed 10 duplex full
ethtool -s eth1 autoneg off speed 10 duplex full
echo "sset 10f" >/proc/driver/igb/0000:04:00.0/test_mode
echo "vloop" > /proc/driver/igb/0000\:04\:00.0/test_mode

if [ -z "$time" ]; then
    read -p "Enter runtime: " time
fi

if [ -z "$no_iperf" ] && [ -z "$loopback_list" ] ; then
    echo error: no loopback list specified
fi

day=$(echo $time | grep -o -e '[0-9]\+[Dd]' | sed -n 's/[Dd]*//gp')
[ -z "$day" ] && day=0
hour=$(echo $time | grep -o -e '[0-9]\+[Hh]' | sed -n 's/[Hh]*//gp')
[ -z "$hour" ] && hour=0
min=$(echo $time | grep -o -e '[0-9]\+[Mm]' | sed -n 's/[Mm]*//gp')
[ -z "$min" ] && min=0
sec=$(echo $time | grep -o -e '[0-9]\+[Ss]\|^[0-9]\+$' | sed -n 's/[Ss]*//gp')
[ -z "$sec" ] && sec=0
time=$(echo "( $day * 3600 * 24 ) + ( $hour * 3600 ) + ( $min * 60 ) + $sec " | bc)

if [ -z "$no_disk" ]; then
    sys_disk=$(mount | grep 'on / ' | cut -d' ' -f1 | cut -d/ -f3 | sed 's/.$//')
    if [ -z "$disk_list" ]; then
        disk_list=$(lsblk | grep mmc -v | grep disk | awk '{print $1}')
        if [ -z "$no_mmc" ] && [ -n "$(lsblk | grep disk | grep $mmc_disk)" ]; then
            disk_list="${disk_list} ${mmc_disk}"
        fi
    else
        disk_list=$(echo $disk_list | sed -n 's/,/ /gp')
    fi

    extra_disk_list=""
    extra_disk_count=0
    for disk in $disk_list; do
        if [ "$disk" != "$sys_disk" ]; then
            extra_disk_list="${extra_disk_list}${disk} "
	    extra_disk_count=$(expr $extra_disk_count + 1)
        fi
    done

    echo System Disk: ${sys_disk}
    echo Other Disks: ${extra_disk_list}
    
   if [ "$extra_disk_count" -lt "$disk_count" ]; then
      echo "Detect: $extra_disk_count, Disk resource not enough"
      exit
   fi

    tmp_file="tmp_dd"
    file_id=1
    for disk in $disk_list; do
        mkdir -p /tmp/$disk
        if [ "$disk" != "$sys_disk" ]; then
            if [ -n "$(udevadm info /dev/$disk | grep DEVPATH | grep '/mmc')"  ]; then
                disk_part=$disk
            else
                if [ -z "$(parted -sm /dev/$disk print | grep '^1:')" ]; then
                    if [ -n "$(udevadm info /dev/$disk | grep DEVPATH | grep '/usb')" ]; then
                        parted /dev/$disk mklabel dos --script
                    else
                        parted /dev/$disk mklabel gpt --script
                    fi
                    parted /dev/$disk mkpart primary 0% 100% --script
                fi
                disk_part=${disk}1
            fi
            umount /dev/$disk_part 2> /dev/null
            fsck /dev/$disk_part -p
            mount /dev/$disk_part /tmp/$disk 2> /dev/null
            if [ $? -ne 0 ]; then
                if [ -n "$(udevadm info /dev/$disk | grep DEVPATH | grep '/usb')" ]; then
                    mkfs.vfat /dev/$disk_part
                else
                    mkfs.ext4 /dev/$disk_part -F
                fi
                mount /dev/$disk_part /tmp/$disk
                if [ $? -ne 0 ]; then
                    echo "Failed to mount /dev/$disk_part"
                    exit 1
                fi
            fi
        fi
        stress_disk_arg="${stress_disk_arg}-f /tmp/${disk}/${tmp_file}${file_id} "
        file_id=$(( file_id + 1 ))
    done
fi

if [ -z "$no_iperf" ]; then
    service network-manager stop 2> /dev/null
    iptables --flush -t nat

    if [ ! -z "$(echo $loopback_list | grep ,)" ]; then
        loopback_list=$(echo $loopback_list | sed -n 's/,/ /gp')
    fi

    for pair in $loopback_list;
    do
        iface1=$(echo $pair | cut -d: -f1)
        id1=$(grep -n "${iface1}:" /proc/net/dev | awk -F':' '{print $1}')
        iface2=$(echo $pair | cut -d: -f2)
        id2=$(grep -n "${iface2}:" /proc/net/dev | awk -F':' '{print $1}')
        for str in $iface1:$id1:$id2 $iface2:$id2:$id1;
        do
            iface=$(echo $str | awk -F':' '{print $1}')
            if_idx=$(echo $str | awk -F':' '{print $2}')
            peer_idx=$(echo $str | awk -F':' '{print $3}')
            if_ip=10.0.$if_idx.1
            snat_ip=10.1.$if_idx.1
            peer_ip=10.1.$peer_idx.1
            ifconfig $iface down
            ifconfig $iface hw ether 02:00:00:10:10:$if_idx
            ifconfig $iface $if_ip netmask 255.255.255.0 up
            iptables -t nat -A POSTROUTING -s $if_ip -d $peer_ip -j SNAT --to-source $snat_ip
            iptables -t nat -A PREROUTING -d $snat_ip -j DNAT --to-destination $if_ip
            route del $peer_ip 2> /dev/null
            ip route add $peer_ip dev $iface
            arp -i $iface -s $peer_ip 02:00:00:10:10:$peer_idx
            iperf_ip_list="${iperf_ip_list}${peer_ip} "
        done
    done

    if_count=0
    stat_rate_count=0
    for iface in $(echo $loopback_list | sed -n 's/[:,]/ /gp');
    do
        wait_iface_link_up $iface 10
        if [ "$wait_iface_link_up_ret" != "1" ]; then
            echo "error: $iface link down"
            exit 1
        fi
        if_name[if_count]=$iface
        if_rx_rate_sum[if_count]=0
        if_tx_rate_sum[if_count]=0
        if_rx_error[if_count]=$(cat /sys/class/net/$iface/statistics/rx_errors)
        if_tx_error[if_count]=$(cat /sys/class/net/$iface/statistics/tx_errors)
        if_no_link[if_count]=0
        if_count=$(( if_count + 1 ))
    done
fi

killall -9 iperf 2> /dev/null
killall stressapptest 2> /dev/null
trap 'killall stressapptest; killall -9 iperf; echo "Test is stopped by user"; exit 0' SIGINT

if [ -z "$no_iperf" ]; then
    iperf -s -D -w 512k
    iperf -s -D -u -w 512k
    iperf_count=0
    rm /tmp/*.iperf_res 2> /dev/null
    for ipaddr in $iperf_ip_list;
    do
        iperf -c $ipaddr -t 9999999 $iperf_arg > /tmp/$iperf_count.iperf_res &
        iperf_count=$(( iperf_count + 1 ))
    done
    sleep 1
fi

start_time=$(cat /proc/uptime | cut -d. -f1)
end_time=$(expr $start_time + $time)

if [ -z "$stress_mem_arg" ]; then
    stress_mem_arg="-M $(grep MemFree /proc/meminfo | awk '{ printf $2/1000 }' | cut -d. -f1)"
fi

#echo "stressapptest $stress_cpu_arg $stress_mem_arg $stress_disk_arg $stress_filesize_arg -s $time -v 4"
stressapptest $stress_cpu_arg $stress_mem_arg $stress_disk_arg $stress_filesize_arg -s $time -v 4 > /tmp/stress_res &

echo "Stress test running"
sleep 2
stress_running=1
while [ "$stress_running" != "0" ]
do
    show_stat
    stress_running=$(ps aux | grep stressapptest | grep -vc grep)
done

if [ -z "$no_disk" ]; then
    file_id=1
    for disk in $disk_list; do
        rm /tmp/${disk}/${tmp_file}${file_id}
        file_id=$(( file_id + 1 ))
    done
fi

echo "-------------------------------------------------------"
cat /tmp/stress_res

if [ -z "$no_iperf" ]; then
    pid_list=$(ps aux | grep 'iperf -c' | grep -v grep | awk '{printf $2" "}')
    for pid in $pid_list;
    do
        kill -9 $pid 2> /dev/null
    done

    iperf_running=1
    while [ "$iperf_running" != "0" ]
    do
        iperf_running=$(ps aux | grep 'iperf -c' | grep -vc grep)
        sleep 1
    done

    for (( i = 0; i < $if_count; i++));
    do
        result="[PASS]"
        average_rx_rate=$(echo "${if_rx_rate_sum[$i]} / $stat_rate_count" | bc)
        average_tx_rate=$(echo "${if_tx_rate_sum[$i]} / $stat_rate_count" | bc)
        if (( average_rx_rate < rate_criteria )) || (( average_tx_rate < rate_criteria )); then
            result="[FAIL]"
        fi
        if_tx_error[i]=$(expr $(cat /sys/class/net/${if_name[$i]}/statistics/tx_errors) - ${if_tx_error[i]})
        if_rx_error[i]=$(expr $(cat /sys/class/net/${if_name[$i]}/statistics/rx_errors) - ${if_rx_error[i]})
        if (( if_tx_error[i] > 0 )) || (( if_rx_error[i] > 0 )); then
            result="[FAIL]"
        fi
        if (( if_no_link[i] > 0 )); then
            result="[FAIL]"
        fi
        echo ${if_name[$i]} tx/rx rate $average_tx_rate/$average_rx_rate Mbps tx/rx error ${if_tx_error[i]}/${if_rx_error[i]} link failure ${if_no_link[i]} $result
    done
fi
