*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=Redis    @AUTHOR=Jill_Chou
Library  Process

*** Variables ***
${cwd}  /home/vagrant/Downloads/online_tool
${deviceId}   600097052
*** Test Cases ***
tc_Cloud_033_Device_Online
    [Tags]    @TCID=WRTM-326ACN-502    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Device disconnect to internet
    Send check device status command to cloud.
    Should get the right status(Offline) from cloud

*** Keywords ***
Device disconnect to internet
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    Set Suite Variable  ${apiResult}    ${resp}

Send check device status command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  Get device status api  ${deviceId}
    log  ${resp}
    Set Suite Variable  ${onlineResult}    ${resp}


Should get the right status(Offline) from cloud
    [Tags]     @AUTHOR=Jill_Chou
    should be equal as strings   ${onlineResult['value']['IsOnline']}  False



*** Comment ***
2018-01-22     Jill_Chou
Init the script

