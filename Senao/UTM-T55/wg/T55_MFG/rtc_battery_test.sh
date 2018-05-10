#! /bin/bash

rtc_reboot_flag="/root/automation/RTC_REBOOT"

echo "*******************************************************************************"
echo "RTC and Battery test start...."
echo "*******************************************************************************"
echo ""

if [ -f $rtc_reboot_flag ];then
    echo "Reboot done..."
    /root/automation/T55_MFG/testRtc.sh check
    rtc=$(/root/automation/T55_MFG/testRtc.sh check)
    if [[ $rtc == "pass" ]] ; then                                                                                                                                       
        echo "RTC_AND_BATTERY_TEST: PASS" >> /root/automation/test_results.txt
    else
        echo "RTC_AND_BATTERY_TEST: FAIL" >> /root/automation/test_results.txt
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
