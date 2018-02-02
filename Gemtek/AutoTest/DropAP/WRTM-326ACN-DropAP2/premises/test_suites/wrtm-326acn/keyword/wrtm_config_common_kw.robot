*** Settings ***

*** Variables ***
${keyword_timeout}    5

*** Keywords ***
Config DHCP Server IP Range
    [Arguments]    ${browser}    ${start_ip}    ${end_ip}=none
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    Input Text    ${browser}    xpath=//*[@id="lan_dhcp_range_start"]    ${start_ip}
    
    Run Keyword If    '${end_ip}' != 'none'    Input Text    ${browser}    xpath=//*[@id="lan_dhcp_range_end"]    ${end_ip}
    
    log many    ${start_ip}   ${end_ip}
    
    cpe click    ${browser}    xpath=//*[@id="dhcpSaveButton"]
    
    sleep    2s
    
    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=error_ip_range@style
    log    ${status}
    ${config_status} =    Run Keyword And Return Status   Should Contain    ${status}    none


    [Return]    ${config_status}


Config DHCP Server Lease Time
    [Arguments]    ${browser}    ${lease_value}    ${lease_unit}='minutes'
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
     # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    Input Text    ${browser}    xpath=//*[@id="leasetime_num"]    ${lease_value} 
    
    Run Keyword If    '${lease_unit}' == 'minutes'    Select From List By Value    ${browser}    xpath=//*[@id="leasetime_unit"]    m
    ...     ELSE    Select From List By Value    ${browser}    xpath=//*[@id="leasetime_unit"]    h
    # Sleep 5 seconds for taking effect
    sleep    5s
    log many    ${lease_value}    ${lease_unit}
    
    cpe click    ${browser}    xpath=//*[@id="dhcpSaveButton"]
    
Get DHCP Server Lease Time
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
     # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    ${lease_value}=    Get Element Value    ${browser}    xpath=//*[@id="leasetime_num"]
    ${lease_unit}=    Get Element Value    ${browser}    xpath=//*[@id="leasetime_unit"]
    ${lease_value}=    Convert To Integer    ${lease_value}
    
    ${total_lease_time}=   Run Keyword If    '${lease_unit}' == 'm'    Evaluate    ${lease_value}*60
    ...     ELSE    Evaluate    ${lease_value}*60*60
    
    log many    ${lease_value}    ${lease_unit}   ${total_lease_time}
    
    [Return]    ${total_lease_time}

Unconfig Static DHCP Client
    [Arguments]    ${browser}    ${table_id}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    Input Text    ${browser}    xpath=//*[@id="dhcpStaticT[${table_id}].ipaddr"]    ${EMPTY}
    Input Text    ${browser}    xpath=//*[@id="dhcpStaticT[${table_id}].mac"]    ${EMPTY}
   
    cpe click    ${browser}    xpath=//*[@id="dhcpSaveButton"]
    
Config Static DHCP Client
    [Arguments]    ${browser}    ${table_id}    ${client_ip}    ${client_mac}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    Input Text    ${browser}    xpath=//*[@id="dhcpStaticT[${table_id}].ipaddr"]    ${client_ip}
    Input Text    ${browser}    xpath=//*[@id="dhcpStaticT[${table_id}].mac"]    ${client_mac}
   
    cpe click    ${browser}    xpath=//*[@id="dhcpSaveButton"]
    
    
Config UPNP Switch
    [Arguments]    ${browser}    ${on_off}=off
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand UPNP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="upnp"]/h4/div[1]    1.5    30
    sleep    3s
    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_upnp"]/div[1]/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    Run Keyword If    '${on_off}' == 'on' and ${ret_switch_on} == False    cpe click     ${browser}    xpath=//*[@id="form_upnp"]/div[1]/div/div/div/span[3]
    ...    ELSE IF    '${on_off}' == 'on' and ${ret_switch_on} == True    comment    Config UPNP Switch is already on
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="form_upnp"]/div[1]/div/div/div/span[1]
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    Config UPNP Switch is already off

    sleep    3s
        

Check MAC Filter Switch is Off
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand MAC Filter section

    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    
    Should Not Be True    ${ret_switch_on}
    
