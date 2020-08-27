#!/bin/bash


eth1_mac=$(ifconfig eth1 | grep HWaddr | awk '{printf $5}')
eth2_mac=$(ifconfig eth2 | grep HWaddr | awk '{printf $5}')
eth3_mac=$(ifconfig eth3 | grep HWaddr | awk '{printf $5}')
eth4_mac=$(ifconfig eth4 | grep HWaddr | awk '{printf $5}')

service network-manager stop 2> /dev/null
iptables --flush -t nat

ifconfig eth1 down
ifconfig eth1 10.0.3.1 netmask 255.255.255.0 up
ifconfig eth2 down
ifconfig eth2 10.0.4.1 netmask 255.255.255.0 up

iptables -t nat -A POSTROUTING -s 10.0.3.1 -d 10.1.4.1 -j SNAT --to-source 10.1.3.1 
iptables -t nat -A PREROUTING -d 10.1.3.1 -j DNAT --to-destination 10.0.3.1
route del 10.1.4.1
ip route add 10.1.4.1 dev eth1 
arp -i eth1 -s 10.1.4.1 $eth2_mac
iptables -t nat -A POSTROUTING -s 10.0.4.1 -d 10.1.3.1 -j SNAT --to-source 10.1.4.1
iptables -t nat -A PREROUTING -d 10.1.4.1 -j DNAT --to-destination 10.0.4.1
route del 10.1.3.1
ip route add 10.1.3.1 dev eth2
arp -i eth2 -s 10.1.3.1 $eth1_mac

ifconfig eth3 down
ifconfig eth3 10.0.5.1 netmask 255.255.255.0 up
ifconfig eth4 down
ifconfig eth4 10.0.6.1 netmask 255.255.255.0 up

iptables -t nat -A POSTROUTING -s 10.0.5.1 -d 10.1.6.1 -j SNAT --to-source 10.1.5.1
iptables -t nat -A PREROUTING -d 10.1.5.1 -j DNAT --to-destination 10.0.5.1
route del 10.1.6.1
ip route add 10.1.6.1 dev eth3
arp -i eth3 -s 10.1.6.1 $eth4_mac
iptables -t nat -A POSTROUTING -s 10.0.6.1 -d 10.1.5.1 -j SNAT --to-source 10.1.6.1
iptables -t nat -A PREROUTING -d 10.1.6.1 -j DNAT --to-destination 10.0.6.1
route del 10.1.5.1
ip route add 10.1.5.1 dev eth4
arp -i eth4 -s 10.1.5.1 $eth3_mac


#ping -I eth1 10.1.4.1 &
#ping -I eth2 10.1.3.1 &
#ping -I eth3 10.1.6.1 &
#ping -I eth4 10.1.5.1 &
