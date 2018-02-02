*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang
Test teardown    Restore Networking Configuration

*** Variables ***
${GraterThan_MTU_Maximum}    1465
*** Test Cases ***
tc_PPPoE_mode_with_greater_than_MTU
    [Documentation]  tc_PPPoE_mode_with_greater_than_MTU
    ...    1. Connect a PC on LAN side. [Hardware setup]
    ...    2. Connect a PPPoE Server on WAN side.  [Hardware setup]
    ...    3. Configure WAN Internet connection type to be PPPoE mode And Input right User ID and Password of 63 characters and connect to PPPoE Server.
    ...    4. Verify WAN port IP information
    ...    5. In MTU Auto mode, ping greater than 1465 bytes packet from LAN to WAN side PC, check the packet size. Checking WAN side(DUT WAN) packet will not be slice 2 packets.
    [Tags]   @TCID=WRTM-326ACN-331    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Configure WAN Internet connection type to be PPPoE mode And Input right User ID and Password of 63 characters and connect to PPPoE Server.
    Verify WAN port IP information
    MTU Checking In MTU Auto Mode, Ping Greater Than Maximum Packet Size From LAN Host To WAN Host, Check Packet Is Fragmented

*** Keywords ***
Configure WAN Internet connection type to be PPPoE mode And Input right User ID and Password of 63 characters and connect to PPPoE Server.
    [Documentation]  configure DUT WAN Internet connection type to be static mode and Setting of WAN IP address, Mask, default gateway and DNS information in DUT.
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config PPPoE Client    ${g_dut_pppoe_username}    ${g_dut_pppoe_password}

Verify WAN port IP information
    [Documentation]  Verify PPPoE Wan Type
    [Tags]   @AUTHOR=Jujung_Chang
    Verify PPPoE Wan Type

MTU Checking In MTU Auto Mode, Ping Greater Than Maximum Packet Size From LAN Host To WAN Host, Check Packet Is Fragmented
    [Documentation]  In MTU Auto mode, ping greater than 1465 bytes packet from LAN to WAN side PC, check the packet size. Checking WAN side(DUT WAN) packet will not be slice 2 packets.
    [Tags]   @AUTHOR=Jujung_Chang
    Checking Packet Greater Than MTU And Will Be Freagment    ${GraterThan_MTU_Maximum}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config DHCP Client

*** comment ***
2017-11-8     Jujung_Chang
Init the script
