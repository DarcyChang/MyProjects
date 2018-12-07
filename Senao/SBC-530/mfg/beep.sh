#!/bin/bash

TIME=0.1

function beep()
{
    while [ 1 ]; do
        /usr/bin/beep
        sleep $TIME
    done
}

modprobe pcspkr

beep &

read -p "press enter to stop" ps
disown $!
kill $!

