#!/bin/sh

echo -e "ate0\r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cpin=\"8888\"\r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cops=2 \r\n"> /dev/ttyACM2
sleep 2

echo -e "at+xdatachannel=1,1,\"/USBCDC/2\",\"/USBHS/NCM/0\",0 \r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cops=0 \r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cgdcont? \r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cgdata="M-RAW_IP",1 \r\n"> /dev/ttyACM2
sleep 2

echo -e "at+cgdcont? \r\n"> /dev/ttyACM2

