*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=StressTest    @AUTHOR=Jill_Chou
Test Setup  Device reset default

*** Test Cases ***
tc_Cloud_046_Integration_and_stress_test_for_cloud
    [Tags]    @TCID=WRTM-326ACN-513    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Login account
    Binding device
    Check device list with device
    Modify device name
    Unbind device
    Check device list without device
    Repeat 100 times


*** Keywords ***
Login account
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud user login
    Set Suite Variable  ${loginToken}    ${resp}
Binding device
    Cloud user binding device   ${loginToken}

Check device list with device
    [Tags]     @AUTHOR=Jill_Chou
    ${deviceList}=    Get account device api  ${loginToken}

    Set Suite Variable  ${deviceList}    ${deviceList}


Modify device name
    Device list device ID check     ${deviceList}

Unbind device
    Cloud user unbinding device   ${loginToken}

Check device list without device
    ${deviceList2}=    Get account device api  ${loginToken}
    Device list have no device ID check     ${deviceList2}


Repeat 100 times
    Repeat Keyword  100   Repeat step

Repeat step
    Login account
    Binding device
    Check device list with device
    Modify device name
    Unbind device
    Check device list without device



*** Comment ***
2018-01-18     Jill_Chou
Init the script