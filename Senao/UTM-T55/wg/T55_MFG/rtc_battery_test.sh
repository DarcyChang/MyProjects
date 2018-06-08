#! /bin/bash

#source /root/automation/Library/path.sh
test_result_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/T55_MFG/mfg_version | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/T55_MFG/mfg_version | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/T55_MFG/mfg_version | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/T55_MFG/mfg_version | grep "log_path" | awk '{print $2}')
time_path=$(cat /root/automation/T55_MFG/mfg_version | grep "time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/T55_MFG/mfg_version | grep "tmp_golden_path" | awk '{print $2}')   

rtc_reboot_flag="/etc/wg/log/diag/RTC_REBOOT"

echo "*******************************************************************************"
echo "RTC and Battery test start...."
echo "*******************************************************************************"
echo ""

if [ -f $rtc_reboot_flag ];then
    echo "Reboot done..."
    /root/automation/T55_MFG/testRtc.sh check
    rtc=$(/root/automation/T55_MFG/testRtc.sh check)
    if [[ $rtc == "pass" ]] ; then                                                                                                                                       
        echo "RTC_AND_BATTERY_TEST: PASS" >> $test_result_path
    else
        echo "RTC_AND_BATTERY_TEST: FAIL" >> $test_result_path
    fi
else
    echo "After DUT shutdown, please plug out power cord and wait 5 seconds at the least."
    echo ""
    echo "Press any key to continue..." 
    read
    /root/automation/T55_MFG/testRtc.sh set
    date > $rtc_reboot_flag
    init 0
fi
