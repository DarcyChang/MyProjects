*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=ALG    @AUTHOR=Jujung_Chang

*** Variables ***
${getIP}
*** Test Cases ***
tc_After_reboot_verify_VPN_Passthrough_PPTP_is_work_well
    [Documentation]  tc_After_reboot_verify_VPN_Passthrough_PPTP_is_work_well

    ...    1. Reboot.
    ...    2. Setup PPTP server on WAN side.
    ...    3. Configure PPTP client on LAN side.
    ...    4. VPN client(PPTP client) dial in remote PPTP server.

    [Tags]   @TCID=WRTM-326ACN-514    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Reboot
    Setup PPTP server on WAN side
    Configure PPTP client on LAN side
    VPN client(PPTP client) dial in remote PPTP server

*** Keywords ***
Reboot
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Click Reboot Button And Verify Function Is Work

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