Config MAC Filter Switch Off and Clear All
    [Arguments]    ${browser}    ${on_off}=off
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand MAC Filter section

    
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    //*[@id="mac_table"]/table/tfoot/tr/td/button
    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    Run Keyword If    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div/div/span[1]
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    MAC Filter Switch is already off
    
    sleep    3s
    cpe click    ${browser}    xpath=//*[@id="wifiMacSaveButton"]
    
Config MAC Filter Switch Off
    [Arguments]    ${browser}    ${on_off}=off
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand MAC Filter section
    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    Run Keyword If    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div/div/span[1]
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    MAC Filter Switch is already off
    
    sleep    3s
    cpe click    ${browser}    xpath=//*[@id="wifiMacSaveButton"]
    
Config MAC Filter Switch On and Add MAC
    [Arguments]    ${browser}    ${mac_address}    ${on_off}=on    ${type}=block
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand MAC Filter section
    #Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="wifi_mac"]/h4/div[1]    1.5    30
    sleep    3s
    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    Run Keyword If    '${on_off}' == 'on' and ${ret_switch_on} == False    cpe click     ${browser}    xpath=//*[@id="form_wifimac"]/div[1]/div[1]/div/div/div/div/span[3]
    ...    ELSE IF    '${on_off}' == 'on' and ${ret_switch_on} == True    comment    MAC Filter Switch is already on

    # Add deivce to blacklist (block) or whitelist (allow)
    cpe click    ${browser}    xpath=//*[@id="${type}"]     
    
    Input Text    ${browser}    xpath=//*[@id="new_mac_address"]    ${mac_address}
    cpe click    ${browser}    xpath=//*[@id="add_mac"]/span
    
    #Page Should Contain Element    ${browser}    xpath=//*[@id="${mac_address}"]
    sleep    3s
    cpe click    ${browser}    xpath=//*[@id="wifiMacSaveButton"]


Check PPTP_L2TP Connected
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="l2tp"]/h4/div[1]    1.5    30
    sleep    3s

    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=disconnect@style
    log    ${status}
    Should Not Contain    ${status}    none
    
    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=connect@style
    log    ${status}
    Should Contain    ${status}    none
    
Check PPTP_L2TP Disconnected
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="l2tp"]/h4/div[1]    1.5    30
    sleep    3s

    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=connect@style
    log    ${status}
    # Should not contain display none because when status connected, this text should be displayed so user can click on it to disconnect it.
    Should Not Contain    ${status}    none
    
    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=disconnect@style
    log    ${status}
    Should Contain    ${status}    none
    
Config PPTP_L2TP Disconnect
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen


    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=disconnect@style
    log    ${status}
    Run Keyword If    'display: none;' not in '''${status}'''    cpe click    ${browser}     xpath=//*[@id="disconnect"]
    # Sleep 10 seconds for taking effect
    sleep    10s
    
Config PPTP_L2TP Connect
    [Arguments]    ${browser}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen


    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=connect@style
    log    ${status}
    Run Keyword If    'display: none;' not in '''${status}'''    cpe click    ${browser}     xpath=//*[@id="connect"]
    # Sleep 10 seconds for taking effect
    sleep    10s
    

Config PPTP_L2TP
    [Arguments]    ${browser}    ${protocol_type}    ${pptp_server}    ${username}    ${password}    ${connection_type}=full    ${start_when_boot}=False    ${force_encryption}=False
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="l2tp"]/h4/div[1]    1.5    30
    sleep    3s
    Select From List By Value    ${browser}    xpath=//*[@id="proto"]    ${protocol_type}

    
    Input Text    ${browser}    xpath=//*[@id="server_ipaddr"]    ${pptp_server}
    Input Text    ${browser}    xpath=//*[@id="username"]    ${username}    
    Input Text    ${browser}    xpath=//*[@id="pw_ui"]    ${password}

    Run Keyword If    '${connection_type}' == 'full'    Select From List By Index    ${browser}    xpath=//*[@id="defaultroute"]    0
    ...    ELSE    Select From List By Index    ${browser}    xpath=//*[@id="defaultroute"]    1
    
    # connection_type=1: full, connection_type=0: smart
    Run Keyword If    ${start_when_boot}    select_checkbox    ${browser}    xpath=//*[@id="auto_checkbox"] 
    ...    ELSE    unselect_checkbox    ${browser}    xpath=//*[@id="auto_checkbox"] 
    
    Run Keyword If    ${force_encryption}    select_checkbox    ${browser}    xpath=//*[@id="mppe_checkbox"]
    ...    ELSE    unselect_checkbox    ${browser}    xpath=//*[@id="mppe_checkbox"] 
    
    
    cpe click    ${browser}    xpath=//*[@id="l2tpSaveButton"]
    
