*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_015_Login_by_email_registered_account_but_verified
    [Tags]    @TCID=WRTM-326ACN-484    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send email /password for login but the account already registered and verified.
    Cloud should feedback login success.

*** Keywords ***
Send email /password for login but the account already registered and verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by email but the account already registered and verified
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login success.
    [Tags]     @AUTHOR=Jill_Chou
    check login success   ${loginResp}

*** Comment ***
2017-12-13     Jill_Chou
Init the script
