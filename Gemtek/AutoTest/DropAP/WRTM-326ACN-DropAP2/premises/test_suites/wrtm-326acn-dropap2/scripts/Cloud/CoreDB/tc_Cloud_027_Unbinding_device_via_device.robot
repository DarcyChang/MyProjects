*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=CoreDB    @AUTHOR=Jill_Chou
Test Setup  Let APP binging device


*** Test Cases ***
tc_Cloud_027_Unbinding_device_via_device
    [Tags]    @TCID=WRTM-326ACN-496    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send unbinding command to cloud.(Account ID & device ID)
    Get account device list
    Device list should not have this device ID

*** Keywords ***
Send unbinding command to cloud.(Account ID & device ID)
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud device login
    Set Suite Variable  ${loginToken}    ${resp}
    Cloud device remove user   ${resp}

Get account device list
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Get user list api  ${loginToken}
    Set Suite Variable  ${userList}    ${resp}

Device list should not have this device ID
    [Tags]     @AUTHOR=Jill_Chou
    User list have no user ID check     ${userList}


*** Comment ***
2017-12-12     Jill_Chou
Init the script