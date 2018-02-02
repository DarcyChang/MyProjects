*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_022_Account_Settings_Sign_in_email
    [Documentation]  tc_AndroidAPP_022_Account_Settings_Sign_in_email
    ...    1. Launch the app and go to the login page.
    ...    2. Input the username or email, password.
    ...    3. Press Sign in button.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-213    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Input the username or email and password
    Press Sign in button
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP


Input the username or email and password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    input username
    input password
    touch sign in
    wait main screen
    verify main screen device name
    touch account menu
    touch sign out
    wait sign out web
    input email
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