Check IP and Hostname Exist in the DHCP Client Table
    [Arguments]    ${browser}    ${table_id}    ${client_ip}    ${client_hostname}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_dhcp"]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    
    element_should_contain    ${browser}    xpath=//*[@id='${table_id}']    ${client_ip}
    element_should_contain    ${browser}    xpath=//*[@id='${table_id}']    ${client_hostname}

Config DEVICE DHCP Server Switch
    [Arguments]    ${browser}    ${on_off}=on
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand DHCP section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="dhcp"]/h4/div[1]    1.5    30
    sleep    3s
    
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="form_dhcp"]/div[1]/div/div/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    Run Keyword If    '${on_off}' == 'on' and ${ret_switch_on} == False    cpe click     ${browser}    xpath=//*[@id="form_dhcp"]/div[1]/div/div/div/div/span[3]
    ...    ELSE IF    '${on_off}' == 'on' and ${ret_switch_on} == True    comment    DHCP Server Switch is already on
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="form_dhcp"]/div[1]/div/div/div/div/span[1]
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    DHCP Server Switch is already off
    
    sleep    3s
    cpe click    ${browser}    xpath=//*[@id="dhcpSaveButton"]

    
Config Repeater WAN
    [Arguments]    ${browser}    ${wan_ssid}    ${wan_ssid_pw}    
    [Documentation]    Configure Repeater WAN
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]    ${keyword_timeout} minutes    Original Keyword didn't finish in ${keyword_timeout} minutes
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    2s
    
    # Click on Repearter mode tab
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_2"]/a
    
    
    # Wait until reflash icon stop
    Wait Until Keyword Succeeds    10x    2s    page should contain element    ${browser}    xpath=//*[@src="img/refresh_green_24.png"]
    
    #Select ssid and input password
    Select From List By Value    ${browser}    xpath=//*[@id="wifi_relay_auto_ssid"]    ${wan_ssid}
    Input Text    ${browser}    xpath=//*[@id="wifi_relay_netpass_auto"]    ${wan_ssid_pw}   
        
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    id=save_tab3    1.5    60
    
    
Config Port Forward Setting To Specified Index
    [Arguments]   ${Browser}    ${pf_index}    ${pf_switch}    ${pf_ext_port}    ${pf_int_port}    ${pf_int_ip}
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="port_forwarding"]/h4/div[1]    1.5    30
    sleep    3s
    
    # Check if specified port forward index is enabled.
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${pf_index}]/div[1]/label/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    

    log    ${pf_ext_port}
    input_text    ${browser}    xpath=//input[@id="pf_start_port_${pf_index}"]    ${pf_ext_port}
    
    log    ${pf_int_port}
    input_text    ${browser}    xpath=//input[@id="pf_end_port_${pf_index}"]    ${pf_int_port}
    
    log    ${pf_int_ip}
    input_text    ${browser}    xpath=//input[@id="pf_lan_ip_${pf_index}"]    ${pf_int_ip}
    
    
    
Control Multiple Port Forward Rule Switch
    [Arguments]   ${Browser}    ${pf_index_list}    ${on_off}=on
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p    1.5    30
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p    1.5    30
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="port_forwarding"]/h4/div[1]    1.5    30
    sleep    3s
    log many    ${pf_index_list}    ${on_off}

    :FOR    ${Port_Forward_ID}    IN    @{pf_index_list}
    \    # Check if specified port forward index is enabled.	
    \    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${Port_Forward_ID}]/div[1]/label/div@class
    \    log    ${CLASS}
    \    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    \    log    ${ret_switch_on}
    \    Run Keyword If    '${on_off}' == 'on' and ${ret_switch_on} == False    cpe click     ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${Port_Forward_ID}]/div[1]/label/div/div/span[3]
    \    ...    ELSE IF    '${on_off}' == 'on' and ${ret_switch_on} == True    comment    Port Forward Rule Switch is already on
    \    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${Port_Forward_ID}]/div[1]/label/div/div/span[1]
    \    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    Port Forward Rule Switch is already off
    
    cpe click    ${browser}    xpath=//*[@id="forwaring_save"]
    

