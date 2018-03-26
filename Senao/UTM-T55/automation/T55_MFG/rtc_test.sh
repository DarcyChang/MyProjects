#! /bin/bash

/root/automation/T55_MFG/testRtc.sh set | tee -a /root/automation/log.txt
/root/automation/T55_MFG/testRtc.sh check | tee -a /root/automation/log.txt | tee /tmp/log_tmp.txt

rtc=$( cat /tmp/log_tmp.txt)
if [[ $rtc == "pass" ]] ; then                                                                                                                                       
	echo "RTC_TEST: PASS" >> /root/automation/test_results.txt
else
	echo "RTC_TEST: FAIL" >> /root/automation/test_results.txt
fi
