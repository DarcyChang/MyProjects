*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_013_Login_by_email_registered_account_but_not_verified
    [Tags]    @TCID=WRTM-326ACN-482    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send email /password for login but the account already registered and not verified.
    Cloud should feedback login failed.

*** Keywords ***
Send email /password for login but the account already registered and not verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by email but the account already registered and not verified
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login failed.
    [Tags]     @AUTHOR=Jill_Chou
    check login fail   ${loginResp}

*** Comment ***
2017-12-13     Jill_Chou
Init the script
