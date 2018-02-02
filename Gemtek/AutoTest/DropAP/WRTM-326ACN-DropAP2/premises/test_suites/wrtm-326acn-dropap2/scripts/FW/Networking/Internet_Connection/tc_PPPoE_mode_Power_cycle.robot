*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_PPPoE_mode_Power_cycle
    [Documentation]  tc_PPPoE_mode_Power_cycle
    ...  1. To establish PPPoE Connection.
    ...  2. Reboot DUT.
    ...  3. The DUT can establish the WAN connection automatically after Power cycle.
    ...  4. Verify LAN-PCs and smart mobile devices can access Internet.
    [Tags]   @TCID=WRTM-326ACN-386    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    To establish PPPoE Connection
    Reboot DUT
    The DUT can establish the WAN connection automatically after Power cycle
    Verify LAN-PCs and smart mobile devices can access Internet

*** Keywords ***
To establish PPPoE Connection
    [Documentation]  To establish PPPoE Connection
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config PPPoE Client    ${g_dut_pppoe_username}    ${g_dut_pppoe_password}
    Check Address on the IPv4 WAN Status Table Is Valid    web

Reboot DUT
    [Documentation]  Reboot DUT
    [Tags]   @AUTHOR=Jujung_Chang
    Click Reboot Button And Verify Function Is Work

The DUT can establish the WAN connection automatically after Power cycle
    [Documentation]  The DUT can establish the WAN connection automatically after Power cycle
    [Tags]   @AUTHOR=Jujung_Chang
    Go to Status Page
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status
    Verify PPPoE Wan Type

Verify LAN-PCs and smart mobile devices can access Internet
    [Documentation]  Verify LAN-PCs and smart mobile devices can access Internet
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.wanhost.traffic_ip}

Go to Status Page
    [Documentation]  Go to Status Page
    [Tags]   @AUTHOR=Jujung_Chang
    ${r} =  run keyword and return status    Wait Until Keyword Succeeds    3x    2s    cpe click    web    xpath=//*[@id="btn-control"]
    sleep    3s
    #if button is not visbale,then reload page.
    run keyword if  '${r}'=='False'    run keywords    Reload Page    web
    ...    AND    sleep    1
    ...    AND    Wait Until Element Is Visible    web    ${Link_Configure_DropAP}
    page should contain text    web    Status

*** comment ***
2017-11-21     Jujung_Chang
Init the script
