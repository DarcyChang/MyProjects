#!/bin/bash

i2cdetect -l | awk '{print $1}' > /tmp/i2c.tmp
#cat /tmp/i2c.tmp
bus=$(grep -c "i2c" /tmp/i2c.tmp)
echo $bus
