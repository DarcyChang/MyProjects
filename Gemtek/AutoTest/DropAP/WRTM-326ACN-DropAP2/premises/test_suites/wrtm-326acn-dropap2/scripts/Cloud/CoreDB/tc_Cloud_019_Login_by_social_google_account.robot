*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_019_Login_by_social_google_account
    [Tags]    @TCID=WRTM-326ACN-488    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use google account to login.
    Cloud should feedback login success.

*** Keywords ***
Use google account to login.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by google
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login success.
    [Tags]     @AUTHOR=Jill_Chou
    check fb login success   ${loginResp}

*** Comment ***
2018-01-10     Jill_Chou
Init the script

