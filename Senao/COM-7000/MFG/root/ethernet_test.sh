#/bin/bash
#Objective: Before stress item, we do iperf between ethernet port and USB NIC.
#Author:Darcy Chang
#Date:2019/03/05


if [ $# -ne 1 ] ;then
	echo "[ERROR] Wrong command."
	echo "./ethernet_test.sh seconds"
	echo "E.g., 30 seconds."
	echo "./ethernet_test.sh 30"
	exit
fi


timer=$1
rate_criteria=20


link_state=$(ethtool eth8 | grep 'Link detected' | awk '{print $3}')
echo "[DEBUG] eth8 $link_state"
if [ $link_state != "yes" ] ; then
	echo "[ERROR] Port eth8 link status $link_state" 
	ifconfig eth8
	echo "Ethernet port: FAIL"
	exit
fi


rm /tmp/1.txt
rm /tmp/2.txt
killall -9 iperf
iperf -s -D -w 512k
iperf -s -D -u -w 512k

ifconfig eth8 down
ifconfig eth8 hw ether 02:00:01:00:00:01
ifconfig eth8 10.0.1.1 netmask 255.255.255.0 up
ifconfig eth13 down
ifconfig eth13 hw ether 02:00:05:00:00:02
ifconfig eth13 10.0.2.1 netmask 255.255.255.0 up

iptables -t nat -A POSTROUTING -s 10.0.1.1 -d 10.1.2.1 -j SNAT --to-source 10.1.1.1
iptables -t nat -A PREROUTING -d 10.1.1.1 -j DNAT --to-destination 10.0.1.1
route del 10.1.2.1
ip route add 10.1.2.1 dev eth8
arp -i eth8 -s 10.1.2.1 02:00:05:00:00:02
iptables -t nat -A POSTROUTING -s 10.0.2.1 -d 10.1.1.1 -j SNAT --to-source 10.1.2.1
iptables -t nat -A PREROUTING -d 10.1.2.1 -j DNAT --to-destination 10.0.2.1
route del 10.1.1.1
ip route add 10.1.1.1 dev eth13
arp -i eth13 -s 10.1.1.1 02:00:01:00:00:01

sar -n DEV $timer 1 | grep Average | grep -v lo 1> /tmp/7.stat.tmp &
iperf -c 10.1.2.1 -t $timer -P 1 > /tmp/1.txt &
iperf -c 10.1.1.1 -t $timer -P 1 > /tmp/2.txt &

rx_rate_eth8=$(grep "eth8 " /tmp/7.stat.tmp | awk '{print $5}')
tx_rate_eth8=$(grep "eth8 " /tmp/7.stat.tmp | awk '{print $6}')
#echo "[DEBUG] eth8 tx rate $tx_rate_eth8"
#echo "[DEBUG] eth8 rx rate $rx_rate_eth8"

sleep $timer
sleep 10

eth8_tx=$(cat /tmp/1.txt  | grep "Mbits" | awk '{print $7}')
eth13_tx=$(cat /tmp/2.txt  | grep "Mbits" | awk '{print $7}')

if [ $(echo "$eth8_tx >= $rate_criteria" | bc) -eq 1 ] && [ $(echo "$eth13_tx >= $rate_criteria" | bc) -eq 1 ] ; then
	echo "Ethernet port: PASS"
else
	echo "Ethernet port: FAIL"
fi
