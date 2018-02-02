*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_021_Forget_password_Email_not_registered
    [Tags]    @TCID=WRTM-326ACN-490    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send forget password but the email didn't registered.
    Cloud should feedback failed.


*** Keywords ***
Send forget password but the email didn't registered.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=   cloud forget password but the email didn't registered
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback failed.
    [Tags]     @AUTHOR=Jill_Chou
    check reset fail     ${apiResult}

*** Comment ***
2017-12-11     Jill_Chou
Init the script

