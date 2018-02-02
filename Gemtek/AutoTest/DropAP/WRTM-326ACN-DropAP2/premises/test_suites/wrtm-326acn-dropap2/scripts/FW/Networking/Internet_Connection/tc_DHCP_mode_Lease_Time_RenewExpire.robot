*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_DHCP_mode_Lease_Time_RenewExpire
    [Documentation]  tc_DHCP_mode_Lease_Time_RenewExpire
    ...    1. To prepare the sniffer between WAN interface and peer router or ISP device.  [Hardware Setup]
    ...    2. Setting DHCP server. The lease time is 1 minutes.
    ...    3. Verify the DUT will get DUT WAN IP.
    ...    4. To disable the DHCP server and checking DUT WAN IP is disappear.
    ...    5. To enable the DHCP server and set lease time is 1 minutes the DUT can to obtain DUT WAN IP.
    ...    6. After 1 minutes, the DUT WAN IP can access DHCP server. It's means checking expire time is up ,the server will lease IP to DHCP client again.
    [Tags]   @TCID=WRTM-326ACN-347    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [Teardown]  Enable DHCP Server

    Setting DHCP server. The lease time is 1 minutes
    Verify the DUT will get DUT WAN IP
    To disable the DHCP server and checking DUT WAN IP is disappear
    To enable the DHCP server and set lease time is 1 minutes the DUT can to obtain DUT WAN IP
    After 1 minutes, the DUT WAN IP can access DHCP server. It's means checking expire time is up ,the server will lease IP to DHCP client again

*** Keywords ***
Setting DHCP server. The lease time is 1 minutes
    [Documentation]  Move on WAN setting page, will show DUT WAN IP on GUI
    [Tags]   @AUTHOR=Jujung_Chang
    Setting DHCP Server Lease Time    60

Verify the DUT will get DUT WAN IP
    [Documentation]  Move on WAN setting page, will show DUT WAN IP on GUI
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Check Address on the IPv4 WAN Status Table Is Valid    web

To disable the DHCP server and checking DUT WAN IP is disappear
    [Documentation]  To disable the DHCP server and checking DUT WAN IP is disappear
    [Tags]   @AUTHOR=Jujung_Chang
    Disable DHCP Server
    sleep    60s
    Check Address on the IPv4 WAN Status Table Is Empty    web

To enable the DHCP server and set lease time is 1 minutes the DUT can to obtain DUT WAN IP
    [Documentation]  To enable the DHCP server and set lease time is 1 minutes the DUT can to obtain DUT WAN IP
    [Tags]   @AUTHOR=Jujung_Chang
    Enable DHCP Server
    Setting DHCP Server Lease Time    60
    sleep    50s
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    Check Address on the IPv4 WAN Status Table Is Valid    web

After 1 minutes, the DUT WAN IP can access DHCP server. It's means checking expire time is up ,the server will lease IP to DHCP client again
    [Documentation]  In order to checking WAN interface is working, so checking LAN host can access WAN host
    [Tags]   @AUTHOR=Jujung_Chang
    sleep    60s
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}


Check Address on the IPv4 WAN Status Table Is Empty
    [Arguments]    ${b}
    [Documentation]
    [Tags]
    Reload Page    ${b}
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status
    Wait Until Keyword Succeeds    10x    2s    click links    ${b}    Status  Overview
    sleep    2
    ${value} =    get_element_text    ${b}    ${Table_Wan}
    log    ${value}
    should contain    ${value}    Not connected

*** comment ***
2017-11-27     Jujung_Chang
We put sleep after click Overview and extend sleep times.
2017-11-15     Jujung_Chang
Init the script
