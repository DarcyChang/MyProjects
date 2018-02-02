*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=NS    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_042_Send_notification_to_one_Android_APP_MQTT
    [Tags]    @TCID=WRTM-326ACN-509    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Login account on Android phone then stay at APP
    Trigger cloud send a notofication to Android APP via MQTT
    APP can received the notification



*** Keywords ***
Login account on Android phone then stay at APP
    ${mosquitto_process}=  set mosquitto_sub waiting
    Set Suite Variable  ${mosquitto_process}    ${mosquitto_process}

Trigger cloud send a notofication to Android APP via MQTT
    ${resp1}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    ${resp}  ${text}=  Send TLV command use android format  type=1  token=${resp1}
    Set Suite Variable  ${apiResult}    ${resp}
    Set Suite Variable  ${textResult}    ${text}

APP can received the notification
    ${TVLresult}=  end of process  ${mosquitto_process}
    Should Be Equal As Strings    ${apiResult['status']['code']}    2221
    Should Be Equal As Strings    ${TVLresult[12:108]}  ${textResult}


*** Comment ***
2017-12-29     Jill_Chou
Init the script

