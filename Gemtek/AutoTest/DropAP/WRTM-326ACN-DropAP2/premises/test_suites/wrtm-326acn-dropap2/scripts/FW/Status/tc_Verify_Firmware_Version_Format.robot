*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Status    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Verify_Firmware_Version_Format
    [Documentation]  tc_Verify_Firmware_Version_Format
    ...    1. Go to web page Device Management>Firmware
    ...    2. Verify Firmware Version Format in page is x.x.xx
    [Tags]   @TCID=WRTM-326ACN-286    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>Firmware
    Verify Firmware Version Format in page is x.x.xx

*** Keywords ***
Go to web page Device Management>Firmware
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  Firmware

Verify Firmware Version Format in page is x.x.xx
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element Text    web    ${FW_version}
    log    ${result}
    Should Match Regexp    ${result}    \\d\\.\\d\\.\\d+

*** comment ***
2017-11-06     Hans_Sun
Init the script
