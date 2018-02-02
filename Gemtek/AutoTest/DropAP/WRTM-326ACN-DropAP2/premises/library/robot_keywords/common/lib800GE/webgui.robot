*** Settings ***
Documentation     ONT WebGUI keywords
Resource          caferobot/cafebase.robot

*** Keywords ***
cpe web click
    [Documentation]  Click visible element and wait the action finished, ${wait_time} is timeout value for finding element
    [Arguments]    ${browser}    ${locator}    ${search_time}=1.5    ${wait_time}=30
    click visible element    ${browser}    ${locator}
    wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}

log in to ONT
    [Arguments]    ${browser}    ${url}    ${username}    ${password}
    [Documentation]    log in to ONT through web browser
    delete_all_cookies    ${browser}
    go_to_page    ${browser}    ${url}
    input_text    ${browser}    name=Username    ${username}
    input_text    ${browser}    name=Password    ${password}
    cpe web click    ${browser}    xpath=//button[contains(., "Login")]
    page_should_contain_element    ${browser}    link=Logout

restore defaults for device
    [Arguments]    ${browser}    ${url}
    [Documentation]    restore defaults configuration for the device and reboot it
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Utilities
    cpe web click    ${browser}    link=Restore Defaults
    cpe web click    ${browser}    xpath=//button[contains(., "Restore")]
    cpe web click    ${browser}    xpath=//button[contains(., "Ok")]

reset device to factory status
    [Arguments]    ${browser}    ${url}
    [Documentation]    reset the device to factory status
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Support
    cpe web click    ${browser}    link=Factory Reset
    cpe web click    ${browser}    xpath=//button[contains(., "Reset")]
    cpe web click    ${browser}    xpath=//button[contains(., "Ok")]

reboot device
    [Arguments]    ${browser}    ${url}
    [Documentation]    reboot the device
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Utilities
    cpe web click    ${browser}    link=Reboot
    cpe web click    ${browser}    xpath=//button[contains(., "Reboot")]
    cpe web click    ${browser}    xpath=//button[contains(., "Ok")]

modify dhcp address
    [Arguments]    ${browser}    ${url}    ${gateway_address}    ${min_address}    ${max_address}
    [Documentation]    modify dhcp gateway and pool address
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Advanced
    cpe web click    ${browser}    link=IP Addressing
    cpe web click    ${browser}    link=DHCP Settings
    input_text    ${browser}    name=IPInterfaceIPAddress    ${gateway_address}
    input_text    ${browser}    name=MinAddress    ${min_address}
    input_text    ${browser}    name=MaxAddress    ${max_address}
    cpe web click    ${browser}    xpath=//button[contains(., "Apply")]
    cpe web click    ${browser}    xpath=//button[contains(., "Ok")]

check dhcp device ip address
    [Arguments]    ${browser}    ${url}    ${exp_ip_address}
    [Documentation]    check dhcp gateway ip address
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Advanced
    cpe web click    ${browser}    link=IP Addressing
    cpe web click    ${browser}    link=DHCP Settings
    ${ip_address}    get element value    ${browser}    name=IPInterfaceIPAddress
    should be equal    ${ip_address}    ${exp_ip_address}

enable WAP
    [Arguments]    ${browser}    ${url}      ${search_time}=1.5    ${wait_time}=30
    [Documentation]    enable WAP on ONT
    go_to_page    ${browser}    ${url}
    #click_elem    ${browser}    link=Quick Start
    click visible element    ${browser}    link=Quick Start
    wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}
    #cpe web click    ${browser}    link=Configure Wireless Network
    click visible element    ${browser}    link=Configure Wireless Network
    wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}
    select_radio_button    ${browser}    wireless_access_point_onoff    1
    #cpe web click    ${browser}    xpath=//button[contains(., "Apply")]
    click visible element    ${browser}    xpath=//button[contains(., "Apply")]
    wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}
    #cpe web click    ${browser}    xpath=//button[contains(., "Ok")]
    wait until element is visible          ${browser}    xpath=//button[contains(., "Ok")]
    click visible element    ${browser}    xpath=//button[contains(., "Ok")]
    wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}
WAP should be enable
    [Arguments]    ${browser}    ${url}
    [Documentation]    WAP should be enable
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Quick Start
    cpe web click    ${browser}    link=Configure Wireless Network
    sleep    3
    radio_button_should_be_set_to    ${browser}    wireless_access_point_onoff    1

WAP should be disable
    [Arguments]    ${browser}    ${url}
    [Documentation]    WAP should be disable
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Quick Start
    cpe web click    ${browser}    link=Configure Wireless Network
    sleep    3
    radio_button_should_be_set_to    ${browser}    wireless_access_point_onoff    0

enable WAP-IGMP
    [Arguments]    ${browser}    ${url}
    [Documentation]    enable WAP-IGMP on ONT
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Support
    cpe web click    ${browser}    link=WAP Setup
    select_radio_button    ${browser}    wap_mode    1
    cpe web click    ${browser}    xpath=//button[contains(., "Apply")]
    cpe web click    ${browser}    xpath=//button[contains(., "Ok")]

WAP-IGMP should be enable
    [Arguments]    ${browser}    ${url}
    [Documentation]    WAP-IGMP should be enable on ONT
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Support
    cpe web click    ${browser}    link=WAP Setup
    sleep    3
    radio_button_should_be_set_to    ${browser}    wap_mode    1

WAP-IGMP should be disable
    [Arguments]    ${browser}    ${url}
    [Documentation]    WAP-IGMP should be disable on ONT
    go_to_page    ${browser}    ${url}
    cpe web click    ${browser}    link=Support
    cpe web click    ${browser}    link=WAP Setup
    sleep    3
    radio_button_should_be_set_to    ${browser}    wap_mode    0
