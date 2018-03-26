#!/bin/bash

trap 'echo 398 > /sys/class/gpio/unexport;
      echo 400 > /sys/class/gpio/unexport;
      echo 402 > /sys/class/gpio/unexport;
      echo 404 > /sys/class/gpio/unexport;
      echo 496 > /sys/class/gpio/unexport;
      echo 497 > /sys/class/gpio/unexport;
      echo "";
      echo "LED test stop"; exit 1' INT

echo 398 > /sys/class/gpio/export
echo 400 > /sys/class/gpio/export
echo 402 > /sys/class/gpio/export
echo 404 > /sys/class/gpio/export
echo 496 > /sys/class/gpio/export
echo 497 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio398/direction
echo out > /sys/class/gpio/gpio400/direction
echo out > /sys/class/gpio/gpio402/direction
echo out > /sys/class/gpio/gpio404/direction
echo out > /sys/class/gpio/gpio496/direction
echo out > /sys/class/gpio/gpio497/direction
sleep 1
echo 1 > /sys/class/gpio/gpio398/value
echo 1 > /sys/class/gpio/gpio400/value
echo 1 > /sys/class/gpio/gpio402/value
echo 1 > /sys/class/gpio/gpio404/value
read -p "1. press enter to test system LED on" ps
echo 0 > /sys/class/gpio/gpio398/value
echo 0 > /sys/class/gpio/gpio400/value
echo 0 > /sys/class/gpio/gpio402/value
echo 0 > /sys/class/gpio/gpio404/value
read -p "2. press enter to test system LED off" ps
echo 1 > /sys/class/gpio/gpio398/value
echo 1 > /sys/class/gpio/gpio400/value
echo 1 > /sys/class/gpio/gpio402/value
echo 1 > /sys/class/gpio/gpio404/value
read -p "3. press enter to test WAP LED (green)" ps
echo 0 > /sys/class/gpio/gpio496/value
echo 1 > /sys/class/gpio/gpio497/value
read -p "4. press enter to test WAP LED (amber)" ps
echo 1 > /sys/class/gpio/gpio496/value
echo 0 > /sys/class/gpio/gpio497/value
read -p "5. press enter to turn off WAP LED" ps
echo 1 > /sys/class/gpio/gpio496/value
echo 1 > /sys/class/gpio/gpio497/value

echo 398 > /sys/class/gpio/unexport
echo 400 > /sys/class/gpio/unexport
echo 402 > /sys/class/gpio/unexport
echo 404 > /sys/class/gpio/unexport
echo 496 > /sys/class/gpio/unexport
echo 497 > /sys/class/gpio/unexport

echo "System LED test finished!!"
