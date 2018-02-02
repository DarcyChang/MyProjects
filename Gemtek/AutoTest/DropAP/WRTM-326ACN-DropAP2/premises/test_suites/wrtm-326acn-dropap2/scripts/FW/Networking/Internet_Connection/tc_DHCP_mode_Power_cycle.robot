*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_DHCP_mode_Power_cycle
    [Documentation]  tc_DHCP_mode_Power_cycle
    ...  1. To establish DHCP Connection.
    ...  2. Reboot DUT.
    ...  3. After Power cycle, the DUT can establish the WAN connection automatically; verify LAN-PCs and smart mobile devices can access Internet.
    [Tags]   @TCID=WRTM-326ACN-355    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    To establish DHCP Connection
    Reboot DUT
    After Power cycle, the DUT can establish the WAN connection automatically; verify LAN-PCs and smart mobile devices can access Internet


*** Keywords ***
To establish DHCP Connection
    [Documentation]  To establish DHCP Connection.
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config DHCP Client

Reboot DUT
    [Documentation]  Reboot DUT
    [Tags]   @AUTHOR=Jujung_Chang
    Click Reboot Button And Verify Function Is Work

After Power cycle, the DUT can establish the WAN connection automatically; verify LAN-PCs and smart mobile devices can access Internet
    [Documentation]  After Power cycle, the DUT can establish the WAN connection automatically; verify LAN-PCs and smart mobile devices can access Internet
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-11-16     Jujung_Chang
Init the script
