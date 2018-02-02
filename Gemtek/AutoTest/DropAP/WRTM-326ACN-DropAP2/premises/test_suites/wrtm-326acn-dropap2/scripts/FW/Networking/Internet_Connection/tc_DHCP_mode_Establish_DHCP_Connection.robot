*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${getIP}
*** Test Cases ***
tc_DHCP_mode_Establish_DHCP_Connection
    [Documentation]  tc_DHCP_mode_Establish_DHCP_Connection
    ...    1. To prepare the sniffer between WAN interface and peer router or ISP device.  [Hardware Setup]
    ...    2. WAN interface connect to router or ISP device.  [Hardware Setup]
    ...    3. Move on WAN setting page, will show DUT WAN IP on GUI.
    ...    4. Verify IP information on the console (command: ifstatus wan).
    ...    5. In order to checking WAN interface is working, so checking LAN host can access WAN host.
    [Tags]   @TCID=WRTM-326ACN-339    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [Teardown]    Enable DHCP Server
    Move on WAN setting page, will show DUT WAN IP on GUI
    Verify IP information on the console (command: ifstatus wan)
    In order to checking WAN interface is working, so checking LAN host can access WAN host

*** Keywords ***
Move on WAN setting page, will show DUT WAN IP on GUI
    [Documentation]  Move on WAN setting page, will show DUT WAN IP on GUI
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    ${getIP} =  Check Address on the IPv4 WAN Status Table Is Valid    web

Verify IP information on the console (command: ifstatus wan)
    [Documentation]  Verify IP information on the console (command: ifstatus wan)
    [Tags]   @AUTHOR=Jujung_Chang
    ${r} =  Wait Until Keyword Succeeds    3x    2s    cli    dut1    ifstatus wan | grep address
    should contain    ${r}    ${getIP}

In order to checking WAN interface is working, so checking LAN host can access WAN host
    [Documentation]  In order to checking WAN interface is working, so checking LAN host can access WAN host
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-11-15     Jujung_Chang
Init the script
