#!/bin/sh
while [ 1 ];
do
echo "r 0x0d" > /proc/bb_smbus_reg
rst=`cat /proc/bb_smbus_reg`
if [ x$rst = x"0" ]; then
cat /proc/bb_smbus_reg
cat /proc/bb_smbus_battery_connected
exit;
elif [ x$rst = x"255" ]; then
cat /proc/bb_smbus_reg
cat /proc/bb_smbus_battery_connected
exit;
elif [ x$rst = x"65535" ]; then
cat /proc/bb_smbus_reg
cat /proc/bb_smbus_battery_connected
exit;
fi
done