Control Port Forward Rule Switch
    [Arguments]   ${Browser}    ${pf_index}    ${on_off}=on
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="port_forwarding"]/h4/div[1]    1.5    30
    sleep    3s
    log many    ${pf_index}    ${on_off}
    # Check if specified port forward index is enabled.
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${pf_index}]/div[1]/label/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    
    Run Keyword If    '${on_off}' == 'on' and ${ret_switch_on} == False    cpe click     ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${pf_index}]/div[1]/label/div/div/span[3]
    ...    ELSE IF    '${on_off}' == 'on' and ${ret_switch_on} == True    comment    Port Forward Rule Switch is already on
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == True    cpe click     ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${pf_index}]/div[1]/label/div/div/span[1]
    ...    ELSE IF    '${on_off}' == 'off' and ${ret_switch_on} == False    comment    Port Forward Rule Switch is already off
    
    cpe click    ${browser}    xpath=//*[@id="forwaring_save"]
    
Get Port Forward Setting From Specified Index
    [Arguments]   ${Browser}    ${pf_index}    
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="port_forwarding"]/h4/div[1]    1.5    30
    sleep    3s
    
    # Check if specified port forward index is enabled.
    ${CLASS} =    Get Element Attribute    ${browser}    xpath=//*[@id="forwarding_rule_T"]/div[${pf_index}]/div[1]/label/div@class
    log    ${CLASS}
    ${ret_switch_on} =    Run Keyword And Return Status   Should Contain    ${CLASS}    bootstrap-switch-on
    log    ${ret_switch_on}
    
    ${ret_pf_ext_port} =    Get Element Value    ${browser}    xpath=//input[@id="pf_start_port_${pf_index}"]
    log    ${ret_pf_ext_port}
    
    ${ret_pf_int_port} =    Get Element Value    ${browser}    xpath=//input[@id="pf_end_port_${pf_index}"]
    log    ${ret_pf_int_port}
    
    ${ret_pf_int_ip} =    Get Element Value    ${browser}    xpath=//input[@id="pf_lan_ip_${pf_index}"]
    log    ${ret_pf_int_ip}

    [Return]    ${ret_switch_on}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}

Config PPPoE WAN
    [Arguments]    ${browser}    ${username}    ${password}    
    [Documentation]    Configure PPPoE WAN
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]    ${keyword_timeout} minutes    Original Keyword didn't finish in ${keyword_timeout} minutes
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    10s
    
    cpe click    ${browser}    xpath=//*[@id="tab_0"]/a
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="tab_0"]/a

    # Config value to pppoe wan

    Wait Until Element Is Visible    ${browser}    id=save_tab1
    
    input_text    ${browser}    xpath=//*[@id="pppoe_username"]    ${username}
    input_text    ${browser}    xpath=//*[@id="pppoe_Password"]    ${password}
    
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    id=save_tab1     1.5    60

Config Static WAN and Check Internet 
    [Arguments]    ${browser}    ${ipaddr}    ${netmask}    ${gateway}    ${dns1}    ${dns2}=
    [Documentation]    Configure Static WAN and check internet status on main page
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Config Static WAN    ${browser}    ${ipaddr}    ${netmask}    ${gateway}    ${dns1}    ${dns2}
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html

    sleep    6s
    # Make sure Internet connection is up
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    ${browser}

