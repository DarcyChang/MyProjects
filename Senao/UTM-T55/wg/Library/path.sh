#!/bin/bash

test_result_path=$(cat /root/automation/config | grep "test_result_path" | awk '{print $2}')
test_result_failure_path=$(cat /root/automation/config | grep "test_result_failure_path" | awk '{print $2}')
all_test_done_path=$(cat /root/automation/config | grep "all_test_done_path" | awk '{print $2}')
memory_stress_test_path=$(cat /root/automation/config | grep "memory_stress_test_path" | awk '{print $2}')
log_backup_path=$(cat /root/automation/config | grep "log_backup_path" | awk '{print $2}')
log_path=$(cat /root/automation/config | grep "log_path" | awk '{print $2}')
time_path=$(cat /root/automation/config | grep "time_path" | awk '{print $2}')
tmp_path=$(cat /root/automation/config | grep "tmp_path" | awk '{print $2}')
tmp_golden_path=$(cat /root/automation/config | grep "tmp_golden_path" | awk '{print $2}')
