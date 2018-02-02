*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${MTU_Maximum}    1472
*** Test Cases ***
tc_DHCP_mode_MTU_function
    [Documentation]  tc_DHCP_mode_MTU_function
    ...    1. Connect a PC on LAN side. [Hardware  setup]
    ...    2. To Create WAN host and connection to DUT. [Hardware setup]
    ...    3. Connect DUT WAN port to a DHCP Server.
    ...    4. Verify WAN port IP information
    ...    5. Renew IP manually, and check connection is built again
    ...    6. In MTU Auto mode, ping 1472 bytes packet from LAN host to WAN host check the packet size is 1472 bytes on DUT WAN side
    [Tags]   @TCID=WRTM-326ACN-276    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Connect DUT WAN port to a DHCP Server
    Verify WAN port IP information
    Renew IP manually, and check connection is built again
    MTU Checking In MTU Auto Mode, Ping Maximum Size Packet From LAN Host To WAN Host, Check Packet Is Not Fragmented

*** Keywords ***
Connect DUT WAN port to a DHCP Server
    [Documentation]  DUT connect to WAN host and setting DUT is DHCP mode.
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client

Verify WAN port IP information
    [Documentation]  Verify DHCP Wan Type
    [Tags]   @AUTHOR=Jujung_Chang
    Verify DHCP Wan Type

Renew IP manually, and check connection is built again
    [Documentation]  Renew IP manually, and check connection is built again
    [Tags]   @AUTHOR=Jujung_Chang
    DUT Renew IP
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

DUT Renew IP
    [Documentation]  DUT Renew IP manually using ifconfig down and up.
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    cli    dut1    ifconfig ${DEVICES.dut1.wan_interface} down
    Wait Until Keyword Succeeds    3x    2s    cli    dut1    ifconfig ${DEVICES.dut1.wan_interface} up

MTU Checking In MTU Auto Mode, Ping Maximum Size Packet From LAN Host To WAN Host, Check Packet Is Not Fragmented
    [Documentation]  In MTU Auto mode, ping 1472 bytes packet from LAN host to WAN host check the packet size is 1472 bytes on DUT WAN side
    [Tags]   @AUTHOR=Jujung_Chang
    Checking Packet Not Greater Than MTU And Won't Be Freagment    ${MTU_Maximum}

*** comment ***
2017-11-8     Jujung_Chang
Init the script
