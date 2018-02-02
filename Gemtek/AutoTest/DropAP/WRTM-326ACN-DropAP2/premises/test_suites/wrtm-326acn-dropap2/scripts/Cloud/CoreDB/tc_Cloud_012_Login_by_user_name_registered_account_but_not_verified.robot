*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_012_Login_by_user_name_registered_account_but_not_verified
    [Tags]    @TCID=WRTM-326ACN-481    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/password for login but the account already registered and not verified.
    Cloud should feedback login success.


*** Keywords ***
Send username/password for login but the account already registered and not verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login but the account already registered and not verified
    Set Suite Variable  ${loginResp}    ${apiResult}


Cloud should feedback login success.
    [Tags]     @AUTHOR=Jill_Chou
    check login success   ${loginResp}



*** Comment ***
2017-12-13     Jill_Chou
Init the script
