#!/bin/bash

for (( i = 0; i < 10; i ++)); do
    Driver_Path="/proc/driver/igb/0000:0$i:00.0/test_mode"
    if [ -f "$Driver_Path" ]; then
        break
    fi
done

read -p "1. press enter to set LAN Port LED at 100Mbps" ps
echo "sset 100f" > $Driver_Path
sleep 3

read -p "2. press enter to set LAN Port LED at 1000Mbps" ps
echo "sset 1000f" > $Driver_Path
sleep 3

read -p "3. press enter to set LAN Port LED at 10Mbps" ps
echo "sset 10f" > $Driver_Path
sleep 3

read -p "LAN port LED Test finish, press enter to set back to 1000Mbps!!"
echo "sset 1000f" > $Driver_Path
