*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou
Test Teardown   change unvarify password back  12345678

*** Variables ***


*** Test Cases ***
tc_Cloud_022_Forget_password_Email_but_not_verified
    [Tags]    @TCID=WRTM-326ACN-491    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send forget password and the email already registered but not verified.
    Cloud should feedback success.
    Can received the Email and can modify old password to New password


*** Keywords ***
Send forget password and the email already registered but not verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=   cloud reset password request with unverifiedEmail
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback success.
    [Tags]     @AUTHOR=Jill_Chou
    check reset password request success   ${apiResult}

Can received the Email and can modify old password to New password
    [Tags]     @AUTHOR=Jill_Chou
    ${emailcode}=  received the unregister email
    modify unregister old password to new password   ${emailcode}   87654321
    check unvarify new password work


*** Comment ***
2018-01-15     Jill_Chou
Init the script