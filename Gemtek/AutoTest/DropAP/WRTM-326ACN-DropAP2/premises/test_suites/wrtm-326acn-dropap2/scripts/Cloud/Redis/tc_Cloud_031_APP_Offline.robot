*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=Redis    @AUTHOR=Jill_Chou
Library  Process

*** Variables ***
${cwd}  /home/vagrant/Downloads/online_tool
${userId}   700010073
*** Test Cases ***
tc_Cloud_031_APP_Offline
    [Tags]    @TCID=WRTM-326ACN-500    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use APP logout account
    Send check account status command to cloud.
    Should get the right status(Offline) from cloud

*** Keywords ***
Use APP logout account
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  Cloud login the account already registered and verified
    Set Suite Variable  ${apiResult}    ${resp}

Send check account status command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  Get device status api  ${userId}
    log  ${resp}
    Set Suite Variable  ${onlineResult}    ${resp}


Should get the right status(Offline) from cloud
    [Tags]     @AUTHOR=Jill_Chou
    should be equal as strings   ${onlineResult['value']['IsOnline']}  False



*** Comment ***
2018-01-22     Jill_Chou
Init the script

