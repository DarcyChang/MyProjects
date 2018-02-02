*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_NTP_work_well_after_reboot_with_DHCP_mode
    [Documentation]  tc_NTP_work_well_after_reboot_with_DHCP_mode
    ...    1. Change the DHCP WAN connection types.
    ...    2. DUT reboot on DHCP WAN connection types, verify NTP works well after DUT boot up.

    [Tags]   @TCID=WRTM-326ACN-329    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Change the DHCP WAN connection types
    DUT reboot on DHCP WAN connection types, verify NTP works well after DUT boot up.

*** Keywords ***
Change the DHCP WAN connection types
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Login Web GUI
    Config DHCP Client

DUT reboot on DHCP WAN connection types, verify NTP works well after DUT boot up.
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Click Reboot Button And Verify Function Is Work
    Login Web GUI
    Go to web page Device Management>System and Beneath System Properties
    ${realtime_before_push_syn_brower} =  Get Real Time
    sleep     10s
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
