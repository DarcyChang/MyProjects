*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_010_Account_Settings_Buy_Drop_AP
    [Documentation]  tc_AndroidAPP_010_Account_Settings_Buy_Drop_AP
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Press Buy Drop AP.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-184    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left-upper corner
    Press Buy Drop AP
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

Press Buy Drop AP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch buy dropap
    wait Buy DropAP web

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify Buy DropAP web status

*** comment ***
2017-11-20 Gavin_Chang
Move Variables To Parameters.

2017-11-17    Leo_Li
Init the script