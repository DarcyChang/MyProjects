#!/bin/bash
/root/automation/T55_MFG/superIO > /root/showIO
cat /root/showIO | tee -a /root/automation/log.txt
Pass_count=$(grep -c "pass" /root/showIO)
if [ "$Pass_count" == "7" ];
then
	echo "HW monitor Test Pass!!" | tee -a /root/automation/log.txt
	echo "HW_MONITOR_TEST: PASS" >> /root/automation/test_results.txt
else 
	echo "HW monitor Test Fail!!" | tee -a /root/automation/log.txt
	echo "HW_MONITOR_TEST: FAIL" >> /root/automation/test_results.txt
fi

rm /root/showIO
exit 0
