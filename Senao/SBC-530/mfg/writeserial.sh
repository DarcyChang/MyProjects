#!/bin/bash

if (($# < 1)); then
        echo "please input serial number"
        echo "usage: $0 {serial number}"
        exit 1
fi

SERIAL=$1

bios_tools/h2osde-lx64 -BS $SERIAL > /dev/null

value=$(bios_tools/h2osde-lx64 -BS | grep 0x07 | cut -d' ' -f7 | cut -d'"' -f2)
echo "Write to BIOS: $SERIAL"
echo "Read from BIOS: $value"
if [ "$value" == "$SERIAL" ]; then
    echo "write serial number ok"
else
    echo "write serial number fail"
fi
