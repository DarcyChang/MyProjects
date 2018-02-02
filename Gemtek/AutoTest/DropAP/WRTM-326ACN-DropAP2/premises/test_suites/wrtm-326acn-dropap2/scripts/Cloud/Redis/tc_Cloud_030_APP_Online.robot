*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=Redis    @AUTHOR=Jill_Chou
Library  Process

*** Variables ***
${cwd}  /home/vagrant/Downloads/online_tool
${userId}   700010073
*** Test Cases ***
tc_Cloud_030_APP_Online
    [Tags]    @TCID=WRTM-326ACN-499    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use APP login account
    Send check account status command to cloud.
    Should get the right status(Online) from cloud

*** Keywords ***
Use APP login account
    [Tags]     @AUTHOR=Jill_Chou
    ${mosquitto_process}=  set user online and waiting
    ${resp}=  Cloud login the account already registered and verified
    Set Suite Variable  ${apiResult}    ${resp}
    Set Suite Variable  ${mosquitto_process}   ${mosquitto_process}


set user online and waiting
    [Tags]     @AUTHOR=Jill_Chou
    ${output}=  start process    node client.js   shell=True     cwd=${cwd}   alias=myproc
    [Return]   ${output}

Send check account status command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  Get device status api  ${userId}
    log  ${resp}
    Set Suite Variable  ${onlineResult}    ${resp}


Should get the right status(Online) from cloud
    [Tags]     @AUTHOR=Jill_Chou
    should be equal as strings   ${onlineResult['value']['IsOnline']}  True
    ${result}=  end of process  ${mosquitto_process}



*** Comment ***
2018-01-26     Jill_Chou
Init the script

