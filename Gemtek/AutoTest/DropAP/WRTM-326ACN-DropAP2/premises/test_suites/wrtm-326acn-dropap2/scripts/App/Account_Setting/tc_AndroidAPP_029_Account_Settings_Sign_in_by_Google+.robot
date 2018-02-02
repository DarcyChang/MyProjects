*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${googleplus_account_id}    com.google.android.gms:id/account_display_name
${googleplus_sign_in_username}    SVTeam Gemtek

*** Test Cases ***
tc_AndroidAPP_029_Account_Settings_Sign_in_by_Google+
    [Documentation]  tc_AndroidAPP_029_Account_Settings_Sign_in_by_Google+
    ...    1. Launch the app and go to the login page.
    ...    2. Press Google+ button.
    ...    3. Input the account and password about Google+.
    ...    4. Press submit button.
    ...    5. Check the status.

    [Tags]   @TCID=WRTM-326ACN-394    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Press Google+ button
    Press submit button
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Press Google+ button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch google+ sign in

Input the account and password about Google+
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li


Press submit button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${googleplus_account_id}
    wait Bind the Existing DropAP Router Slave

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    ${sign_in_username}    Get Text    ${account_uesername}
    log    ${sign_in_username}
    Should Contain    ${sign_in_username}    ${googleplus_sign_in_username}

*** comment ***
2017-12-15 Gavin_Chang
1. Confirm the user info is correct, and slave account can bind Drop AP by authorization code

2017-11-27    Leo_Li
Init the script