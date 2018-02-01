#!/bin/sh

lsusb | grep 'Huawei' | cut -d ' ' -f6 | cut -d ':' -f2
huawei=$(lsusb | grep 'Huawei' | cut -d ' ' -f6 | cut -d ':' -f2)
echo $huawei   
