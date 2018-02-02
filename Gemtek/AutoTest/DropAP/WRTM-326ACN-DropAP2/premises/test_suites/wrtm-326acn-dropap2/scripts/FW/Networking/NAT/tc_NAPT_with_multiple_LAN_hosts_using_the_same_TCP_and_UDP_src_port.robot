*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

Test Setup  Adding Route On vagrant PC(LAN host)
Test teardown  Delete Route On vagrant PC(LAN host)
*** Variables ***
${TCP_Port}    1234
${UDP_Port}    1234
*** Test Cases ***
tc_NAPT_with_multiple_LAN_hosts_using_the_same_TCP_and_UDP_src_port
    [Documentation]  tc_NAPT_with_multiple_LAN_hosts_using_the_same_TCP_and_UDP_src_port
    ...    1. Configure additional lan host(2 LAN host) and connect to the DUT LAN port.  [Hardware Setup]
    ...    2. Sending traffic from 2 LAN host to 1 WAN host, one is TCP the other is UDP.

    [Tags]   @TCID=WRTM-326ACN-262    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup an environment that two LAN host can connect to WAN host
    Sending traffic from 2 LAN host to 1 WAN host, one is TCP the other is UDP

*** Keywords ***
Setup an environment that two LAN host can connect to WAN host
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}
    Is Linux Ping Successful    vm1    ${DEVICES.wanhost.traffic_ip}

Sending traffic from 2 LAN host to 1 WAN host, one is TCP the other is UDP
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Using Hping with TCP Port Successful Or Not    vm1    wanhost    ${DEVICES.wanhost.traffic_ip}    ${TCP_Port}
    Using Hping with UDP Port Successful Or Not    lanhost    wanhost    ${DEVICES.wanhost.traffic_ip}    ${UDP_Port}

Adding Route On vagrant PC(LAN host)
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    echo ${DEVICES.vm1.password} | sudo -S route add -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}

Delete Route On vagrant PC(LAN host)
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    echo ${DEVICES.vm1.password} | sudo -S route del -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}
*** comment ***
2017-11-30     Jujung_Chang
Init the script
