*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${fb_sign_in_username}    Svteam Gemt

*** Test Cases ***
tc_AndroidAPP_027_Account_Settings_Sign_in_by_Facebook
    [Documentation]  tc_AndroidAPP_027_Account_Settings_Sign_in_by_Facebook
    ...    1. Launch the app and go to the login page.
    ...    2. Press Facebook button.
    ...    3. Input the account and password about facebook.
    ...    4. Press submit button.
    ...    5. Try to use the facebook account to bind one Drop AP device.
    ...    6. Check the status.
    [Tags]   @TCID=WRTM-326ACN-392    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Press Facebook button
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Press Facebook button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch facebook sign in
    wait Bind the Existing DropAP Router Slave

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    ${sign_in_username}    Get Text    ${account_uesername}
    log    ${sign_in_username}
    Should Contain    ${sign_in_username}    ${fb_sign_in_username}

*** comment ***
2017-12-15 Gavin_Chang
1. Confirm the user info is correct, and slave account can bind Drop AP by authorization code

2017-11-27    Leo_Li
Init the script