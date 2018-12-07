#!/bin/bash

eeupdate64e > /tmp/nic_info
nic_count=$(grep '8086-' -c /tmp/nic_info)
if (( nic_count != 2 )); then
    echo "FAIL: Could not detect NIC from PCI bus"
    exit 1
fi

poweroff=0
for (( i = 1; i <= nic_count; i++ ))
do
    if [ "$(grep "^  $i " /tmp/nic_info | grep 'I210 Gigabit Network Connection' -c)" == "0" ]; then
        echo "Update NIC$i EEPROM.."
        eeupdate64e /NIC=$i /D=/root/SBC-1100/i210_eeprom/$i.bin 1> /dev/null
        eeupdate64e /NIC=$i /D=/root/SBC-1100/i210_eeprom/$i.EEP 1> /dev/null
        poweroff=1
    fi
done

if (( poweroff == 1 )); then
    echo "PASS: EEPROMs are updated and need power cycle to take effect"
    init 0
else
    echo "PASS: EEPROMs are ready"
fi
