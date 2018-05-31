#! /bin/bash

source /root/automation/Library/path.sh

/root/automation/T55_MFG/testRtc.sh set | tee -a $log_path
sleep 2
/root/automation/T55_MFG/testRtc.sh check | tee -a $log_path | tee $tmp_path

rtc=$( cat $tmp_path)
if [[ $rtc == "pass" ]] ; then                                                                                                                                       
	echo "RTC_TEST: PASS" >> $test_result_path
else
	echo "RTC_TEST: FAIL" >> $test_result_path
fi
