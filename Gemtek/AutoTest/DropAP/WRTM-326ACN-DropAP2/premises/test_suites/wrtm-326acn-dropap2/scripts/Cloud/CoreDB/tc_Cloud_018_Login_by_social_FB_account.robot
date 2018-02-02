*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_018_Login_by_social_FB_account
    [Tags]    @TCID=WRTM-326ACN-487    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use FB account to login.
    Cloud should feedback login success.

*** Keywords ***
Use FB account to login.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login by facebook
    Set Suite Variable  ${loginResp}    ${apiResult}

Cloud should feedback login success.
    [Tags]     @AUTHOR=Jill_Chou
    check fb login success   ${loginResp}

*** Comment ***
2018-01-10     Jill_Chou
Init the script

