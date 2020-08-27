#!/bin/bash

/root/pre_test.sh
/root/ethernet_test.sh
/root/stress.sh -t 3600
/root/memory_stress.sh
/root/memory_detect.sh
