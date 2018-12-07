#!/bin/bash

eeupdate64e > /tmp/nic_info
nic_count=$(grep '8086-15' -c /tmp/nic_info)
if (( nic_count != 2 )); then
    echo "FAIL: Could not detect NIC from PCI bus"
    exit 1
fi

for (( i = 1; i <= nic_count; i++ ))
do
    echo "Clean NIC$i EEPROM.."
    eeupdate64e /NIC=$i /FORCE /D=/root/SBC-1100/i210_eeprom/empty.bin
    eeupdate64e /NIC=$i /FORCE /D=/root/SBC-1100/i210_eeprom/empty.EEP
done
echo "Done"
