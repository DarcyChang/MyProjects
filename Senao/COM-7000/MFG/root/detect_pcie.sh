#!/bin/bash

lspci | tee /tmp/log.txt
#realtek=$(grep -c "Realtek Semiconductor" /tmp/log.txt)
cavium=$(grep -c "Cavium" /tmp/log.txt)
#reboot_times=$(cat /root/reboot_times)
cavium_fail=$(cat /root/cavium_fail)

echo ""
#echo "Boot $reboot_times times"
#if [ "$reboot_times" != "2" ]; then
#	(( reboot_times++ ))
#	echo "$reboot_times" > /root/reboot_times
#else
#	exit
#fi
#if [ "$realtek" == "2" ]; then
#	echo [PASS] Detect realtek PASS.
#	lspci | grep "Realtek Semiconductor"
#else
#	echo "[FAIL] Detect realtek number is $realtek"
#	lspci | grep "Realtek Semiconductor"
#fi

if [ "$cavium" == "1" ]; then
	echo [PASS] Detect cavium PASS.
	lspci | grep "Cavium"
else
	(( cavium_fail++ ))
	echo "$cavium_fail" > /root/cavium_fail
	echo "[FAIL] Detect cavium fail number is $cavium_fail times"
	lspci | grep "Cavium"
fi
echo ""
#echo "[SENAO] Rebooting..."
#sleep 5
#reboot
