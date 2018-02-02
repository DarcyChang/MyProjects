*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_PPPoE_mode_Mismatched_authentication_types_or_usernamepassword
    [Documentation]  tc_PPPoE_mode_Mismatched_authentication_types_or_usernamepassword
    ...    1. To prepare the sniffer between WAN interface and peer router (PPPoE Server) or ISP device.  [Hardware Setup]
    ...    2. Go to WAN setting page ,and input mismatched authentication username or password with PPPoE mode.
    ...    3. Verify the DUT cannot establish PPPoE session with PPPoE Server.
    [Tags]   @TCID=WRTM-326ACN-385    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    Go to WAN setting page ,and input mismatched authentication username or password with PPPoE mode
    Verify the DUT cannot establish PPPoE session with PPPoE Server

*** Keywords ***
Go to WAN setting page ,and input mismatched authentication username or password with PPPoE mode
    [Documentation]  Setting WAN page on the GUI, to connect router/ISP device with PPPoE mode using correct username/password
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config PPPoE Client    ${g_dut_invalid_pppoe_username}    ${g_dut_invalid_pppoe_password}

Verify the DUT cannot establish PPPoE session with PPPoE Server
    [Documentation]  Verify the DUT cannot establish PPPoE session with PPPoE Server
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Fail    lanhost    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-11-22     Jujung_Chang
Init the script
