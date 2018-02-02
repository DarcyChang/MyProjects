*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou
Test Setup  Device reset default


*** Test Cases ***
tc_Cloud_026_Binding_device_via_device
    [Tags]    @TCID=WRTM-326ACN-495    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send binding command to cloud.(Account ID & device ID)
    Get account device list
    Device list should have this account ID


*** Keywords ***
Send binding command to cloud.(Account ID & device ID)
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud device login
    Set Suite Variable  ${loginToken}    ${resp}
    Cloud device binding user   ${resp}

Get account device list
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Get user list api  ${loginToken}
    Set Suite Variable  ${userList}    ${resp}

Device list should have this account ID
    [Tags]     @AUTHOR=Jill_Chou
    User list user ID check     ${userList}


*** Comment ***
2017-12-12     Jill_Chou
Init the script