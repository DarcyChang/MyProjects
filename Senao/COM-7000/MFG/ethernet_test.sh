#/bin/bash

timer=900
rate_criteria=50


link_state=$(ethtool eth0 | grep 'Link detected' | awk '{print $3}')
echo "[DEBUG] eth0 $link_state"
if [ $link_state != "yes" ] ; then
	echo "[ERROR] Port eth0 link status $link_state" 
	ifconfig eth0
	echo "Ethernet port: FAIL"
	exit
fi


rm /tmp/1.txt
rm /tmp/2.txt
killall -9 iperf
iperf -s -D -w 512k
iperf -s -D -u -w 512k

ifconfig eth0 down
ifconfig eth0 hw ether 02:00:01:00:00:01
ifconfig eth0 10.0.1.1 netmask 255.255.255.0 up
ifconfig eth5 down
ifconfig eth5 hw ether 02:00:05:00:00:02
ifconfig eth5 10.0.2.1 netmask 255.255.255.0 up

iptables -t nat -A POSTROUTING -s 10.0.1.1 -d 10.1.2.1 -j SNAT --to-source 10.1.1.1
iptables -t nat -A PREROUTING -d 10.1.1.1 -j DNAT --to-destination 10.0.1.1
route del 10.1.2.1
ip route add 10.1.2.1 dev eth0
arp -i eth0 -s 10.1.2.1 02:00:05:00:00:02
iptables -t nat -A POSTROUTING -s 10.0.2.1 -d 10.1.1.1 -j SNAT --to-source 10.1.2.1
iptables -t nat -A PREROUTING -d 10.1.2.1 -j DNAT --to-destination 10.0.2.1
route del 10.1.1.1
ip route add 10.1.1.1 dev eth5
arp -i eth5 -s 10.1.1.1 02:00:01:00:00:01

sar -n DEV $timer 1 | grep Average | grep -v lo 1> /tmp/7.stat.tmp &
iperf -c 10.1.2.1 -t $timer -P 1 > /tmp/1.txt &
iperf -c 10.1.1.1 -t $timer -P 1 > /tmp/2.txt &

rx_rate_eth0=$(grep "eth0 " /tmp/7.stat.tmp | awk '{print $5}')
tx_rate_eth0=$(grep "eth0 " /tmp/7.stat.tmp | awk '{print $6}')
#echo "[DEBUG] eth0 tx rate $tx_rate_eth0"
#echo "[DEBUG] eth0 rx rate $rx_rate_eth0"

sleep $timer
sleep 10

eth0_tx=$(cat /tmp/1.txt  | grep "Mbits" | awk '{print $7}')
eth5_tx=$(cat /tmp/2.txt  | grep "Mbits" | awk '{print $7}')

if [ $(echo "$eth0_tx >= $rate_criteria" | bc) -eq 1 ] && [ $(echo "$eth5_tx >= $rate_criteria" | bc) -eq 1 ] ; then
	echo "Ethernet port: PASS"
else
	echo "Ethernet port: FAIL"
fi
