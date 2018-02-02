*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_009_Registration_new_account_Check_Email_already_used_and_verified
    [Tags]    @TCID=WRTM-326ACN-478    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the email already registered and verified.
    Cloud should feedback the email already registered.


*** Keywords ***
Send username/email /password for registration but the email already registered and verified.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=   cloud registration but the email is  jill_chou@gemteks.com
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback the email already registered.
    [Tags]     @AUTHOR=Jill_Chou
    check email already registered     ${apiResult}

*** Comment ***
2017-12-18     Jill_Chou
Init the script
