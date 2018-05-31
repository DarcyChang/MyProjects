#! /bin/bash

source /root/automation/Library/path.sh

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
