*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Recover Time Schedule List

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_030_Parental_control_Screen_check
    [Documentation]  tc_AndroidAPP_030_Parental_control_Screen_check
    ...    1. Launch the app and go to the main screen.
    ...    2. Use finger slide to right side.
    ...    3. Check the UI screen of parental control page.

    [Tags]   @TCID=WRTM-326ACN-211    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the main screen
    Use finger slide to right side
    Check the UI screen of parental control page

*** Keywords ***
Launch the app and go to the main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Use finger slide to right side
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Right
    Wait Until Page Contains Element    ${Family_members_icon}

Check the UI screen of parental control page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    Time Limit
    Page Should Contain Text    Time Schedule
    Click Element    ${Time_Schedule_Switch}
    Wait Until Page Contains Element    ${Time_Schedule_Start_Time_arrow}
    Page Should Contain Text    Start Time
    Page Should Contain Text    Stop Time
    Page Should Contain Text    Content Filters
    Page Should Contain Text    Blocked Websites
    Page Should Contain Text    Blocked Apps
    Swipe To Up
    Page Should Contain Text    Clear Website and Apps Data
    Page Should Contain Text    Delete

Recover Time Schedule List
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Switch}
    sleep    5
    Page Should Contain Text    OFF
    Close APP

*** comment ***
2017-12-19    Leo_Li
Init the script
