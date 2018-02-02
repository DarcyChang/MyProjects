*** Settings ***
Resource    base.robot
Force Tags    @FEATURE=DeviceManager    @AUTHOR=Jill_Chou

*** Variables ***


*** Test Cases ***
tc_Cloud_029_Download_FW
    [Tags]    @TCID=WRTM-326ACN-498    @DUT=WRTM-326ACN     @AUTHOR=Jill_Chou
    Send download FW command to cloud.
    Get OTA server address
    Should get the right address from cloud and can download FW


*** Keywords ***
Send download FW command to cloud.
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=    Cloud request FW version
    Set Suite Variable  ${versionInfo}    ${resp}
Get OTA server address
    [Tags]     @AUTHOR=Jill_Chou
    ${str} =  Generate comment line   ${versionInfo['url']}
    Set Suite Variable  ${DownloadCommand}  ${str}

Should get the right address from cloud and can download FW
    ${md5sum}=  download file and check md5sum
    should be equal as strings  ${md5sum}    ${versionInfo['checksum']}

*** Comment ***
2018-01-05     Jill_Chou
Init the script
