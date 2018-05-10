#! /bin/bash

echo "MEMORY_TEST: FAIL: Not terminated normally." >> /root/automation/test_results.txt

free_memory=$(free -m | grep Mem | awk '{print $4}')
#echo "[DEBUG] $free_memory"
echo "Memory test start..." | tee -a /root/automation/log.txt 
echo "This could take 4 hours, so wait for it." | tee -a /root/automation/log.txt 
time memtester $free_memory 20 | tee -a /root/automation/log.txt | tee -a /root/automation/memory_stress_test.txt
# Test 20 times will take 4 hours.

failure_count=$(grep -c "FAILURE" /root/automation/memory_stress_test.txt)
#echo "[DEBUG] FAILURE number $failure_count"
sed -i '$d' /root/automation/test_results.txt
if [ "$failure_count" == "0" ]; then
	echo "MEMORY_TEST: PASS" >> /root/automation/test_results.txt
else
	echo "MEMORY_TEST: FAIL" >> /root/automation/test_results.txt
fi
