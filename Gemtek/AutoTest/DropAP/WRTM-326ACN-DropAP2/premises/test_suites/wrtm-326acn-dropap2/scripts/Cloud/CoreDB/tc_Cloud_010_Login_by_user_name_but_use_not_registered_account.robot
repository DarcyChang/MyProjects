*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_010_Login_by_user_name_but_use_not_registered_account
    [Tags]    @TCID=WRTM-326ACN-479    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/password for login but the user name not registered
    Cloud should feedback login failed


*** Keywords ***
Send username/password for login but the user name not registered
    [Tags]     @AUTHOR=Jill_Chou
    ${apiResult}=   Cloud login but unregister user
    [Return]  ${apiResult}


Cloud should feedback login failed
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=     Send username/password for login but the user name not registered
    Should Be Equal As Strings    ${resp.status_code}    401
    Delete All Sessions

*** Comment ***
2017-12-11     Jill_Chou
Init the script