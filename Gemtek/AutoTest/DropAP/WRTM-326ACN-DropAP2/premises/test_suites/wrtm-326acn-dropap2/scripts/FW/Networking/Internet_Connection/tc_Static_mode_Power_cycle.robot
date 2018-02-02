*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_Static_mode_Power_cycle
    [Documentation]  tc_Static_mode_Power_cycle
    ...  1. Setting static mode on the DUT, to Connect WAN interface to router or ISP.
    ...  2. Reboot DUT.
    ...  3. The DUT can establish the WAN connection automatically after Power cycle.
    ...  4. Verify LAN-PCs and smart mobile devices can access Internet.
    [Tags]   @TCID=WRTM-326ACN-368    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setting static mode on the DUT, to Connect WAN interface to router or ISP
    Reboot DUT
    The DUT can establish the WAN connection automatically after Power cycle
    Verify LAN-PCs and smart mobile devices can access Internet

*** Keywords ***
Setting static mode on the DUT, to Connect WAN interface to router or ISP
    [Documentation]  Setting static mode on the DUT, to Connect WAN interface to router or ISP
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Config Static Client

Reboot DUT
    [Documentation]  Reboot DUT
    [Tags]   @AUTHOR=Jujung_Chang
    Click Reboot Button And Verify Function Is Work

The DUT can establish the WAN connection automatically after Power cycle
    [Documentation]  The DUT can establish the WAN connection automatically after Power cycle
    [Tags]   @AUTHOR=Jujung_Chang
    Go to Status Page
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status
    Verify Static Wan Type

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
