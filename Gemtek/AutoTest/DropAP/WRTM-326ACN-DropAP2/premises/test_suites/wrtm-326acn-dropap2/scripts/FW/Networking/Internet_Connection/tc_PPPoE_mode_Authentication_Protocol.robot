*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_PPPoE_mode_Authentication_Protocol
    [Documentation]  tc_PPPoE_mode_Authentication_Protocol
    ...    1. To prepare the sniffer between WAN interface and peer router (PPPoE Server) or ISP device.  [Hardware Setup]
    ...    2. Go to WAN setting page, to set PPPoE mode with correct username/password.
    ...    3. Configure PPPoE server with CHAP authentication only.
    ...    4. Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet.
    ...    5. Configure PPPoE server with PAP authentication only
    ...    6. Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet.
    ...    7. Configure PPPoE server with CHAP and PAP authentication both.
    ...    8. Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet.
    [Tags]   @TCID=WRTM-326ACN-384    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [teardown]  Restore Networking Configuration

    Go to WAN setting page, to set PPPoE mode with correct username/password
    Configure PPPoE server with CHAP authentication only
    Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet
    Configure PPPoE server with PAP authentication only
    Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet
    Configure PPPoE server with CHAP and PAP authentication both
    Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet

*** Keywords ***
Go to WAN setting page, to set PPPoE mode with correct username/password
    [Documentation]  Go to WAN setting page, to set PPPoE mode with correct username/password
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config PPPoE Client    ${g_dut_pppoe_username}    ${g_dut_pppoe_password}
    Check Address on the IPv4 WAN Status Table Is Valid    web

Configure PPPoE server with CHAP authentication only
    [Documentation]  Configure PPPoE server with CHAP authentication only
    [Tags]   @AUTHOR=Jujung_Chang
    Change PPPoE Server Authentication On Cisco Server    chap

Configure PPPoE server with PAP authentication only
    [Documentation]  Configure PPPoE server with CHAP authentication only
    [Tags]   @AUTHOR=Jujung_Chang
    Change PPPoE Server Authentication On Cisco Server    pap

Configure PPPoE server with CHAP and PAP authentication both
    [Documentation]  Configure PPPoE server with CHAP authentication only
    [Tags]   @AUTHOR=Jujung_Chang
    Change PPPoE Server Authentication On Cisco Server    both

Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet
    [Documentation]  Verify the PPPoE connection can be established, and LAN-PCs and smart mobile devices can access Internet
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking
    Config DHCP Client

*** comment ***
2017-11-21     Jujung_Chang
Init the script
