#!/bin/bash

function memory_test {
        mem_speed=$(dmidecode -t 17 | grep "Configured Clock Speed: 2133 MHz" | wc -l)
        mem_type=$(dmidecode -t 17 | grep "Type: DDR4" | wc -l)
        mem_size=$(dmidecode -t 17 | grep "Size: 8192 MB" | wc -l)

	if [[ $mem_speed != 2 ]] || [[ $mem_type != 2 ]] || [[ $mem_size != 2 ]] ; then
                dmidecode -t 17
                echo "[ERROR] Memory information ERROR"
                exit
        fi

	free_memory=$(free -m | grep Mem | awk '{print $4}')
	echo "[DEBUG] free memory $free_memory MB"
	memtester 14000 1 | tee /tmp/mem_test.log
	failure_count=$(grep -c "FAILURE" /tmp/mem_test.log)
	if [ "$failure_count" != "0" ]; then
		echo "[ERROR] Memory stress test fail."
		exit
	fi
}

memory_test
