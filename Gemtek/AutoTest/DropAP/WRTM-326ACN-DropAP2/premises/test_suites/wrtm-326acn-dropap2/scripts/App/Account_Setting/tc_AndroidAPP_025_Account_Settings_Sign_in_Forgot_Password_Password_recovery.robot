*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Gavin_Chang

*** Variables ***
${reset_email}    devopsreport@gemteks.com
${g_app_username}    devops_test
${g_app_password}    1234abcd
${domainName80}    https://api.dropap.com:80

*** Test Cases ***
tc_AndroidAPP_025_Account_Settings_Sign_in_Forgot_Password_Password_recovery
    [Documentation]  tc_AndroidAPP_025_Account_Settings_Sign_in_Forgot_Password_Password_recovery
    ...    1. Launch the app and go to the login page
    ...    2. Press Forget Password(?) button
    ...    3. Input the email then press submit
    ...    4. Received the email to get the password
    ...    5. Use the default password to login the account
    ...    6. Check the status
    [Tags]   @TCID=WRTM-326ACN-390    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and go to the login page
    Press Forget Password(?) button
    Input the email then press submit
    Received the email to get the password
    Use the default password to login the account
    Check the status

*** Keywords ***
Launch the app and go to the login page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP

Press Forget Password(?) button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch reset password icon

Input the email then press submit
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    reset password    ${reset_email}

Received the email to get the password
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${emailcode}    received the email
    modify old password to new password    ${emailcode}    ${g_app_password}

Use the default password to login the account
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Sign In
    Wait Until Page Contains Element    ${account_info_menu}    timeout=30

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch account menu
    ${sign_in_email}    Get Text    ${Account_useremail}
    log    ${sign_in_email}
    Should Contain    ${sign_in_email}    ${reset_email}
*** comment ***
2017-11-20 Gavin_Chang
Move Variables To Parameters.

2017-11-17    Leo_Li
Init the script