*** Settings ***
Documentation     ONT WebGUI keywords
Resource          caferobot/cafebase.robot

*** Keywords ***
log in to ONT
    [Arguments]    ${browser}    ${url}    ${username}    ${password}
    [Documentation]    log in to ONT through web browser
    delete_all_cookies    ${browser}
    go_to_page    ${browser}    ${url}
    input_text    ${browser}    name=Username    ${username}
    input_text    ${browser}    name=Password    ${password}
    click_element    ${browser}    xpath=//button[contains(., "Login")]
    page_should_contain_element    ${browser}    link=Logout

restore defaults for device
    [Arguments]    ${browser}    ${url}
    [Documentation]    restore defaults configuration for the device and reboot it
    go_to_page    ${browser}    ${url}
    click_element    ${browser}    link=Utilities
    click_element    ${browser}    link=Restore Defaults
    click_element    ${browser}    xpath=//button[contains(., "Restore")]
    click_element    ${browser}    xpath=//button[contains(., "Ok")]

reset device to factory status
    [Arguments]    ${browser}    ${url}
    [Documentation]    reset the device to factory status
    go_to_page    ${browser}    ${url}
    click_element    ${browser}    link=Support
    click_element    ${browser}    link=Factory Reset
    click_element    ${browser}    xpath=//button[contains(., "Reset")]
    click_element    ${browser}    xpath=//button[contains(., "Ok")]

reboot device
    [Arguments]    ${browser}    ${url}
    [Documentation]    reboot the device
    go_to_page    ${browser}    ${url}
    click_element    ${browser}    link=Utilities
    click_element    ${browser}    link=Reboot
    click_element    ${browser}    xpath=//button[contains(., "Reboot")]
    click_element    ${browser}    xpath=//button[contains(., "Ok")]


