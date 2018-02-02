*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang
Test teardown    Restore Networking Configuration

*** Variables ***
${GraterThan_MTU_Maximum}    1473
*** Test Cases ***
tc_Static_mode_with_greater_than_MTU
    [Documentation]  tc_Static_mode_with_greater_than_MTU
    ...    1. Connect a PC on LAN side. [Hardware  setup]
    ...    2. Configure DUT WAN Internet Connection Type To Be Static Mode And Setting Of WAN IP Address, Mask, Default Gateway And DNS Information In DUT.
    ...    3. Connect a PC on WAN side. [Hardware setup]
    ...    4. Verify WAN port IP information
    ...    5. Verify LAN to WAN communication.
    ...    6. In MTU Auto mode, ping greater than 1473 bytes packet from LAN to WAN side PC, check the packet size. Checking WAN side(DUT WAN) packet will be slice 2 packets.
    [Tags]   @TCID=WRTM-326ACN-304    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Configure DUT WAN Internet connection type to be static mode and Setting of WAN IP address, Mask, default gateway and DNS information in DUT
    Verify WAN port IP information
    Verify LAN to WAN communication
    MTU Checking In MTU Auto Mode, Ping Greater Than Maximum Packet Size From LAN Host To WAN Host, Check Packet Is Fragmented

*** Keywords ***
Configure DUT WAN Internet connection type to be static mode and Setting of WAN IP address, Mask, default gateway and DNS information in DUT
    [Documentation]  Configure DUT WAN Internet connection type to be static mode and Setting of WAN IP address, Mask, default gateway and DNS information in DUT
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config Static Client

Verify WAN port IP information
    [Documentation]  Verify DHCP Wan Type
    [Tags]   @AUTHOR=Jujung_Chang
    Verify Static Wan Type

Verify LAN to WAN communication
    [Documentation]  Renew IP manually, and check connection is built again
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

MTU Checking In MTU Auto Mode, Ping Greater Than Maximum Packet Size From LAN Host To WAN Host, Check Packet Is Fragmented
    [Documentation]  In MTU Auto mode, ping 1473 bytes packet from LAN host to WAN host check the packet size is 1473 bytes on DUT WAN side
    [Tags]   @AUTHOR=Jujung_Chang
    Checking Packet Greater Than MTU And Will Be Freagment    ${GraterThan_MTU_Maximum}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config DHCP Client

*** comment ***
2017-11-8     Jujung_Chang
Init the script
