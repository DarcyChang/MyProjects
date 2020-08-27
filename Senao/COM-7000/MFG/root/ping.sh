#!/bin/bash

INDEX=0
eth1_loss_num=0
eth2_loss_num=0
eth3_loss_num=0
eth4_loss_num=0

eth1_log_path=/root/log_folder/eth1.log
eth2_log_path=/root/log_folder/eth2.log
eth3_log_path=/root/log_folder/eth3.log
eth4_log_path=/root/log_folder/eth4.log

eth1_tmp_path=/root/log_folder/eth1_tmp.log
eth2_tmp_path=/root/log_folder/eth2_tmp.log
eth3_tmp_path=/root/log_folder/eth3_tmp.log
eth4_tmp_path=/root/log_folder/eth4_tmp.log
log_path=/root/log.txt

log_backup_path=/root/backup


function backup(){
	mkdir -p /root/log_folder
    if [ ! -d "$log_backup_path" ]; then
        echo "[SENAO] Directory $log_backup_path does not exists. Creating it."
        mkdir -p $log_backup_path
    fi

    dir=$(date +%Y%m%d%H%M%S)
    mkdir $log_backup_path/$dir
    mv $eth1_log_path $log_backup_path/$dir 2> /dev/null
    mv $eth2_log_path $log_backup_path/$dir 2> /dev/null
    mv $eth3_log_path $log_backup_path/$dir 2> /dev/null
    mv $eth4_log_path $log_backup_path/$dir 2> /dev/null
	mv $log_path $log_backup_path/$dir 2> /dev/null
}

backup
./set_ip.sh

while [ 1 ]
do
#	ping -I eth1 10.1.4.1 -c1 | tee -a $eth1_log_path | tee $eth1_tmp_path 
#	ping -I eth2 10.1.3.1 -c1 | tee -a $eth2_log_path | tee $eth2_tmp_path 
#	ping -I eth3 10.1.6.1 -c1 | tee -a $eth3_log_path | tee $eth3_tmp_path
#	ping -I eth4 10.1.5.1 -c1 | tee -a $eth4_log_path | tee $eth4_tmp_path
	ping -I eth1 10.1.4.1 -c1 > $eth1_tmp_path 
	ping -I eth2 10.1.3.1 -c1 > $eth2_tmp_path 
	ping -I eth3 10.1.6.1 -c1 > $eth3_tmp_path
	ping -I eth4 10.1.5.1 -c1 > $eth4_tmp_path
	cat $eth1_tmp_path >> $eth1_log_path
	cat $eth2_tmp_path >> $eth2_log_path
	cat $eth3_tmp_path >> $eth3_log_path
	cat $eth4_tmp_path >> $eth4_log_path

	eth1_received=$(grep -c "1 received" $eth1_tmp_path)
	eth2_received=$(grep -c "1 received" $eth2_tmp_path)
	eth3_received=$(grep -c "1 received" $eth3_tmp_path)
	eth4_received=$(grep -c "1 received" $eth4_tmp_path)

#	echo "[DEBUG] eth1_received=$eth1_received, eth2_received=$eth2_received, eth3_received=$eth3_received, eth4_received=$eth4_received"

	if [ $eth1_received == "0" ] ; then
		(( eth1_loss_num++ ))
	fi
	if [ $eth2_received == "0" ] ; then
		(( eth2_loss_num++ ))
	fi
	if [ $eth3_received == "0" ] ; then
		(( eth3_loss_num++ ))
	fi
	if [ $eth4_received == "0" ] ; then
		(( eth4_loss_num++ ))
	fi

#	echo "[DEBUG] eth1_loss_num=$eth1_loss_num, eth2_loss_num=$eth2_loss_num, eth3_loss_num=$eth3_loss_num, eth4_loss_num=$eth4_loss_num"

	(( INDEX++ ))
	eth1_loss_rate=`awk 'BEGIN{printf "%.1f%%\n",('$eth1_loss_num'/'$INDEX')*100}'`
	eth2_loss_rate=`awk 'BEGIN{printf "%.1f%%\n",('$eth2_loss_num'/'$INDEX')*100}'`
	eth3_loss_rate=`awk 'BEGIN{printf "%.1f%%\n",('$eth3_loss_num'/'$INDEX')*100}'`
	eth4_loss_rate=`awk 'BEGIN{printf "%.1f%%\n",('$eth4_loss_num'/'$INDEX')*100}'`
	echo "[$INDEX Round, $(date +%Y-%m-%d_%H:%M:%S)] eth1 packet loss rate=$eth1_loss_num|$eth1_loss_rate, eth2 packet loss rate=$eth2_loss_num|$eth2_loss_rate, eth3 packet loss rate=$eth3_loss_num|$eth3_loss_rate, eth4 packet loss rate=$eth4_loss_num|$eth4_loss_rate" | tee -a $log_path
done
echo "ping test stop"
