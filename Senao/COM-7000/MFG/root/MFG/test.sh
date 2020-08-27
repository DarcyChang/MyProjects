#!/bin/bash
# 16 <-> 10 
# AND OR

echo_led=ef
sys_led=df
bi_led=bf
eth_led=7f

value=$(i2cget -y 0 0x21 0x03 | awk -F "x" '{print $2}' )

echo "value $value  $((16#$value))"

tmp=$(( $((16#$value)) & $((16#$sys_led)) ))
echo "tmp $tmp"

tmp=$(echo "obase=16;$tmp"|bc)
echo "tmp $tmp"

i2cset -y 0 0x21 0x03 0x$tmp
