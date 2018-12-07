#!/bin/bash

test_list="ttyS3 ttyS2 ttyS1"

while [[ $# > 0 ]]
do
    key=$1
    case $key in
    --list)
    test_list=$2
    shift
    ;;
    *)
    echo "unknown option '$key'"
    ;;
    esac
    shift
done

for dev in $test_list
do
./RS232-selftest -e -p /dev/${dev} -b 115200 -o 5 -i 7 > ${dev} &
done

echo "Now test"
sleep 10

for dev in $test_list
do
rx=$(cat ${dev} | grep "session" | awk '{print $6}' | awk -F'=' '{print $2}')
tx=$(cat ${dev} | grep "session" | awk '{print $7}' | awk -F'=' '{print $2}')
err=$(cat ${dev} | grep "session" | awk '{print $9}' | awk -F'=' '{print $2}')
pincheck=$(./RS232-pincheck /dev/${dev} | grep FAILED)
if [ "$rx" == "$tx" ] && [ "$err" == "0" ] && [ -z "$pincheck" ]; then
    echo "${dev} PASS"
else
    echo "${dev} FAILED"
    echo "  ${dev} - rx: $rx  tx: $tx  err: $err"
    echo "  ${dev} - $(./RS232-pincheck /dev/${dev} | grep FAILED | sed -n '1p') , $(./RS232-pincheck /dev/${dev} | grep FAILED | sed -n '2p')"
fi
rm $dev
done


