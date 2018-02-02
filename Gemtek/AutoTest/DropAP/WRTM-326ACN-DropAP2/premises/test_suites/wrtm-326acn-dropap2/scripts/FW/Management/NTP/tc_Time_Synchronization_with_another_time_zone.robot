*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=NTP    @AUTHOR=Jujung_Chang

Test teardown    Select Timezone By Value    ${time_zone_default}
*** Variables ***
${time_zone_default}    UTC
${select_taipei_timezone}    Asia/Taipei
${UTC_time}
${Taipei_time}

*** Test Cases ***
tc_Time_Synchronization_with_another_time_zone
    [Documentation]  tc_Time_Synchronization_with_another_time_zone
    ...    1. DUT connect to Internet then it will get network time from NTP servers.
    ...    2. Change the time zone.
    ...    3. Verify the current time switch to correct time.
    [Tags]   @TCID=WRTM-326ACN-320    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    DUT connect to Internet then it will get network time from NTP servers
    Change the time zone
    Verify the current time switch to correct time

*** Keywords ***
DUT connect to Internet then it will get network time from NTP servers
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Go to web page Device Management>System and Beneath System Properties
    ${realtime_before_push_syn_brower} =  Get Real Time
    Click SYNC WITH BROWSER Button
    Click SYNC WITH BROWSER Button
    ${realtime_after_push_syn_brower} =  Get Real Time
    Should Not Be Equal    ${realtime_before_push_syn_brower}    ${realtime_after_push_syn_brower}
    Set Global Variable    ${UTC_time}    ${realtime_after_push_syn_brower}

Change the time zone
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Select Timezone By Value    ${select_taipei_timezone}

    #workaround -> To select taipei time zone again.Because the time can't changed by running script.
    Select Timezone By Value    ${select_taipei_timezone}

Verify the current time switch to correct time
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Click SYNC WITH BROWSER Button
    ${taipei_time} =   Get Real Time
    log    ${taipei_time}
    @{taipei_times} =  Split String  ${taipei_time}
    log  ${taipei_time}
    ${taipei_time} =  Set Variable    @{taipei_times}[3]
    @{taipei_times} =  Split String  ${taipei_time}    :

    log    ${UTC_time}
    @{UTC_times} =  Split String  ${UTC_time}
    ${UTC_time} =   Set Variable    @{UTC_times}[3]
    @{UTC_times} =  Split String  ${UTC_time}    :

    log    @{taipei_times}[0]
    log    @{UTC_times}[0]

    Verify The Time Is Difference 8 Or 9 Hours Between Taipei and UTC    @{taipei_times}[0]    @{UTC_times}[0]

Go to web page Device Management>System and Beneath System Properties
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
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

Verify The Time Is Difference 8 Or 9 Hours Between Taipei and UTC
    [Arguments]    ${TPE}    ${UTC}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    ${diff} =  Run Keyword If    '${TPE}' < '${UTC}'    (TPE Time+24 Hours) Then Subtract UTC Time    ${TPE}    ${UTC}
    ...    ELSE IF    '${TPE}' > '${UTC}'    TPE Time Subtract UTC Time    ${TPE}    ${UTC}

    Run Keyword If    '${diff}' == '8' or '${diff}' == '9'    Pass Execution    Procedure is successful.
    ...    ELSE        Fail

TPE Time Subtract UTC Time
    [Arguments]    ${TPE}    ${UTC}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${d}
    ${d} =  Evaluate    ${TPE} - ${UTC}
    ${d} =  Convert To String    ${d}

(TPE Time+24 Hours) Then Subtract UTC Time
    [Arguments]    ${TPE}    ${UTC}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${d}
    ${TPE} =  Evaluate    ${TPE} + 24
    ${d} =  Evaluate    ${TPE} - ${UTC}
    ${d} =  Convert To String    ${d}

*** comment ***
2018-01-12     Jujung_Chang
The TPI and UTC time difference is 8,but it's probably 9 for running this script at some time point.
2017-12-05     Jujung_Chang
Init the script
