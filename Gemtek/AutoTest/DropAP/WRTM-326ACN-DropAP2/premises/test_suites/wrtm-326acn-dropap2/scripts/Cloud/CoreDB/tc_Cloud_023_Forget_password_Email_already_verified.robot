*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou
Test Teardown   change password back  12345678

*** Variables ***


*** Test Cases ***
tc_Cloud_023_Forget_password_Email_already_verified
    [Tags]    @TCID=WRTM-326ACN-492    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send forget password and the email already registered and verified.
    Cloud should feedback success.
    Can received the Email and can modify old password to New password


*** Keywords ***
Send forget password and the email already registered and verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=   cloud reset password request
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback success.
    [Tags]     @AUTHOR=Jill_Chou
    check reset password request success   ${apiResult}

Can received the Email and can modify old password to New password
    [Tags]     @AUTHOR=Jill_Chou
    ${emailcode}=  received the email
    modify old password to new password   ${emailcode}   87654321
    check new password work


*** Comment ***
2017-12-21     Jill_Chou
Init the script