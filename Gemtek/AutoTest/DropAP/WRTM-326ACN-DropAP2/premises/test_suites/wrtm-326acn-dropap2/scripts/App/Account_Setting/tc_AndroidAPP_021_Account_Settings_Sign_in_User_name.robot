*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_021_Account_Settings_Sign_in_User_name
    [Documentation]  tc_AndroidAPP_021_Account_Settings_Sign_in_User_name
    ...    1. Launch the app and go to the login page.
    ...    2. Input the username, password.
    ...    3. Press Sign in button.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-212    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Input the username and password
    Press Sign in button
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Input the username and password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    input username
    input password

Press Sign in button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch sign in

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait main screen
    verify main screen device name

*** comment ***
2017-11-24    Leo_Li
Init the script