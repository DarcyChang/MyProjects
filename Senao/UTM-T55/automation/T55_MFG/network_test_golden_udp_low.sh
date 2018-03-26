#! /bin/bash

sleep 2
/root/automation/T55_MFG/iperf_test.sh -g -u -l 64 -b 30 -T 25 -L 3 -r 1 -f
