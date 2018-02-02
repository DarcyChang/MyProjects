*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=MEC    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_036_Send_TLV_command_via_devices
    [Tags]    @TCID=WRTM-326ACN-505    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send TLV command (Sprinkler is watering)
    Cloud should feedback success.
    Received TLV command (Sprinkler is watering)



*** Keywords ***
Send TLV command (Sprinkler is watering)
    [Tags]     @AUTHOR=Jill_Chou
    ${mosquitto_process}=  set mosquitto_sub waiting
    ${resp1}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    ${resp}  ${text}=  Send TLV command  type=0  token=${resp1}
    Set Suite Variable  ${apiResult}    ${resp1}
    Set Suite Variable  ${sendResult}    ${resp}
    ${result}=  end of process  ${mosquitto_process}
    Set Suite Variable  ${TVLresult}    ${result}
    Set Suite Variable  ${textResult}    ${text}

Cloud should feedback success.
    [Tags]     @AUTHOR=Jill_Chou
    Should Be Equal As Strings    ${sendResult['status']['code']}    2221


Received TLV command (Sprinkler is watering)
    [Tags]     @AUTHOR=Jill_Chou
    ${serial}=  get the serial number  ${TVLresult}
    ${messageInfo}=  cloud get message by  ${serial}  ${apiResult}
    Should Be Equal As Strings    ${messageInfo}  ${textResult}



*** Comment ***
2017-12-29     Jill_Chou
Init the script