Config Static WAN
    [Arguments]    ${browser}    ${ipaddr}    ${netmask}    ${gateway}    ${dns1}    ${dns2}=
    [Documentation]    Configure Static IP WAN
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]    ${keyword_timeout} minutes    Original Keyword didn't finish in ${keyword_timeout} minutes
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    10s
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_1"]/a

    # Config value to static wan

    Wait Until Element Is Visible    ${browser}    id=save_tab2
    cpe click    ${browser}    xpath=//*[@id="wlan_dhcp"]/div/div/div[1]/div/div/div/span[1]
    sleep    3s

    input_text    ${browser}    xpath=//*[@id="static_ipaddr"]    ${ipaddr}
    input_text    ${browser}    xpath=//*[@id="static_netmask"]    ${netmask}
    input_text    ${browser}    xpath=//*[@id="static_gateway"]    ${gateway}
    input_text    ${browser}    xpath=//*[@id="static_dns1"]    ${dns1}
    input_text    ${browser}    xpath=//*[@id="static_dns2"]    ${dns2}

    cpe click    ${browser}    id=save_tab2

Config WAN MTU 
    [Arguments]   ${browser}    ${mtu_size}
    [Documentation]    Configure MTU in Advanced setting
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # Go to device setting page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/p
    sleep    3s
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="mtu"]/h4/div[2]/i

    input_text    ${browser}    xpath=//input[@id="mtu_ui"]    ""
    input_text    ${browser}    xpath=//input[@id="mtu_ui"]    ${mtu_size}

    cpe click    ${browser}    xpath=//*[@id="mtuSaveButton"]

Config DHCP WAN And Check Internet
    [Arguments]    ${browser}
    [Documentation]    Configure DHCP WAN
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    5x    2s    Config DHCP WAN    ${browser}
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html

    sleep    3s    
    # Make sure Internet connection is up
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    ${browser}

Config DHCP WAN
    [Arguments]    ${browser}
    [Documentation]    Configure DHCP WAN
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]    ${keyword_timeout} minutes    Original Keyword didn't finish in ${keyword_timeout} minutes
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    5s
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    5s
    
    cpe click    ${browser}    xpath=//*[@id="tab_1"]/a
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_1"]/a
    
    
    #${class_ret}=    Get Element Attribute    ${browser}    xpath=//*[@id="tab_1"]/div[${pf_index}]@class
    #...    AND Should Contain    ${class_ret}    active
    #sleep    5s
    #Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_1"]/a
    
    #Run Keyword If    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_1"]/a 
    #...    AND     Wait Until Element Is Visible    ${browser}    id=save_tab2
    
    # Click on DHCP setting
    #Wait Until Element Is Visible    ${browser}    id=save_tab2
    sleep    3s
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="wlan_dhcp"]/div/div/div[1]/div/div/div/span[3]
    cpe click    ${browser}    id=save_tab2

    
    
    
    
Config Cisco Vlan on Ethernet Port
    [Arguments]    ${server}     ${ethernet_port}    ${vlan}
    [Documentation]    Config Cisco Vlan on Ethernet Port
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen    

    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${ethernet_port}
    cli    ${server}     switchport access ${vlan}
    cli    ${server}     sh
    cli    ${server}     no sh
    cli    ${server}     end
    ${val} =    cli    ${server}     show run int ${ethernet_port} | inc switchport  
    ${val} =    cli    ${server}     show run int ${ethernet_port} | inc switchport  
    log   ${vlan}
    Should Contain     ${val}    ${vlan}
    

Get Default Gatway IP
    [Arguments]    ${Device}
    [Documentation]    Get Default Gateway IP Address
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${default_gw_val}=    cli    ${Device}    ip route | grep default
    
    # Get gw ip address value from ip route command output
    ${default_gw_val}=    Get Regexp Matches    ${default_gw_val}    (\\w*\\.\\w*\\.\\w*\\.\\w*)
    
    # list to string
    ${default_gw_val}=    Get From List     ${default_gw_val}    0
    log    ${default_gw_val}
    
    Should Match Regexp    ${default_gw_val}    ^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$
    
    [Return]    ${default_gw_val}
    
    

