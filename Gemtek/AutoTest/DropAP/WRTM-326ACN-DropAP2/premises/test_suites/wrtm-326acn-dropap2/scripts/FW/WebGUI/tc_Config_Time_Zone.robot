*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Recover Timezone Value
*** Variables ***
${time_difference}    8

*** Test Cases ***
tc_Config_Time_Zone
    [Documentation]  tc_Config_Time_Zone
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    ...    2. Select Time Zone with any time zone on the list and Save
    ...    3. Verify timezone has changed and Local Time also has changed by new time zone value
    [Tags]   @TCID=WRTM-326ACN-330    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    Select Time Zone with any time zone on the list and Save
    Verify timezone has changed and Local Time also has changed by new time zone value

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Select Time Zone with any time zone on the list and Save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun

    ${UTC_time}    Get Different Timezone Value    UTC
    ${Taipei_time}    Get Different Timezone Value    Asia/Taipei
    cpe click    web    ${System_save}
    ${Taipei_time}    Get Real Time
    log    ${Taipei_time}
    Set Test Variable    ${UTC_time}    ${UTC_time}
    Set Test Variable    ${Taipei_time}    ${Taipei_time}

Get Different Timezone Value
    [Arguments]    ${type}
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Select Timezone By Value    ${type}
    ${time}    Get Real Time
    log    ${time}
    [Return]    ${time}

Verify timezone has changed and Local Time also has changed by new time zone value
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${UTC_hour} =    Get Regexp Matches    ${UTC_time}    \\s([\\w]{2}):     1
    ${UTC_hour}    Convert To Integer    @{UTC_hour}[0]
    log    ${UTC_hour}
    ${Taipei_hour} =    Get Regexp Matches    ${Taipei_time}    \\s([\\w]{2}):     1
    ${Taipei_hour}    Convert To Integer    @{Taipei_hour}[0]
    log    ${Taipei_hour}
    ${Taipei_hour}    run keyword if    ${Taipei_hour}>${UTC_hour}    Set Variable    ${Taipei_hour}
    ...    ELSE    evaluate    ${Taipei_hour}+24
    ${result}    evaluate    ${Taipei_hour}-${UTC_hour}
    ${time_difference}    Convert To Integer    ${time_difference}
    Should Be Equal    ${result}    ${time_difference}

Recover Timezone Value
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Select Timezone By Value    UTC

*** comment ***
2017-10-31     Hans_Sun
Init the script
