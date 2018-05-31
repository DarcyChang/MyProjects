#!/bin/bash

source /root/automation/Library/path.sh

/root/automation/T55_MFG/superIO > /root/showIO
cat /root/showIO | tee -a $log_path
Pass_count=$(grep -c "pass" /root/showIO)
if [ "$Pass_count" == "7" ];
then
	echo "HW monitor Test Pass!!" | tee -a $log_path
	echo "HW_MONITOR_TEST: PASS" >> $test_result_path
else 
	echo "HW monitor Test Fail!!" | tee -a $log_path
	echo "HW_MONITOR_TEST: FAIL" >> $test_result_path
fi

rm /root/showIO
exit 0
