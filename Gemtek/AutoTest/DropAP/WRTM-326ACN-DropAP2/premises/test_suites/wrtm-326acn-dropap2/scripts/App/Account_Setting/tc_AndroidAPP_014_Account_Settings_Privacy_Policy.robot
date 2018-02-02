*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_014_Account_Settings_Privacy_Policy
    [Documentation]  tc_AndroidAPP_014_Account_Settings_Privacy_Policy
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Press Privacy Policy.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-185    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left-upper corner
    Press Privacy Policy
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

Press Privacy Policy
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch privacy policy
    wait privacy policy web

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify privacy policy web status

*** comment ***
2017-11-17    Leo_Li
Init the script