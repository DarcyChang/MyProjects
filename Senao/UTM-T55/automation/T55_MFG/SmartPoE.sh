#!/bin/bash
PD_Detection(){
        i2cget -y 0 0x20 0x0c > PP1
        echo Port 1 Value is : `cat PP1`
}

PD_Disable(){
        i2cset -f -y 0 0x20 0x19 0xf0
}

PD_Enable(){
        i2cset -f -y 0 0x20 0x14 0xff
}

if [[ $# == "0" ]]; then
    echo "./SmartPoE.sh -d  disable"
    echo "./SmartPoE.sh -e  enable"
    echo "./SmartPoE.sh -u  unplug"
    echo "./SmartPoE.sh -p  plug"
    exit 1
fi

while [[ $# > 0 ]]
do
key="$1"
case $key in
    -d|--disable)
    	PD_Disable
	PD_Detection
	if grep -q "0x0" PP1 
        then
                echo Smart PoE Function Disable Pass!!
        else
                echo Smart PoE Function Disable Fail!!
        fi
    ;;
    -e|--enable)
    	PD_Enable
	sleep 1
        PD_Detection
        if grep -q "0x44" PP1 
        then
                echo Smart PoE Function Enable Pass!!
        else
                echo Smart PoE Function Enable Fail!!
        fi
    ;;
    -u|--unplug)
	PD_Detection
        if grep -q "0x06" PP1 
        then
                echo PD Unplug Detection Test Pass!!
        else
                echo PD Unplug Detection Test Fail!!
        fi
    ;;
    -p|--plug)
    	PD_Detection
        if grep -q "0x44" PP1 
        then
                echo PD Plug Detection Test Pass!!
        else
                echo PD Plug Detection Test Fail!!
        fi
    ;;
    *)
    # unknown option
    ;;
esac
	shift # past argument or value
done

rm PP1 -rf

