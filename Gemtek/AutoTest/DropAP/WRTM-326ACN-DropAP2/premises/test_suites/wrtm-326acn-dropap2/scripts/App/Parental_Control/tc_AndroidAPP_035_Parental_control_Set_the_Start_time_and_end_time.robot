*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Recover Time Schedule status

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Leo_Li

*** Variables ***
${Config_Start_Time_value}    0130PM
${Show_Start_Time_value}    1:30PM
${Config_Stop_Time_value}    0200PM
${Show_Stop_Time_value}    2:00PM

*** Test Cases ***
tc_AndroidAPP_035_Parental_control_Set_the_Start_time_and_end_time
    [Documentation]  tc_AndroidAPP_035_Parental_control_Set_the_Start_time_and_end_time
    ...    1. Launch the app and go to the Parental control page.
    ...    2. Press Start time.
    ...    3. Set the timed to start it.
    ...    4. Press end time.
    ...    5. Set the timed to end it.

    [Tags]   @TCID=WRTM-326ACN-230    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the Parental control page
    Press Start time
    Set the timed to start it
    Press end time
    Set the timed to end it

*** Keywords ***
Launch the app and go to the Parental control page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Press Start time
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Right
    Wait Until Page Contains Element    ${Time_Schedule_Switch}    timeout=60
    Click Element    ${Time_Schedule_Switch}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}    timeout=60
    Page Should Contain Text    ON
    Click Element    ${Time_Schedule_Start_Time_arrow}

Set the timed to start it
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${Time_Schedule_Start_Time_hour_value}    ${Config_Start_Time_value}
    Click Element    ${Time_Schedule_Start_Time_Save}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}    timeout=60
    Page Should Contain Text    ${Show_Start_Time_value}

Press end time
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Stop_Time_arrow}

Set the timed to end it
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${Time_Schedule_Stop_Time_hour_value}    ${Config_Stop_Time_value}
    Click Element    ${Time_Schedule_Stop_Time_Save}
    Wait Until Page Contains Element    ${Time_Schedule_Stop_Time_arrow}    timeout=60
    Page Should Contain Text    ${Show_Stop_Time_value}

Recover Time Schedule status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Switch}
    Close APP

*** comment ***
2017-12-26    Leo_Li
Init the script