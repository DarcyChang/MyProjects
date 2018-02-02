*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_001_Registration_new_account_Check_User_name_format
    [Tags]    @TCID=WRTM-326ACN-470    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the username contain special character(Not English character or digital).
    Cloud should feedback the user name is not allowed.


*** Keywords ***
Send username/email /password for registration but the username contain special character(Not English character or digital).
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the username is  testtest#
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback the user name is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check user name not allow  ${apiResult}

*** Comment ***
2017-12-19     Jill_Chou
Init the script
