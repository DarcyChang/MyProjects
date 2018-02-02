*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${TCP_Port}    1234
${UDP_Port}    1234
${sendtimes}    10
*** Test Cases ***
tc_NAPT_with_a_TCP_and_UDP_connection_using_the_same_source_port
    [Documentation]  tc_NAPT_with_a_TCP_and_UDP_connection_using_the_same_source_port
    ...    1. Setup an environment that LAN host can connect to WAN host.
    ...    2. LAN host send TCP and UDP traffic at the same time to WAN host.

    [Tags]   @TCID=WRTM-326ACN-264    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup an environment that LAN host can connect to WAN host
    LAN host send TCP and UDP traffic at the same time to WAN host, using the same source port

*** Keywords ***
Initiate an outbound TCP connection to WAN host.At the same time, initiate an outbound UDP connection using same source port (UDP Echo) to WAN host.Verify WAN host can receive packets that port number(one is for TCP the other is UDP) is same as LAN hosts
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Using Hping with TCP AND UDP Port At the Same Time Successful Or Not    lanhost    wanhost    ${DEVICES.wanhost.traffic_ip}    ${TCP_Port}    ${UDP_Port}

Setup an environment that LAN host can connect to WAN host
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

LAN host send TCP and UDP traffic at the same time to WAN host, using the same source port
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Using Hping with TCP AND UDP Port At the Same Time Successful Or Not    lanhost    wanhost    ${DEVICES.wanhost.traffic_ip}    ${TCP_Port}    ${UDP_Port}

*** comment ***
2017-11-30     Jujung_Chang
Init the script
