*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${twitter_sign_in_username_id}    username_or_email
${twitter_sign_in_username_id}    com.twitter.android:id/login_identifier
${twitter_sign_in_password_id}    password
${twitter_sign_in_password_id}    com.twitter.android:id/login_password
${twitter_login}    com.twitter.android:id/login_login
${twitter_connect}    com.twitter.android:id/ok_button
${twitter_sign_in_username}    gemteksv
${twitter_sign_in_password}    gemtekrd3
${authorize_app}    allow
${allow_share_email_address}    com.dropap.dropap:id/tw__allow_btn

*** Test Cases ***
tc_AndroidAPP_028_Account_Settings_Sign_in_by_Twitter
    [Documentation]  tc_AndroidAPP_028_Account_Settings_Sign_in_by_Twitter
    ...    1. Launch the app and go to the login page.
    ...    2. Press Twitter button.
    ...    3. Input the account and password about Twitter.
    ...    4. Press submit button.
    ...    5. Check the status.

    [Tags]   @TCID=WRTM-326ACN-393    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the login page
    Press Twitter button
    Press submit button
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Press Twitter button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch twitter sign in
    Wait Until Page Contains Element    ${twitter_connect}    timeout=60

Input the account and password about Twitter
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${twitter_sign_in_username_id}    ${twitter_sign_in_username}
    sleep    1
    Input Text    ${twitter_sign_in_password_id}    ${twitter_sign_in_password}
    sleep    1
    Swipe By Percent    50    20    50   10

Press submit button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${twitter_connect}
    sleep    3
    Click Element    ${allow_share_email_address}
    wait Bind the Existing DropAP Router Slave

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu
    ${sign_in_username}    Get Text    ${account_uesername}
    log    ${sign_in_username}
    Should Contain    ${sign_in_username}    ${twitter_sign_in_username}

*** comment ***
2017-12-15 Gavin_Chang
1. Confirm the user info is correct, and slave account can bind Drop AP by authorization code

2017 12-05 Gavin_Chang
1. Install Twitter and auto login

2017-11-27    Leo_Li
Init the script
