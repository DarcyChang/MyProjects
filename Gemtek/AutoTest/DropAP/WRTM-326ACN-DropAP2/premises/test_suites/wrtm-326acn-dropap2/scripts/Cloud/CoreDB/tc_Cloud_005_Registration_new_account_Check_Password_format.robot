*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_005_Registration_new_account_Check_Password_format
    [Tags]    @TCID=WRTM-326ACN-474    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the password contain 符號.
    Cloud should feedback the password is not allowed.

*** Keywords ***
Send username/email /password for registration but the password contain 符號.
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the password is  1234567#
    Set Suite Variable  ${apiResult}    ${resp}

Cloud should feedback the password is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check password not allow  ${apiResult}


*** Comment ***
2017-12-19     Jill_Chou
Init the script
