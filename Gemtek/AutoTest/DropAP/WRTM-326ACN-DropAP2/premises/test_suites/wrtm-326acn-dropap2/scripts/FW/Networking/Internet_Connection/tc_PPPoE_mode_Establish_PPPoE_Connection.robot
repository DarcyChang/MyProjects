*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_PPPoE_mode_Establish_PPPoE_Connection
    [Documentation]  tc_PPPoE_mode_Establish_PPPoE_Connection
    ...    1. To prepare the sniffer between WAN interface and peer router (PPPoE Server) or ISP device.  [Hardware Setup]
    ...    2. Setting WAN page on the GUI, to connect router/ISP device with PPPoE mode using correct username/password.
    ...    3. Verify LAN-PCs and smart mobile devices can access Internet if the PPPoE connect is established.
    [Tags]   @TCID=WRTM-326ACN-371    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    Setting WAN page on the GUI, to connect router/ISP device with PPPoE mode using correct username/password
    Verify LAN-PCs and smart mobile devices can access Internet if the PPPoE connect is established

*** Keywords ***
Setting WAN page on the GUI, to connect router/ISP device with PPPoE mode using correct username/password
    [Documentation]  Setting WAN page on the GUI, to connect router/ISP device with PPPoE mode using correct username/password
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config PPPoE Client    ${g_dut_pppoe_username}    ${g_dut_pppoe_password}
    Check Address on the IPv4 WAN Status Table Is Valid    web

Verify LAN-PCs and smart mobile devices can access Internet if the PPPoE connect is established
    [Documentation]  Verify LAN-PCs and smart mobile devices can access Internet if the PPPoE connect is established
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-11-21     Jujung_Chang
Init the script
