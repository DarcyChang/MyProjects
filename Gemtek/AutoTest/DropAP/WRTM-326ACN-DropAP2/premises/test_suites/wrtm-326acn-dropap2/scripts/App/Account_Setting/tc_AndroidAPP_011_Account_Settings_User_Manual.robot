*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_011_Account_Settings_User_Manual
    [Documentation]  tc_AndroidAPP_011_Account_Settings_User_Manual
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Press User manual.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-205    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left-upper corner
    Press User manual
    Check the status

*** Keywords ***
Launch the app and into the main page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Press account settings at left-upper corner
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu

Press User manual
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch user manual
    wait user manual web

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify user manual web status

*** comment ***
2017-11-21    Leo_Li
Remove Variables

2017-11-20    Gavin_Chang
Move Variables To Parameters

2017-11-17    Leo_Li
Init the script