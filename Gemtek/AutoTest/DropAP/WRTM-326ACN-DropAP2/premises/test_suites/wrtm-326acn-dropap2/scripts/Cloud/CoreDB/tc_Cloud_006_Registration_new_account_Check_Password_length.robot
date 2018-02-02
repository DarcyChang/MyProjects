*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_006_Registration_new_account_Check_Password_length
    [Tags]    @TCID=WRTM-326ACN-475    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the password length only 7.
    Cloud should feedback the password is not allowed.
    Send username/email /password for registration but the password length is 16.
    Cloud should feedback the password is not allowed.

*** Keywords ***
Send username/email /password for registration but the password length only 7.
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the password is  1234567
    Set Suite Variable  ${apiResult}    ${resp}

Send username/email /password for registration but the password length is 16.
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the password is  1234567890123456
    Set Suite Variable  ${apiResult}    ${resp}

Cloud should feedback the password is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check password not allow  ${apiResult}


*** Comment ***
2017-12-19     Jill_Chou
Init the script
