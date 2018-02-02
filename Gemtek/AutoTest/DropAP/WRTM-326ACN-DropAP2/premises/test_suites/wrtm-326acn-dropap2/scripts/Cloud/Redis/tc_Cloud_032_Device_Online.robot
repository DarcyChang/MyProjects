*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=Redis    @AUTHOR=Jill_Chou
Library  Process

*** Variables ***

*** Test Cases ***
tc_Cloud_032_Device_Online
    [Tags]    @TCID=WRTM-326ACN-501    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Use APP login account
    Send check device status command to cloud.
    Should get the right status(Online) from cloud

*** Keywords ***
Use APP login account
    [Tags]     @AUTHOR=Jill_Chou
    ${mosquitto_process}=  set user online and waiting
    ${resp}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    Set Suite Variable  ${apiResult}    ${resp}
    Set Suite Variable  ${mosquitto_process}   ${mosquitto_process}

Send check device status command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  Get device status api  600097052
    log  ${resp}
    Set Suite Variable  ${onlineResult}    ${resp}


Should get the right status(Online) from cloud
    [Tags]     @AUTHOR=Jill_Chou
    should be equal as strings   ${onlineResult['value']['IsOnline']}  True
    ${result}=  end of process  ${mosquitto_process}



*** Comment ***
2018-01-22     Jill_Chou
Init the script

