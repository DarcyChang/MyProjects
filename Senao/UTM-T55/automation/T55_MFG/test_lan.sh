#!/bin/bash

log="lan.log"

if [ "$1" == "1" ]; then
    ./iperf_test.sh -g -T 900 -V | tee $log
    sleep 3
    ./iperf_test.sh -g -u -T 800 -L 3 -r 1 -V | tee -a $log
    sleep 3
    ./iperf_test.sh -g -u -l 64 -b 30 -T 25 -L 3 -r 1 -V | tee -a $log
elif [ "$1" == "2" ]; then
    ./iperf_test.sh -T 900 -V | tee $log
    sleep 3
    ./iperf_test.sh -u -T 800 -L 3 -r 1 -V | tee -a $log
    sleep 3
    ./iperf_test.sh -u -l 64 -b 30 -T 25 -L 3 -r 1 -V | tee -a $log
else
    echo "usage: $0 1 or $0 2"
    exit
fi

echo "9. iperf test" >> result.log
if grep -q failed $log ; then
 echo " [FAIL] iperf test" >> result.log
else
 echo " [ OK ] iperf test" >> result.log
fi
    
