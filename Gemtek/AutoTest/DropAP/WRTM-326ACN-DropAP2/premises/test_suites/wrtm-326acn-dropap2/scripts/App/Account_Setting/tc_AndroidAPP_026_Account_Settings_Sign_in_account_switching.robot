*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${app_second_username}    gavinchang
${app_second_password}    gavinchang

*** Test Cases ***
tc_AndroidAPP_026_Account_Settings_Sign_in_account_switching
    [Documentation]  tc_AndroidAPP_026_Account_Settings_Sign_in_account_switching
    ...    1. Launch the app and go to the login page.
    ...    2. Input the username or email, password.
    ...    3. Press Sign in button.
    ...    4. Press Sign out button.
    ...    5. Login another account.
    ...    6. Check the status.
    [Tags]   @TCID=WRTM-326ACN-391    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Input the username or email, password
    Press Sign in button
    Press Sign out button
    Login another account
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Input the username or email, password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    input username
    input password

Press Sign in button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch sign in
    wait main screen
    verify main screen device name

Press Sign out button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    touch sign out
    wait sign out web

Login another account
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${username}    ${app_second_username}
    Input Text    ${password}    ${app_second_password}
    touch sign in
    wait Bind the Existing DropAP Router Slave

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    ${sign_in_username}    Get Text    ${account_uesername}
    log    ${sign_in_username}
    Should Contain    ${sign_in_username}    ${app_second_username}

*** comment ***
2017-12-15 Gavin_Chang
1. Confirm the user info is correct, and slave account can bind Drop AP by authorization code

2017-11-27    Leo_Li
Init the script