Get Wan IP Value From Device SSH Connection
    [Arguments]   ${Device}    ${connection_type}=ethernet_wan
    [Documentation]    To get wan ip address from dut ssh connection
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    cli    ${Device}    ls
    
    ${val} =    Run Keyword if    '${connection_type}' == 'ethernet_wan'    cli    ${Device}    ifconfig ${DEVICES.${Device}.wan_interface}
    ...            ELSE    cli    ${Device}    ifconfig ${DEVICES.${Device}.pppoe_wan_interface}
    
    ${val} =    Run Keyword if    '${connection_type}' == 'ethernet_wan'    cli    ${Device}    ifconfig ${DEVICES.${Device}.wan_interface} | awk \'/inet addr/ {gsub(\"addr:\", \"\", $2); print $2}\'
    ...            ELSE    cli    ${Device}    ifconfig ${DEVICES.${Device}.pppoe_wan_interface} | awk \'/inet addr/ {gsub(\"addr:\", \"\", $2); print $2}\'

    log    ${val}

    ${val} =   Get Line    ${val}    1
    log    ${val}
    Should Match Regexp    ${val}    ^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$
    
    [Return]    ${val}

Config PPPoE Server Auth Type
    [Arguments]    ${server}    ${pppoe_interface}    ${auth_type}=chap pap
    [Documentation]    Configure PPPoE Server authentication type and verify config
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${pppoe_interface}
    cli    ${server}     ppp authentication ${auth_type}
    cli    ${server}     end
    ${val} =    cli    ${server}     show interfaces ${pppoe_interface} | inc ppp authentication
    ${val} =    cli    ${server}     show interfaces ${pppoe_interface} | inc ppp authentication
    Should Contain     ${val}    ppp authentication ${default_mtu}

Unconfig PPPoE Server Auth Type
    [Arguments]    ${server}    ${pppoe_interface}
    [Documentation]    Configure PPPoE Server authentication type and verify config
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    ${auth_type}=chap pap

    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${pppoe_interface}
    cli    ${server}     ppp authentication ${auth_type}
    cli    ${server}     end
    ${val} =    cli    ${server}     show interfaces ${pppoe_interface} | inc ppp authentication
    ${val} =    cli    ${server}     show interfaces ${pppoe_interface} | inc ppp authentication
    Should Contain     ${val}    ppp authentication ${auth_type}

Config PPPoE Server MTU
    [Arguments]    ${server}    ${mtu_interface}    ${default_mtu}
    [Documentation]    Configure PPPoE Server MTU and verify config
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${mtu_interface}
    cli    ${server}     mtu ${default_mtu}
    cli    ${server}     end
    ${val} =    cli    ${server}     show interfaces ${mtu_interface} | inc MTU
    ${val} =    cli    ${server}     show interfaces ${mtu_interface} | inc MTU
    Should Contain     ${val}    MTU ${default_mtu} bytes

Unconfig PPPoE Server MTU
    [Arguments]    ${server}     ${mtu_interface}
    [Documentation]    Unconfigure PPPoE Server MTU
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen    

    #cisco cleanup
    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${mtu_interface}    
    cli    ${server}     no mtu    
    cli    ${server}     end
    
Config DHCP Server MTU
    [Arguments]    ${server}    ${mtu_interface}    ${default_mtu}
    [Documentation]    Configure DHCP Server MTU and verify config
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${mtu_interface}
    cli    ${server}     mtu ${default_mtu}
    cli    ${server}     end
    ${val} =    cli    ${server}     show interfaces ${mtu_interface} | inc MTU
    ${val} =    cli    ${server}     show interfaces ${mtu_interface} | inc MTU
    Should Contain     ${val}    MTU ${default_mtu} bytes

Unconfig DHCP Server MTU
    [Arguments]    ${server}     ${mtu_interface}
    [Documentation]    Unconfigure DHCP Server MTU
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen    

    #cisco cleanup
    cli    ${server}     \r\n
    cli    ${server}     enable     timeout=20
    cli    ${server}     config t
    cli    ${server}     int ${mtu_interface}    
    cli    ${server}     no mtu    
    cli    ${server}     end
    
    
Clear Line In Terminal Server
    [Arguments]    ${term_serv}    ${line_num}
    [Documentation]    login to terminal server and clear indicated line
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    cli    ${term_serv}    enable    Password\:
    cli    ${term_serv}    lab
    cli    ${term_serv}    clear line ${line_num}   \[confirm\]
    cli    ${term_serv}    \r\n    
    
*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add config port forward keywords

2017-08-26     Gemtek_Thomas_Chen
1. Init the script
2. Add Config Static WAN
