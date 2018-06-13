#!/bin/bash 

killall -9 iperf &> /dev/null                                                                                                                                            
iperf -s -w 512k -l 64k -D &> /dev/null
iperf -s -u -D &> /dev/null

