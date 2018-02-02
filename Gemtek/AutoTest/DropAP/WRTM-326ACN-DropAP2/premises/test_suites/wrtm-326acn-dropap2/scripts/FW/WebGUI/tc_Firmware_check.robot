*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***
${message}    Your firmware is up to date.

*** Test Cases ***
tc_Firmware_check
    [Documentation]  tc_Firmware_check
    ...    1. Go to DeviceManager/Firmware page, it will automatically check lastest firmware from upgrade server
    ...    2. If there's no new firmware available, the page should display a Check button
    ...    3. Verify an up to date message will be displayed if there is no new firmware available
    [Tags]   @TCID=WRTM-326ACN-173    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to DeviceManager/Firmware page, it will automatically check lastest firmware from upgrade server
    If there's no new firmware available, the page should display a Check button
    Verify an up to date message will be displayed if there is no new firmware available

*** Keywords ***
Go to DeviceManager/Firmware page, it will automatically check lastest firmware from upgrade server
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI

If there's no new firmware available, the page should display a Check button
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Click Firmware Check Button

Verify an up to date message will be displayed if there is no new firmware available
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    page should contain text    web    ${message}

*** comment ***
2017-10-11     Hans_Sun
Init the script
