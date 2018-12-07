#!/bin/bash

DELAY=0.5

function blink()
{
    while [ 1 ]; do
        devmem2 0xd0c005f0 b 01 > /dev/null
        sleep $DELAY
        devmem2 0xd0c005f0 b 0  > /dev/null
        sleep $DELAY
    done
}

devmem2 0xd0c005f1 b 02 > /dev/null

blink &

read -p "press enter to stop" ps
devmem2 0xd0c005f0 b 0 > /dev/null
disown $!
kill $!

