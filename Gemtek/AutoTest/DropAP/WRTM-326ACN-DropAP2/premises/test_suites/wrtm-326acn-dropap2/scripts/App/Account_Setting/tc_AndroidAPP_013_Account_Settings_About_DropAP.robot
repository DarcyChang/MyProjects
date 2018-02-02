*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_013_Account_Settings_About_DropAP
    [Documentation]  tc_AndroidAPP_013_Account_Settings_About_DropAP
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Press about DropAP.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-449    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left-upper corner
    Press about DropAP
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

Press about DropAP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch about
    wait about web

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify about web status

*** comment ***
2017-11-17    Leo_Li
Init the script