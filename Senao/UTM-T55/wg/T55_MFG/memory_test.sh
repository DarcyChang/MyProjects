#! /bin/bash

source /root/automation/Library/path.sh

echo "MEMORY_TEST: FAIL: Not terminated normally." >> $test_result_path

free_memory=$(free -m | grep Mem | awk '{print $4}')
memory_loop=$(cat /root/automation/config | grep "Memory Test loop number" | awk '{print $5}')
#echo "[DEBUG] free memory : $free_memory , memory test loop : $memory_loop"
echo "Memory test start..." | tee -a $log_path
echo "This could take 4 hours, so wait for it." | tee -a $log_path
time memtester $free_memory $memory_loop | tee -a $log_path | tee -a $memory_stress_test_path
# Test 20 times will take 4 hours.

failure_count=$(grep -c "FAILURE" $memory_stress_test_path)
#echo "[DEBUG] FAILURE number $failure_count"
sed -i '$d' $test_result_path
if [ "$failure_count" == "0" ]; then
	echo "MEMORY_TEST: PASS" >> $test_result_path
else
	echo "MEMORY_TEST: FAIL" >> $test_result_path
fi
