#!/usr/bin/env python3
# -*- coding: cp950 -*-

import time
import serial
import os
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=57600,
)


def send_cmd(keyin):
    if "nvram restore" in keyin:
        delay_time = 3
    elif "reboot" in keyin:
        delay_time = 10
    else:
        delay_time = 1
    ser.isOpen()
    out = ""
    cmd = str(keyin) + "\n"
#    ser.write(cmd.encode('utf-8'))
    ser.write(cmd.encode())
    ser.flushOutput()
    time.sleep(12)  # Important

    max = -1
    while(max < ser.inWaiting()):
        max = ser.inWaiting()
        time.sleep(delay_time)

    while ser.inWaiting() > 4:
#        out += ser.read(1).decode('utf-8')
        out += ser.read(1).decode()
    ser.flushInput()
    if(str(out) != ""):
        print(">>" + out)
        if "Manage multi interface eth and wifi" in str(out):
            print("[Gemtek] nvram restore finish.\n")
