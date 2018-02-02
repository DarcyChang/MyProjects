*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=NS    @AUTHOR=Jill_Chou

*** Variables ***



*** Test Cases ***
tc_Cloud_044_Send_notification_to_multiple_Android_APP_MQTT
    [Tags]    @TCID=WRTM-326ACN-511    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Login account on three Android phone then stay at APP
    Trigger cloud send a notofication to Android APP via MQTT
    APP can received the notification



*** Keywords ***
Login account on three Android phone then stay at APP
    ${mosquitto_process1}  ${mosquitto_process2}  ${mosquitto_process3}=  set multi mosquitto_sub waiting
    Set Suite Variable  ${mosquitto_process1}    ${mosquitto_process1}
    Set Suite Variable  ${mosquitto_process2}    ${mosquitto_process2}
    Set Suite Variable  ${mosquitto_process3}    ${mosquitto_process3}

Trigger cloud send a notofication to Android APP via MQTT
    ${resp1}=  cloud device login with  deviceid=701a05010002  password=4u9kpm2h
    ${resp}  ${text}=  Send TLV command use android format  type=1  token=${resp1}
    Set Suite Variable  ${apiResult}    ${resp}
    Set Suite Variable  ${textResult}    ${text}

APP can received the notification
    Should Be Equal As Strings    ${apiResult['status']['code']}    2221

    ${TVLresult1}  ${TVLresult2}  ${TVLresult3}=  end of multi process   ${mosquitto_process1}   ${mosquitto_process2}   ${mosquitto_process3}
    Should Be Equal As Strings    ${TVLresult1[12:108]}  ${textResult}
    Should Be Equal As Strings    ${TVLresult2[12:108]}  ${textResult}
    Should Be Equal As Strings    ${TVLresult3[12:108]}  ${textResult}


*** Comment ***
2018-01-11     Jill_Chou
Init the script

