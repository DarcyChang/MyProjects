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
echo "POE TEST WITH POWER LOADING start...."
echo "*******************************************************************************"
echo ""
./T55_MFG/poe > /root/PLoadResult
cat /root/PLoadResult

P1V=$(cat /root/PLoadResult | grep "Port1 Voltage" | cut -d':' -f 2 | cut -d' ' --f 1)
P1C=$(cat /root/PLoadResult | grep "Port1 Current" | cut -d':' -f 2 | cut -d' ' --f 1)
P1W=$(cat /root/PLoadResult | grep "Port1 Watt" | cut -d':' -f 2 | cut -d'.' -f 1)

echo ""
echo "Please input following parameter value:"
echo ""
echo "Voltage minimum integer value( <= P1V):"
read parameter1
echo "Voltage maximum integer value( >  P1V):"
read parameter2
echo "Current minimum integer value( <= P1C):"
read parameter3
echo "Watt minimum integer value( <= P1W):"
read parameter4

if [ $P1V -ge $parameter1 ] && [ $P1V -le $parameter2 ] && [ $P1C -ge $parameter3 ] && [ $P1W -ge $parameter4 ]; then
    echo Power Load Test Pass!!
    echo "POE_TEST_WITH_POWER_LOADING: PASS" >> $test_result_path
else
    echo Power Load Test Fail!!
    echo "POE_TEST_WITH_POWER_LOADING: FAIL" >> $test_result_path
fi

#rm /root/PLoadResult
exit 0

