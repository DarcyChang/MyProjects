*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_003_Registration_new_account_Check_Email_format
    [Tags]    @TCID=WRTM-326ACN-472    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send username/email /password for registration but the email format is not XXXXX@XXX.XXX
    Cloud should feedback the email is not allowed.
    Send username/email /password for registration but the email format is XXXXX@XXX.XX123
  #  Cloud should feedback the domain name is not allowed.

*** Keywords ***
Send username/email /password for registration but the email format is not XXXXX@XXX.XXX
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the email is  yoyocheckitout
    Set Suite Variable  ${apiResult}    ${resp}

Send username/email /password for registration but the email format is XXXXX@XXX.XX123
    [Tags]  @AUTHOR=Jill_Chou
    ${resp}=  cloud registration but the email is  jill_chou@gemteks.co123
    Set Suite Variable  ${apiResult}    ${resp}

Cloud should feedback the email is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check Email not allow  ${apiResult}

Cloud should feedback the domain name is not allowed.
    [Tags]  @AUTHOR=Jill_Chou
    check domain name not allow  ${apiResult}

*** Comment ***
2017-12-19     Jill_Chou
Init the script
