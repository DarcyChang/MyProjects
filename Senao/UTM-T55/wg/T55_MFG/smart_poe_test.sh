#!/bin/bash                                                                                                                                                              

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

echo "*******************************************************************************"
echo "Smart POE Test start...."
echo "*******************************************************************************"
echo ""
echo "Please do not connect any PD fixture into LAN port 4."
echo "When you are ready, press any key to continue..."
read
/root/automation/T55_MFG/SmartPoE.sh -u
status1=$(/root/automation/T55_MFG/SmartPoE.sh -u | grep PD | cut -d " " -f 5)
echo $status1

echo ""
echo "Please connect PD fixture into LAN port 4."
echo "When you are ready, press any key to continue..."
read
/root/automation/T55_MFG/SmartPoE.sh -p
status2=$(/root/automation/T55_MFG/SmartPoE.sh -p | grep PD | cut -d " " -f 5)
echo $status2

/root/automation/T55_MFG/SmartPoE.sh -d
status3=$(/root/automation/T55_MFG/SmartPoE.sh -d | grep Smart | cut -d " " -f 5)
echo $status3

/root/automation/T55_MFG/SmartPoE.sh -e
status4=$(/root/automation/T55_MFG/SmartPoE.sh -e | grep Smart | cut -d " " -f 5)
echo $status4

if [ "$status1" == "Pass!!" ] && [ "$status2" == "Pass!!" ] && [ "$status3" == "Pass!!" ] && [ "$status4" == "Pass!!" ]; then
    echo "SMART_POE_TEST: PASS" >> $test_result_path
else
    echo "SMART_POE_TEST: FAIL" >> $test_result_path
fi

