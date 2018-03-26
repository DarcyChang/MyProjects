#!/bin/bash

PWD=$(pwd)
log="test1.log"
test_result="result.log"

printf "\E[0;37;40m"
echo 10. Smart POE Test | tee -a $test_result
$PWD/SmartPoE.sh -u >> $log

printf "\E[0;33;40m"
read -p "Plug PD device in port 4" ps
$PWD/SmartPoE.sh -p >> $log

if grep -q 'PD Unplug Detection Test Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] PD Unplug Detection Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] PD Unplug Detection Test" | tee -a $test_result
fi

if grep -q 'PD Plug Detection Test Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] PD Plug Detection Test" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] PD Plug Detection Test" | tee -a $test_result
fi

$PWD/SmartPoE.sh -d >> $log
if grep -q 'Smart PoE Function Disable Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] Smart PoE Function Disable" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] Smart PoE Function Disable" | tee -a $test_result
fi
sleep 3

$PWD/SmartPoE.sh -e >> $log
if grep -q 'Smart PoE Function Enable Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] Smart PoE Function Enable" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] Smart PoE Function Enable" | tee -a $test_result
fi

printf "\E[0;37;40m"
echo 11. POE Test with power loading | tee -a $test_result
$PWD/PLoadCheck.sh 0 999 0 29 >> $log
printf "\E[0;33;40m"
read -p "Plug PD fixture in port 4 and Enable Power Load to Class4 and 30W" ps
if grep -q 'Power Load Test Pass!!' $log; then
    printf "\E[0;32;40m"
    echo " [ OK ] POE Test with power loading" | tee -a $test_result
else
    printf "\E[0;31;40m"
    echo " [FAIL] POE Test with power loading" | tee -a $test_result
fi

printf "\E[0;37;40m"
