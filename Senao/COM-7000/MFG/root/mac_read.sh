#!/bin/bash

eeupdate64e /NIC=2 /MAC_DUMP | grep "LAN MAC Address"
ifconfig eth1 | grep HWaddr

eeupdate64e /NIC=3 /MAC_DUMP | grep "LAN MAC Address"
ifconfig eth2 | grep HWaddr

eeupdate64e /NIC=4 /MAC_DUMP | grep "LAN MAC Address"
ifconfig eth3 | grep HWaddr

eeupdate64e /NIC=5 /MAC_DUMP | grep "LAN MAC Address"
ifconfig eth4 | grep HWaddr

eeupdate64e /NIC=1 /MAC_DUMP | grep "LAN MAC Address"
ifconfig eth0 | grep HWaddr
