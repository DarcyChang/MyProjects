*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${browse_web}    yahoo.com

*** Test Cases ***
tc_AndroidAPP_036_Parental_control_Enable_Disable_the_time_schedule
    [Documentation]  tc_AndroidAPP_036_Parental_control_Enable_Disable_the_time_schedule
    ...    1. Launch the app and go to the Parental control page.
    ...    2. Enable the time schedule
    ...    3. Use the family mobile to browse network within the time
    ...    4. Use the family mobile to browse network overtime
    ...    5. Disable the time schedule
    ...    6. Use the family mobile to browse network within the time
    ...    7. Use the family mobile to browse network overtime
    [Tags]   @TCID=WRTM-326ACN-234    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the app and go to the Parental control page
    Enable the time schedule
    Use the family mobile to browse network within the time
    Use the family mobile to browse network overtime
    Disable the time schedule
    Use the family mobile to browse network within the time without schedule
    Use the family mobile to browse network overtime without schedule


*** Keywords ***
Launch the app and go to the Parental control page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen
    select family member
    Swipe To Right

Enable the time schedule
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Time_Schedule_Switch}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}
    Get Time Interval

Use the family mobile to browse network within the time
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Time_Schedule_Start_Time_arrow}
    Input Text    ${Time_Schedule_Start_Time_hour_value}    ${current_time}
    Click Element    ${Time_Schedule_Start_Time_Save}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}    timeout=10
    Click Element    ${Time_Schedule_Stop_Time_arrow}
    Input Text    ${Time_Schedule_Stop_Time_hour_value}    ${after_1hour_time}
    Click Element    ${Time_Schedule_Stop_Time_Save}
    Wait Until Page Contains Element    ${Time_Schedule_Stop_Time_arrow}    timeout=10
    Is Linux wget Successful    app_lanhost    ${browse_web}    5    -5


Use the family mobile to browse network overtime
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Time_Schedule_Start_Time_arrow}
    Input Text    ${Time_Schedule_Start_Time_hour_value}    ${after_30mins_time}
    Click Element    ${Time_Schedule_Start_Time_Save}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}    timeout=10
    Is Linux wget Failed    app_lanhost    ${browse_web}    5    -5

Disable the time schedule
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Time_Schedule_Switch}
    Wait Until Page Contains    OFF

Use the family mobile to browse network within the time without schedule
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${browse_web}    5    -5

Use the family mobile to browse network overtime without schedule
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${browse_web}    5    -5

Get Time Interval
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${result}    cli    app-vm    date +%s
    ${result}    Get Line    ${result}    1
    ${secs_after_1970}    Convert To Integer    ${result}
    ${result}    cli    app-vm    date --date @${secs_after_1970} +%I%M%p
    ${result}    Get Line    ${result}    1
    set suite variable    ${current_time}    ${result}
    ${after_1hour}    Evaluate    ${secs_after_1970} + 3600
    ${result}    cli    app-vm    date --date @${after_1hour} +%I%M%p
    ${result}    Get Line    ${result}    1
    set suite variable    ${after_1hour_time}    ${result}
    ${after_30mins}    Evaluate    ${secs_after_1970} + 1800
    ${result}    cli    app-vm    date --date @${after_30mins} +%I%M%p
    ${result}    Get Line    ${result}    1
    set suite variable    ${after_30mins_time}    ${result}

*** comment ***
2018-01-08 Gavin_Chang
Init the script
