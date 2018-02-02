*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_002_Registration_new_account_Check_User_name_length
    [Tags]    @TCID=WRTM-326ACN-471    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the username length only 2
    Cloud should feedback the user name is not allowed.
    Send username/email /password for registration but the username length is 256.
    Cloud should feedback the user name is not allowed.


*** Keywords ***
Send username/email /password for registration but the username length only 2
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the username is  ya
    Set Suite Variable  ${apiResult}    ${resp}

Send username/email /password for registration but the username length is 256.
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the username is  aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaP
    Set Suite Variable  ${apiResult}    ${resp}


Cloud should feedback the user name is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check user name not allow  ${apiResult}

*** Comment ***
2017-12-19     Jill_Chou
Init the script
