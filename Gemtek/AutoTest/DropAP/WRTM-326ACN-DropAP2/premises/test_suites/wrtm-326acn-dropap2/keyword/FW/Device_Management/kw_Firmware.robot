*** Settings ***
Resource    base.robot

*** Variables ***
${Button_Check} =    xpath=//*[@id="btn-check"]
${FW_version} =    xpath=//*[@id="maincontent"]/div/fieldset/table/tbody/tr[1]/td[2]
${DropAPcom_FW_version} =    xpath=//*[@id="new_fw_version"]

*** Keywords ***
Click Firmware Check Button
    [Arguments]
    [Documentation]    Click Firmware Check Button
    [Tags]    @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    10x    2s    click links    web    Device Management  Firmware
    Wait Until Keyword Succeeds    10x    2s    cpe click    web    ${Button_Check}
    sleep    1s


