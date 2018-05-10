#!/bin/sh

echo 397 > /sys/class/gpio/export
echo in > /sys/class/gpio/gpio397/direction
watch -n 0.1 "cat /sys/class/gpio/gpio397/value"
