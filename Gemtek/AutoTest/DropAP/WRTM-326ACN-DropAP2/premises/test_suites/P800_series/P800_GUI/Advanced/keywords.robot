*** Settings ***
Resource          base.robot


*** Keywords ***
Create_service_block
    [Arguments]    ${browser}    ${service_name}    ${port_start}   ${port_end}  ${protocol}
    [Documentation]    [Author:bfan] Create the Block service
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | service_name | the name of service block |
    ...    | port_start | the start of the port range |
    ...    | port_end | the end of the port range |
    ...    | protocol | TCP or UDP |
    ...
    ...    Example:
    ...    | Create_service_block | firefox | test | 1000 | 2000 | TCP
    cpe click     ${browser}    link=Advanced
    cpe click     ${browser}    link=Service Blocking
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    cpe click     ${browser}    xpath=//*[@id='create_service_rule_button']
    input text    ${browser}    xpath=//label[text()="Name:"]/parent::div//input    ${service_name}
    input text    ${browser}    xpath=//label[text()="Port Start:"]/parent::div//input    ${port_start}
    input text    ${browser}    xpath=//label[text()="Port End:"]/parent::div//input    ${port_end}
    select_from_list_by_value     ${browser}    xpath=//*[@id='service_protocol_selector']     ${protocol}
    cpe click     ${browser}    xpath=.//*[@id='apply_edit_service_button']
    wait until keyword succeeds    10x    2s     element_should_contain    ${browser}    xpath=//table[@id="services_table"]    ${port_start}

Edit_service_block
    [Arguments]    ${browser}    ${service_name}    ${port_start}    ${protocol}   ${port_start_new}   ${port_end_new}
    [Documentation]   [Author:bfan] Edit the Block service
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | service_name | the name of service block |
    ...    | port_start | the start of the port range |
    ...    | protocol | TCP or UDP |
    ...    | port_start_new | modify the start of port range |
    ...    | port_end_new | modify the end of port range |
    ...
    ...    Example:
    ...    | Edit_service_block | firefox | test | TCP | 3000 | 4000
    cpe click     ${browser}    link=Service Blocking
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    select_from_list_by_label     ${browser}     xpath=//*[@id='service_select']     ${service_name}
    cpe click     ${browser}    xpath=//button[contains(., "Edit")]
    sleep         5
    cpe click     ${browser}    xpath=//td[contains(., "${port_start}")]/..//button[contains(., "Edit")]
    select_from_list_by_value     ${browser}    xpath=//*[@id='service_protocol_selector']     ${protocol}
    input text    ${browser}    xpath=//label[text()="Port Start:"]/parent::div//input    ${port_start_new}
    input text    ${browser}    xpath=//label[text()="Port End:"]/parent::div//input    ${port_end_new}
    cpe click     ${browser}    xpath=.//*[@id='apply_edit_service_button']
    element_should_contain    ${browser}    xpath=//table[@id="services_table"]    ${protocol}
    
Delete_service_block
    [Arguments]    ${browser}    ${service_name}    ${port_start}
    [Documentation]  [Author:bfan]  Delete the Block service
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | service_name | the name of service block |
    ...    | port_start | the start of the port range in the table|
    ...
    ...    Example:
    ...    | Delete_service_block | firefox | test | 3000
    cpe click     ${browser}    link=Service Blocking
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    select_from_list_by_label     ${browser}     xpath=//*[@id='service_select']     ${service_name}
    cpe click     ${browser}    xpath=//button[contains(., "Edit")]
    cpe click     ${browser}    xpath=//td[contains(., "${port_start}")]/..//button[contains(., "Remove")]
    wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
    #element should be visible  ${browser}    xpath=//div[@id='defaultAlertBoxID']
    cpe click     ${browser}    xpath=//button[contains(., "Ok")]
    element should not contain   ${browser}   xpath=//table[@id="services_table"]    ${port_start}


Create_website_block_service
    [Arguments]    ${browser}     ${web_address}    ${ip_address}
    [Documentation]  [Author:bfan]  Create web block service
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | web_address  | the blocked URL |
    ...    | ip_address | the client ip address|
    ...
    ...    Example:
    ...    | Create_website_block_service | firefox | www.baidu.com | 192.168.1.2
    cpe click     ${browser}    link=Website Blocking
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    input text    ${browser}    xpath=//label[text()="Website Address:"]/parent::div//input    ${web_address}
    select radio button       ${browser}        associate_website_with_selector        associate_website_with_ip_radio
    input text    ${browser}    xpath=//input[@id='ip_address_field']       ${ip_address}
    cpe click     ${browser}    xpath=//button[contains(., "Apply")]
    cpe click     ${browser}    link=Website Blocking
    wait until keyword succeeds    10x    2s        element_should_contain    ${browser}    xpath=//table[@id="associations_table"]    ${web_address}

Remove_website_block_service
    [Arguments]    ${browser}     ${web_address}
    [Documentation]  [Author:bfan]  Create web block service
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | web_address  | the blocked URL |
    ...
    ...    Example:
    ...    | Create_website_block_service | firefox | www.baidu.com

    cpe click     ${browser}    link=Advanced
    cpe click     ${browser}    link=Website Blocking
    cpe click     ${browser}    xpath=//td[contains(., "${web_address}")]/..//button
    wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
    #element should be visible     ${browser}     xpath=//div[@id='defaultAlertBoxID']
    cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    wait until keyword succeeds    10x    2s    element_should_not_contain    ${browser}    xpath=//table[@id="associations_table"]    ${web_address}

    
Create_DHCP_Reservation
    [Arguments]    ${browser}     ${mac_address}
    [Documentation]  [Author:bfan]  Create DHCP reservation list
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ip_address  | the ip address which you want to reserve |
    ...    | mac_address | the client mac address|
    ...
    ...    Example:
    ...    | Create_DHCP_Reservation | firefox | 001122334455 | 192.168.1.2
    cpe click     ${browser}    link=Advanced
    cpe click     ${browser}    link=IP Addressing
    cpe click     ${browser}    link=DHCP Reservation
    select radio button       ${browser}        devicetype       deviceTypeRadio2
    ${default_mac_address}      get element value        ${browser}    xpath=//input[@id='macAddressObj_manual']
    should be empty     ${default_mac_address}

    #Configure three types of valid mac address
    ${ip_address}              get selected list value    ${browser}    xpath=//*[@id='ip_address']
    Log to console    ${ip_address}
    select_from_list_by_label    ${browser}     xpath=//*[@id='ip_address']       ${ip_address}
    input text    ${browser}    xpath=//input[@id='macAddressObj_manual']    ${mac_address}
    cpe click     ${browser}    xpath=//button[contains(., "Apply")]
    wait until keyword succeeds    10x    2s        element_should_contain    ${browser}    xpath=//table[@id="dhcp_reservation_list"]    ${ip_address}
    [Return]   ${ip_address}
