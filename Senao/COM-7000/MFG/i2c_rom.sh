#!/bin/bash
#Objective: Write Project Model name and SN into EEPROM 0x56.
#Author:Darcy Chang
#Date:2018/11/29


function clean_rom(){
	i2cset -y $rom_bus 0x56 0x00 0x00
	i2cset -y $rom_bus 0x56 0x01 0x00
	i2cset -y $rom_bus 0x56 0x02 0x00
	i2cset -y $rom_bus 0x56 0x03 0x00
	i2cset -y $rom_bus 0x56 0x04 0x00
	i2cset -y $rom_bus 0x56 0x05 0x00
	i2cset -y $rom_bus 0x56 0x06 0x00
	i2cset -y $rom_bus 0x56 0x07 0x00
	i2cset -y $rom_bus 0x56 0x08 0x00
	i2cset -y $rom_bus 0x56 0x09 0x00
	i2cset -y $rom_bus 0x56 0x0a 0x00
	i2cset -y $rom_bus 0x56 0x0b 0x00
	i2cset -y $rom_bus 0x56 0x0c 0x00
	i2cset -y $rom_bus 0x56 0x0d 0x00
	i2cset -y $rom_bus 0x56 0x0e 0x00
	i2cset -y $rom_bus 0x56 0x0f 0x00

	i2cset -y $rom_bus 0x56 0x10 0x00
	i2cset -y $rom_bus 0x56 0x11 0x00
	i2cset -y $rom_bus 0x56 0x12 0x00
	i2cset -y $rom_bus 0x56 0x13 0x00
	i2cset -y $rom_bus 0x56 0x14 0x00
	i2cset -y $rom_bus 0x56 0x15 0x00
	i2cset -y $rom_bus 0x56 0x16 0x00
	i2cset -y $rom_bus 0x56 0x17 0x00
	i2cset -y $rom_bus 0x56 0x18 0x00
	i2cset -y $rom_bus 0x56 0x19 0x00
	i2cset -y $rom_bus 0x56 0x1a 0x00
	i2cset -y $rom_bus 0x56 0x1b 0x00
	i2cset -y $rom_bus 0x56 0x1c 0x00
	i2cset -y $rom_bus 0x56 0x1d 0x00
	i2cset -y $rom_bus 0x56 0x1e 0x00
	i2cset -y $rom_bus 0x56 0x1f 0x00
}


function write_model_to_rom(){
	echo "[DEBUG] func $1 $2 $3 $4 $5 $6 $7 $8"

	i2cset -y $rom_bus 0x56 0x00 0x$2
	i2cset -y $rom_bus 0x56 0x01 0x$3
	i2cset -y $rom_bus 0x56 0x02 0x$4
	i2cset -y $rom_bus 0x56 0x03 0x$5
	i2cset -y $rom_bus 0x56 0x04 0x$6
	i2cset -y $rom_bus 0x56 0x05 0x$7
	i2cset -y $rom_bus 0x56 0x06 0x$8
}

function write_sn_to_rom(){
	echo "[DEBUG] $1 $2 $3 $4 $5 $6 $7 $8 $9"

	i2cset -y $rom_bus 0x56 0x10 0x$2
	i2cset -y $rom_bus 0x56 0x11 0x$3
	i2cset -y $rom_bus 0x56 0x12 0x$4
	i2cset -y $rom_bus 0x56 0x13 0x$5
	i2cset -y $rom_bus 0x56 0x14 0x$6
	i2cset -y $rom_bus 0x56 0x15 0x$7
	i2cset -y $rom_bus 0x56 0x16 0x$8
	i2cset -y $rom_bus 0x56 0x17 0x$9
}


bus_num=$(/root/i2c_bus.sh)
if [ "$bus_num" == 2 ] ; then
        rom_bus=1
elif [ "$bus_num" == 14 ] ; then
        rom_bus=13
else
	echo "[DEBUG] ROM IIC BUS $rom_bus"
	i2cdetect -l
fi


if [ $# -le 0 ] ; then
	echo ""
	echo "Usage:"
	echo "Clean - i2c_rom c"
	echo "Read - i2c_rom r"
	echo "Write Model Name - i2c_rom wm 11 22 33 44 55 66 77"
	echo "Write Serial Number - i2c_rom ws 11 22 33 44 55 66 77 88"
	exit
fi


echo "[DEBUG] $# $1 $2 $3 $4 $5 $6 $7 $8 $9"
echo "[DEBUG] ROM IIC BUS $rom_bus"


if [ $1 == "wm" ] ; then
	write_model_to_rom $rom_bus $2 $3 $4 $5 $6 $7 $8
elif [ $1 == "ws" ] ; then
	write_sn_to_rom $rom_bus $2 $3 $4 $5 $6 $7 $8 $9
elif [ $1 == "c" ] ; then 
	clean_rom $rom_bus
elif [ $1 == "r" ] ; then 
	i2cdump -y $rom_bus 0x56
else
	echo "[ERROR] Wrong command"
	echo ""
	echo "Usage:"
	echo "Clean - i2c_rom c"
	echo "Read - i2c_rom r"
	echo "Write Model Name - i2c_rom wm 11 22 33 44 55 66 77"
	echo "Write Serial Number - i2c_rom ws 11 22 33 44 55 66 77 88"
fi
