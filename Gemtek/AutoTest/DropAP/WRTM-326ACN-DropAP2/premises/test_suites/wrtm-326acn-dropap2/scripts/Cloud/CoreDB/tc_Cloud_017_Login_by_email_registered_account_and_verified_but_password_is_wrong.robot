*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_017_Login_by_email_registered_account_and_verified_but_password_is_wrong
    [Tags]    @TCID=WRTM-326ACN-486    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send email /password for login but the password is wrong.
    Cloud should feedback login failed.

*** Keywords ***
Send email /password for login but the password is wrong.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by email the password is wrong
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login failed.
    [Tags]     @AUTHOR=Jill_Chou
    check login fail   ${loginResp}

*** Comment ***
2017-12-13     Jill_Chou
Init the script
