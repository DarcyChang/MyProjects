*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${TCP_Port}    1234
*** Test Cases ***
tc_Outbound_TCP_connections_use_NAPT
    [Documentation]  tc_Outbound_TCP_connections_use_NAPT
    ...    1. Setup an environment that LAN host can connect to WAN host.
    ...    2. LAN host initiate an outbound TCP connection to WAN host.
    [Tags]   @TCID=WRTM-326ACN-409    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup an environment that LAN host can connect to WAN host
    LAN host initiate an outbound TCP connection to WAN host

*** Keywords ***
Setup an environment that LAN host can connect to WAN host
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

LAN host initiate an outbound TCP connection to WAN host
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Using Hping with TCP Port Successful Or Not    lanhost    wanhost    ${DEVICES.wanhost.traffic_ip}    ${TCP_Port}

*** comment ***
2017-11-30     Jujung_Chang
Init the script
