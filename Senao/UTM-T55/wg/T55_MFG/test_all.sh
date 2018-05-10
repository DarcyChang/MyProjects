#!/bin/bash

PWD=$(pwd)
log="test1.log"
test_result="result.log"

echo 1. Information Check | tee $test_result
$PWD/hwinfo.sh > $log
if grep -q 'Check Hardware Information Pass!!' $log ; then 
    printf "\E[0;32;40m"
    echo " [ OK ] Information Check" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] Information Check" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 2. RTC and Battery Test | tee -a $test_result
RTC_detect=$($PWD/testRtc.sh check)
if [ "$RTC_detect" == "pass" ]; then 
    printf "\E[0;32;40m"
    echo " [ OK ] RTC and Battery Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] RTC and Battery Test" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 3. TPM Test | tee -a $test_result
tpm_selftest -l info >> $log
if grep -q 'tpm_selftest succeeded' $log ; then
    printf "\E[0;32;40m"
    echo " [ OK ] TPM Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] TPM Test" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 4. HW monitor Test | tee -a $test_result
$PWD/superIO.sh >> $log
if grep -q 'HW monitor Test Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] HW monitor Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] HW monitor Test" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 5. ID EEPROM Test | tee -a $test_result
$PWD/EEPROM_ID_Test.sh >> $log
if grep -q 'EEPROM ID Test Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] ID EEPROM Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] ID EEPROM Test" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 6. Reset Button Test | tee -a $test_result
echo 397 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio397/direction
printf "\E[0;33;40m"
button_detect=$(cat /sys/class/gpio/gpio397/value)
i=0
if [ "$button_detect" == "1" ]; then
    while [ "$button_detect" == "1" ]
    do
     
    button_detect=$(cat /sys/class/gpio/gpio397/value)
    sleep 0.001
    i=$(expr $i + 1)
    if [ "$i" -gt "3000" ]; then
	printf "\E[0;31;40m"
        echo " [FAIL] Reset Button Test" | tee -a $test_result
	break;	
    fi
    done
    while [ "$button_detect" == "0" ]
    do
    button_detect=$(cat /sys/class/gpio/gpio397/value)
    sleep 0.001
    i=$(expr $i + 1)
    if [ "$i" -gt "4000" ]; then
        printf "\E[0;31;40m" 
        echo " [FAIL] Reset Button Test" | tee -a $test_result
        break;
    fi
    done
fi
    if [ "$i" -lt "3000" ]; then
        printf "\E[0;32;40m"
        echo " [ OK ] Reset Button Test" | tee -a $test_result
    fi
echo 397 > /sys/class/gpio/unexport


printf "\E[0;37;40m"
echo 7. System LEDs Test | tee -a $test_result
printf "\E[0;33;40m"
$PWD/SysLEDTest.sh
printf "\E[0;36;40m"
read -p 'Is System LEDs Test OK? (y/n) ' ps
if [ "$ps" == "y" ] || [ "$ps" == "Y" ]; then
    printf "\E[0;32;40m"
    echo " [ OK ] System LEDs Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] System LEDs Test" | tee -a $test_result
fi


printf "\E[0;37;40m"
echo 8. LAN speed LED check | tee -a $test_result
printf "\E[0;33;40m"
read -p 'Please ensure all LAN ports have connection!!' ps
$PWD/LanLEDTest.sh
printf "\E[0;36;40m"
read -p 'Is System LEDs Test OK? (y/n) ' ps
if [ "$ps" == "y" ] || [ "$ps" == "Y" ]; then
    printf "\E[0;32;40m"
    echo " [ OK ] LAN speed LED check" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] LAN speed LED check" | tee -a $test_result
fi

printf "\E[0;37;40m"

