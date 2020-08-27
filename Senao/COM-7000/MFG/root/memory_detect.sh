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

	echo "Memory detect: PASS"
}

memory_test
