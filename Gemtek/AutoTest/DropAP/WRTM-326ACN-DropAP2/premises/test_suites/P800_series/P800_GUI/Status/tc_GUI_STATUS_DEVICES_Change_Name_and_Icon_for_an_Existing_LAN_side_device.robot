*** Settings ***
Documentation     Test suite for 844EGUI Test
Force Tags        @feature=status
Test Setup        setup
Test Teardown     teardown
Resource          base.robot

*** Variables ***
${new_dev_name1}    hahaha456
${new_dev_name2}    hahaha123
${dev_name}       device
${new_icon_name}    PS-3

*** Test Cases ***
change_dev_name_and_icon
    [Documentation]    [Author:wywang] change dev name and icon on 844 GUI
    ...    Step 1: PC 1 is connected to LAN port 1 again;
    ...    Step 2: Select PC 1 in device list and change the name: the name must be alphanumeric and contain less than 16 characters. Special characters can be used excluding “ “, space, commas, \, |;
    ...    Step 3: Select a new device icon;
    ...    Step 4: Verify the result.
    [Tags]    @TMS_ID=    @author=wywang    @Contour_ID=    CI=844V_0

    #**********Ping from lan pc to let the device list contains the PC*********
    Log to console    Ping from lan PC to let the device list contains the PC
    @{dut_address} =    Get Regexp Matches    ${url}    [1-9]+\.[1-9]+\.[1-9]+\.[1-9]+
    ${output} =    Run    ping @{dut_address}[0] -c 10
    log to console    ${output}

    #login to 844 Status-Device page
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Status
    cpe click    ${browser}    link=Devices
    #change the device ID and device icon
    select_from_list_by_index    ${browser}    xpath=//select[@id="lan-device-selector-id"]    1
    input text    ${browser}    xpath=//input[@id="new-device-name-id"]    ${new_dev_name1}
    cpe click    ${browser}    xpath=//button[@id="apply_btn"]
    wait until keyword succeeds    10x    1s    element_should_contain    ${browser}    xpath=//table[@id="device-table-id"]    ${new_dev_name1}
    select_from_list_by_index    ${browser}    xpath=//select[@id="lan-device-selector-id"]    1
    input text    ${browser}    xpath=//input[@id="new-device-name-id"]    ${new_dev_name2}
    select_from_list_by_label    ${browser}    xpath=//select[@id="lan-device-icon-id"]    Phone
    cpe click    ${browser}    xpath=//button[@id="apply_btn"]
    wait until keyword succeeds    10x    1s    element_should_contain    ${browser}    xpath=//table[@id="device-table-id"]    ${new_dev_name2}
    ${res}=    run webgui keyword with timeout    1s    get_element_attribute    ${browser}    xpath=//table[@id="device-table-id"]//div@class
    log to console    ${res}
    should be equal    ${res}    icon-ip-phone

*** Keywords ***
teardown
    factory reset via console    ${device}    ${browser}    ${url}
