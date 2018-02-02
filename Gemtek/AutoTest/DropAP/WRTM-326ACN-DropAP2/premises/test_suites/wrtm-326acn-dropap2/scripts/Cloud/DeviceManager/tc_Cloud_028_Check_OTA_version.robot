*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=DeviceManager    @AUTHOR=Jill_Chou

*** Test Cases ***
tc_Cloud_028_Check_OTA_version
    [Tags]    @TCID=WRTM-326ACN-497    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send check version command to cloud.
    Get OTA version
    Should get the right version from cloud

*** Keywords ***
Send check version command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud request FW version
    Set Suite Variable  ${versionInfo}    ${resp}

Get OTA version
    [Tags]     @AUTHOR=Jill_Chou
    log  ${versionInfo}

Should get the right version from cloud
    [Tags]     @AUTHOR=Jill_Chou
    Cloud check FW version   ${versionInfo}


*** Comment ***
2018-01-04     Jill_Chou
Init the script

