*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=MEC    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_034_Send_TLV_command_via_APP
    [Tags]    @TCID=WRTM-326ACN-503    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send TLV command (Modify device name)
    Cloud should feedback success.
    Received TLV command (Modify device name)



*** Keywords ***
Send TLV command (Modify device name)
    [Tags]     @AUTHOR=Jill_Chou
    ${mosquitto_process}=  set mosquitto_sub waiting
    ${resp}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    ${resp}  ${text}=  Send TLV command  type=1  token=${resp}
    Set Suite Variable  ${apiResult}    ${resp}
    ${result}=  end of process  ${mosquitto_process}
    Set Suite Variable  ${TVLresult}    ${result}
    Set Suite Variable  ${textResult}    ${text}

Cloud should feedback success.
    [Tags]     @AUTHOR=Jill_Chou
    Should Be Equal As Strings    ${apiResult['status']['code']}    2221


Received TLV command (Modify device name)
    [Tags]     @AUTHOR=Jill_Chou
    Should Be Equal As Strings    ${TVLresult[12:35]}  ${textResult}
    Should Be Equal As Strings    ${TVLresult[44:53]}  600097052



*** Comment ***
2018-01-11     Jill_Chou
Init the script
