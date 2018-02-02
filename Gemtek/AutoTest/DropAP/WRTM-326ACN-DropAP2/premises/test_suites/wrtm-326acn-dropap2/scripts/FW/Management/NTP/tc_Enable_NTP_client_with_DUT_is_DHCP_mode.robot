*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_Enable_NTP_client_with_DUT_is_DHCP_mode
    [Documentation]  tc_Enable_NTP_client_with_DUT_is_DHCP_mode
    ...    1. Change the DHCP WAN connection types.
    ...    2. Checking the time is correct.Verify NTP can work well on DHCP mode.

    [Tags]   @TCID=WRTM-326ACN-324    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Change the DHCP WAN connection types
    Checking the time is correct.Verify NTP can work well on DHCP mode

*** Keywords ***
Change the DHCP WAN connection types
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Login Web GUI
    Config DHCP Client
    Check Address on the IPv4 WAN Status Table Is Valid    web

Checking the time is correct.Verify NTP can work well on DHCP mode
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Go to web page Device Management>System and Beneath System Properties
    ${realtime_before_push_syn_brower} =  Get Real Time
    sleep     5s
    Click SYNC WITH BROWSER Button
    ${realtime_after_push_syn_brower} =  Get Real Time
    Should Not Be Equal    ${realtime_before_push_syn_brower}    ${realtime_after_push_syn_brower}

    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management
    Checking NTP packets When Modified NTP Server On GUI

Go to web page Device Management>System and Beneath System Properties
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Get Real Time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result} =   Get Element text    web    ${Text_time}
    log    ${result}
    [Return]    ${result}

Click SYNC WITH BROWSER Button
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe click    web    ${Button_SYNC}
    #wait sync up time for GUI
    sleep    5

*** comment ***
2017-12-07     Jujung_Chang
Init the script
