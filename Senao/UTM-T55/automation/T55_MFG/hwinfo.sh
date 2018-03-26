#!/bin/bash

HOSTNAME=$(hostname)
if [ -f "/root/automation/T55_MFG/checkhw.sh" ]; then
    /root/automation/T55_MFG/checkhw.sh > /root/hwinfo.txt
    cat /root/hwinfo.txt

if grep -q 'CPU check ok' /root/hwinfo.txt &&
   grep -q 'Memory check ok' /root/hwinfo.txt &&
   grep -q 'Disk check ok' /root/hwinfo.txt &&
   grep -q 'Network check ok' /root/hwinfo.txt &&
   grep -q 'Wi-Fi check ok' /root/hwinfo.txt && 
   grep -q 'BIOS version 73.10' /root/hwinfo.txt &&
   [ "$HOSTNAME" == "T55-wifi" ];
then
    echo Check Hardware Information Pass!!
elif grep -q 'CPU check ok' /root/hwinfo.txt &&
     grep -q 'Memory check ok' /root/hwinfo.txt &&
     grep -q 'Disk check ok' /root/hwinfo.txt &&
     grep -q 'Network check ok' /root/hwinfo.txt &&
     grep -q 'BIOS version 73.10' /root/hwinfo.txt
then 
    echo Check Hardware Information Pass!!    
else 
    echo Check Hardware Information Fail!!
fi
rm /root/hwinfo.txt
else
    echo "checkhw.sh file missed"
fi
