*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=ALG    @AUTHOR=Jujung_Chang
Test teardown    Reset Networking Setting
*** Variables ***
${getIP}
*** Test Cases ***
tc_VPN_Passthrough_PPTP
    [Documentation]  tc_VPN_Passthrough_PPTP
    ...    1. Setup PPTP server on WAN side.
    ...    2. Configure PPTP client on LAN side.
    ...    3. VPN client(PPTP client) dial in remote PPTP server.

    [Tags]   @TCID=WRTM-326ACN-387    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup PPTP server on WAN side
    Configure PPTP client on LAN side
    VPN client(PPTP client) dial in remote PPTP server

*** Keywords ***
Setup PPTP server on WAN side
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client
    Wait Until Keyword Succeeds    3x    1s    click links    web    Diagnostics
    Ping Using DropAP GUI    ${DEVICES.wanhost.default_gw}
    Should Be Contain Text At Diagnostics Page    bytes from

Configure PPTP client on LAN side
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S pon pptpserver
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo route add default gw ${gui_url}

VPN client(PPTP client) dial in remote PPTP server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.default_gw}

Reset Networking Setting
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S poff pptpserver

*** comment ***
2017-12-14     Jujung_Chang
Init the script
