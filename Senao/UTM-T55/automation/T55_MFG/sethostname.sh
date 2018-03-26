#!/bin/bash

if [ -z $1 ]; then
    echo "$0 <hostname>"
else
    echo "change hostname to $1"
    HOSTNAME=$(hostname)
    hostname $1
    echo $1 > /etc/hostname
    sed "s/$HOSTNAME/$1/" /etc/hosts > ./tmp 
    cp tmp /etc/hosts ; rm tmp
    systemctl restart systemd-logind.service
fi
