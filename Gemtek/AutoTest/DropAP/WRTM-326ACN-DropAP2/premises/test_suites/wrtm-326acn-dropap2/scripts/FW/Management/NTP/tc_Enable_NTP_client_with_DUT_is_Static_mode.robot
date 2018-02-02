*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang
Test teardown    Restore Networking Configuration
*** Variables ***
*** Test Cases ***
tc_Enable_NTP_client_with_DUT_is_Static_mode
    [Documentation]  tc_Enable_NTP_client_with_DUT_is_Static_mode
    ...    1. Change the static WAN connection types.
    ...    2. Checking the time is correct.Verify NTP can work well on static mode.

    [Tags]   @TCID=WRTM-326ACN-325    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Change the DHCP WAN connection types
    Checking the time is correct.Verify NTP can work well on static mode

*** Keywords ***
Change the DHCP WAN connection types
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Login Web GUI
    Config Static Client    ${g_dut_DNS_from_company}
    Check Address on the IPv4 WAN Status Table Is Valid    web

Checking the time is correct.Verify NTP can work well on static mode
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

Restore Networking Configuration
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Config DHCP Client

*** comment ***
2017-12-07     Jujung_Chang
Init the script
