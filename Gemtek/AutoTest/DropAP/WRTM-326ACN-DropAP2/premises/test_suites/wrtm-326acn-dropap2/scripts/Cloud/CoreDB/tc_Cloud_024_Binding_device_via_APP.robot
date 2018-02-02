*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou
Test Setup  Device reset default

*** Test Cases ***
tc_Cloud_024_Binding_device_via_APP
    [Tags]    @TCID=WRTM-326ACN-493    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send binding command to cloud.(Account ID & device ID)
    Get account device list
    Device list should have this device ID

*** Keywords ***
Send binding command to cloud.(Account ID & device ID)
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud user login
    Set Suite Variable  ${loginToken}    ${resp}
    Cloud user binding device   ${resp}


Get account device list
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Get account device api  ${loginToken}
    Set Suite Variable  ${deviceList}    ${resp}

Device list should have this device ID
    [Tags]     @AUTHOR=Jill_Chou
    Device list device ID check     ${deviceList}


*** Comment ***
2017-12-12     Jill_Chou
Init the script