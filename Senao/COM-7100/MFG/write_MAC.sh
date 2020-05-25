#!/bin/bash
# 2020/05/15
# Darcy.Chang <Darcy.Chang@senao.com>

BASE_MAC=B456B9F008

eeupdate64e /NIC=1 /MAC="$BASE_MAC""01"
sleep 1
eeupdate64e /NIC=2 /MAC="$BASE_MAC""02"
sleep 1
eeupdate64e /NIC=3 /MAC="$BASE_MAC""03"
sleep 1
eeupdate64e /NIC=4 /MAC="$BASE_MAC""04"
sleep 1
eeupdate64e /NIC=5 /MAC="$BASE_MAC""05"
sleep 1
eeupdate64e /NIC=6 /MAC="$BASE_MAC""06"
sleep 1
eeupdate64e /NIC=7 /MAC="$BASE_MAC""07"
sleep 1
eeupdate64e /NIC=8 /MAC="$BASE_MAC""08"
sleep 1
eeupdate64e /NIC=9 /MAC="$BASE_MAC""09"
sleep 1
eeupdate64e /NIC=10 /MAC="$BASE_MAC""0A"
sleep 1
eeupdate64e /NIC=11 /MAC="$BASE_MAC""0B"
sleep 1
eeupdate64e /NIC=12 /MAC="$BASE_MAC""0C"
sleep 1
eeupdate64e /NIC=13 /MAC="$BASE_MAC""0D"
sleep 1
eeupdate64e /NIC=14 /MAC="$BASE_MAC""0E"
sleep 1
eeupdate64e /NIC=15 /MAC="$BASE_MAC""0F"
sleep 1
eeupdate64e /NIC=16 /MAC="$BASE_MAC""10"
sleep 1
eeupdate64e /NIC=17 /MAC="$BASE_MAC""11"
sleep 1
eeupdate64e /NIC=18 /MAC="$BASE_MAC""12"
sleep 1
eeupdate64e /NIC=19 /MAC="$BASE_MAC""13"
sleep 1
eeupdate64e /NIC=20 /MAC="$BASE_MAC""14"
sleep 1
eeupdate64e /NIC=21 /MAC="$BASE_MAC""15"
sleep 1
eeupdate64e /NIC=22 /MAC="$BASE_MAC""16"
sleep 1
eeupdate64e /NIC=23 /MAC="$BASE_MAC""17"
sleep 1


eeupdate64e /NIC=1 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=2 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=3 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=4 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=5 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=6 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=7 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=8 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=9 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=10 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=11 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=12 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=13 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=14 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=15 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=16 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=17 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=18 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=19 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=20 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=21 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=22 /MAC_DUMP | grep "LAN MAC Address is"
eeupdate64e /NIC=23 /MAC_DUMP | grep "LAN MAC Address is"
