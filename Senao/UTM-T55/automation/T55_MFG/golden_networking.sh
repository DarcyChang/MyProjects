#! /bin/bash


igb=$(ls /proc/driver/igb/)
link_state=$(cat /proc/driver/igb/$igb/test_mode | grep -c "DOWN")
if [ $link_state -gt 0 ] ; then
	echo "[ERROR] Golden sample's some ports link down." >> /root/automation/testresults-failure.txt
	cat /proc/driver/igb/$igb/test_mode | tee -a /root/automation/log.txt | tee -a /root/automation/testresults-failure.txt
fi



