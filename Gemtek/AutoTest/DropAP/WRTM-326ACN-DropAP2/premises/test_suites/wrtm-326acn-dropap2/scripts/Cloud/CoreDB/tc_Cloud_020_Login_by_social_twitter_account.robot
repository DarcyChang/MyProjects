*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_020_Login_by_social_twitter_account
    [Tags]    @TCID=WRTM-326ACN-489    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use twitter account to login.
    Cloud should feedback login success.

*** Keywords ***
Use twitter account to login.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by twitter
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login success.
    [Tags]     @AUTHOR=Jill_Chou
    check fb login success   ${loginResp}

*** Comment ***
2018-01-10     Jill_Chou
Init the script

