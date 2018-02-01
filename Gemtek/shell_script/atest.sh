#!/bin/sh
while [ 1 ];
do
echo "r 0x0a" > /proc/bb_smbus_reg
rst=`cat /proc/bb_smbus_reg`
if [ $rst = x"65535" ]; then
cat /proc/bb_smbus_reg
exit;
elif [ $rst -gt 2000 ]; then
cat /proc/bb_smbus_reg
exit;
elif [ $rst -lt -2000 ]; then
cat /proc/bb_smbus_reg
exit;
fi
done
