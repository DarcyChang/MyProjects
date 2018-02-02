*** Settings ***
Resource          base.robot

*** Keywords ***
P800_suite_setup
    [Arguments]    ${switch_session}    ${device_port}    ${device_vlanid}    ${vm_port}    ${vm_vlanid}
    [Documentation]    author:alu.Configure the switch port before 800 Series CI suite
#    Switch_set_hybrid_port_untag_vlan    ${switch_session}    ${device_port}    ${vm_vlanid}
#    run keyword if     "${dut_uplink_ont}"=="0"       Switch_set_hybrid_port_untag_vlan    ${switch_session}    ${vm_port}    ${device_vlanid}
    Switch_set_access_vlan_h3c     ${switch_session}    ${vm_port}    ${device_vlanid}
    ${ont_ins}    Build 800ont Testlib    ${dut_session}
    ${e7_ins}    Build E7 Testlib    ${e7_session}
    run keyword unless      "${dut_uplink_ont}"=="0"      P800_config_uplink_device      ${e7_ins}      ${ont_ins}      ${dut_uplink_ethport}        brdg
    #set ip for device    ${linux_host}    cafetest    eth1    ${client_ip}
    ${result_restore_default}    Ont Restore Default    ${ont_ins}
    sleep      150

P800_rg_suite_setup
    [Arguments]    ${switch_session}    ${device_port}    ${device_vlanid}    ${vm_port}    ${vm_vlanid}
    [Documentation]    author:alu.Configure the switch port before 800 Series RG suite
    ${ont_ins}    Build 800ont Testlib    ${dut_session}
    ${e7_ins}    Build E7 Testlib    ${e7_session}
    run keyword unless      "${dut_uplink_ont}"=="0"      P800_config_uplink_device      ${e7_ins}      ${ont_ins}      ${dut_uplink_ethport}        brdg
    set ip for device    ${linux_host}    cafetest    eth1    ${client_ip}
    ${result_restore_default}    Ont Restore Default    ${ont_ins}
    sleep      180

P800_config_uplink_device
    [Arguments]    ${e7_ins}     ${ont_ins}    ${uplink_eth}     ${mode}
    [Documentation]    author:alu.Configure the uplink device to brdg or route mode.
    &{general_conf_uplinkont}=       Create Dictionary    ontid=${dut_uplink_ontid}    vendor=CXNK    ProvisionType=SN    SerialNumber=${dut_uplink_ontsn}    Model=${dut_uplink_model}
    ...       Pots_ports=2    FEPorts=0     GEPorts=4    RG=1    FB=1    RGdefault=y
    ${result}      e7 provision ont      ${e7_ins}       &{general_conf_uplinkont}
    ${result_add_service}=        run keyword if       "${mode}"=="brdg"        E7 add ont L2 service    ${e7_ins}    ${dut_uplink_ontid}    0    ${dut_mgmt_vlan}    ${uplink_eth}
    run keyword if       "${mode}"=="brdg"        log to console      "added first brdg service on uplink device"
    ${result_add_service}=        run keyword if       "${mode}"=="brdg"        E7 add ont L2 ctag service    ${e7_ins}    ${dut_uplink_ontid}    ${dut_data_vlan}
    ...      ${dut_data_vlan}    ${uplink_eth}    Data2
    run keyword if       "${mode}"=="brdg"        log to console      "added data brdg service on uplink device"
    ${result_add_service}=        run keyword if       "${mode}"=="brdg"        E7 add ont L2 ctag service    ${e7_ins}    ${dut_uplink_ontid}    ${dut_iptv_vlan}
    ...     ${dut_iptv_vlan}    ${uplink_eth}     Data3
    ${result_add_service}=        run keyword if       "${mode}"=="brdg"        E7 add ont L2 ctag service    ${e7_ins}    ${dut_mgmt_vlan}    ${dut_mgmt_vlan2}
    ...     ${dut_iptv_vlan}    ${uplink_eth}     Data4
    run keyword if       "${mode}"=="brdg"        log to console      "added iptv service on uplink device"
    ${result_add_service}=        run keyword unless     "${mode}"=="brdg"      E7 add ont rg service    ${e7_ins}    ${dut_uplink_ontid}    ${dut_mgmt_vlan}    ${dut_mgmt_vlan}
    #Should Be True    ${result_add_service}

P800_suite_teardown
    [Arguments]    ${switch_session}    ${device_port}    ${device_vlanid}    ${vm_port}    ${vm_vlanid}
    [Documentation]    author:alu.Configure the switch port after 800 Series CI suite
    Switch_remove_hybrid_port_untag_vlan    ${switch_session}    ${device_port}    ${vm_vlanid}
    run keyword if     "${dut_uplink_ont}"=="0"     Switch_remove_hybrid_port_untag_vlan    ${switch_session}    ${vm_port}    ${device_vlanid}

P800_factory_reset
    [Arguments]    ${dut_session}
    [Documentation]    author:alu. restore the dut to factory default by serial port cmd
    ${result}    Session Command    ${dut_session}    sh
    #${result}    Session Command    ${dut_session}    rm /exa_data/smact_data.json
    #sleep     1
    : FOR    ${i}    IN RANGE    ${5}
    \    ${res}    session command    ${dut_session}    exit
    \    ${status}    ${reg_result}=    Run Keyword And Ignore Error    Should Match Regexp    ${res}    [\\s\\S]*bye[\\s\\S]*
    \    Run Keyword if    '${status}'=='PASS'    Exit For Loop
    \    Sleep    1
    #${result}    Repeat Keyword     3     Session Command    ${dut_session}    exit
    #${result}    Session Command    ${dut_session}    exit
    #Should Match Regexp     ${result}     [\\s\\S]*bye[\\s\\S]*
    ${result}    Session Command    ${dut_session}    restoredefault     timeout=120
    #Should Match Regexp    ${result}    [\\s\\S]*reset[\\s\\S]*
    sleep     150

login ont
    [Documentation]  login ont in ${url} page with ${username} and ${password}
    [Arguments]    ${browser}    ${url}    ${username}    ${password}
    delete all cookies    ${browser}
    go_to_page    ${browser}    ${url}
    #input_text    ${browser}    name=Username    ${username}
    #input_text    ${browser}    name=Password    ${password}
    input_text    ${browser}    xpath=//input[@id="loginuser"]    ${username}
    input_text    ${browser}    xpath=//input[@id="loginpass"]    ${password}
    cpe click    ${browser}    xpath=//*[@id="login"]/div[1]/div/div/div[2]/form/a  
    #cpe click    ${browser}    xpath=//button[contains(., '登入')]
    #//*[@id="login"]/div[1]/div/div/div[2]/form/a
    #cpe click    ${browser}    css=//#login > div.login > div > div > div.col-xs-12.col-sm-8.col-md-6.col-lg-6 > form > a
    page should contain text    ${browser}    Internet

login ont should fail
    [Documentation]  login ont in ${url} page with ${username} and ${password} should be failed
    [Arguments]    ${browser}    ${url}    ${username}    ${password}
    delete all cookies    ${browser}
    go_to_page    ${browser}    ${url}
    input_text    ${browser}    name=Username    ${username}
    input_text    ${browser}    name=Password    ${password}
    cpe click    ${browser}    xpath=//button[contains(., 'Login')]
    page should not contain element    ${browser}    link=Logout

cpe click
    [Documentation]  Click visible element and wait the action finished, ${wait_time} is timeout value for finding element
    [Arguments]    ${browser}    ${locator}    ${search_time}=1.5    ${wait_time}=30
    click visible element    ${browser}    ${locator}
    #run keyword and ignore error  wait action finish    ${browser}    id=darkenScreenObject    ${search_time}    ${wait_time}
    run keyword and ignore error  wait action finish    ${browser}    id=processing_modal   ${search_time}    ${wait_time}

wait action finish
    [Documentation]  Wait action finish by checking element which id is darkenScreenObject is not displayed
    [Arguments]    ${browser}    ${elem_locator}     ${search_time}     ${wait_time}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_wait_time}
    log many    ${search_time}     ${wait_time}
    #${origin_wait_time}    set_implicit_wait_time    ${browser}    ${search_time}
    # check whether the object exist
    ${block_exist}    run keyword and return status    page_should_contain_element    ${browser}    ${elem_locator}
    return from keyword if  ${block_exist}==False
    # wait until element not visible
    #set_implicit_wait_time    ${browser}    ${origin_wait_time}
    run keyword if    ${block_exist}      wait_until_element_is_not_visible    ${browser}    ${elem_locator}    ${wait_time}

factory reset
    [Documentation]  reset the device to factory status
    [Arguments]   ${browser}    ${login_url}
    click links  ${browser}    Support    Factory Reset
    cpe click    ${browser}    xpath=//button[text()="Reset"]
    cpe click    ${browser}    xpath=//button[text()="Ok"]
    sleep    30
    wait until keyword succeeds    5 min    15 sec    ont is login able    ${browser}    ${login_url}

ont is login able
    [Arguments]   ${browser}    ${check_url}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_wait_time}
    close browser     ${browser}
    open browser      ${browser}
    go to page        ${browser}    ${check_url}
    ${origin_wait_time}    set_implicit_wait_time    ${browser}    5
    # page should be login page which contains 'User Name:' or logined page which contains 'Logout'
    ${status}    run keyword and return status    page should contain text    ${browser}    User Name:
    return from keyword if    ${status}==True
    ${status}    run keyword and return status    page should contain text    ${browser}    Logout
    return from keyword if    ${status}==True
    should be true    ${status}

run webgui keyword with timeout
    [Documentation]  Set implicit wait time to ${timeout} before run keyword and reset implicit wait time to its origin value after run the keyword
    [Arguments]  ${timeout}    ${keyword}    ${browser}    @{args}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_timeout}
    ${origin_timeout}    set_implicit_wait_time    ${browser}    ${timeout}
    ${ret}    run keyword    ${keyword}    ${browser}    @{args}
    [Return]  ${ret}

reboot system
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:aijiang] Reboot system via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | reboot system | firefox | http://192.168.1.1 | support | support
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=Reboot
    cpe click    ${browser}    xpath=//button[contains(.,"Reboot")]
    cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    sleep    80
    wait until keyword succeeds    5 min    15 sec    ont is login able    ${browser}    ${ontip}

login and restore default
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:aijiang] login GUI and restore default
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | login and restore default | firefox | http://192.168.1.1 | support | support
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    restore default    ${browser}    ${ontip}

click links
    [Documentation]    Click every link of @{links}
    [Arguments]  ${browser}    @{links}
    :FOR    ${link}    IN    @{links}
    \    cpe click    ${browser}    link=${link}

#delete wan connection
#    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${wan_name}
#    [Documentation]    [Author:aijiang] add a dhcp wan connection via GUI
#    ...
#    ...    Arguments:
#    ...    | =Argument Name= | \ =Argument Value= \ |
#    ...    | browser | browser name setting in your yaml |
#    ...    | ontip | ONT GUI IP |
#    ...    | username | username to login the ONT GUI |
#    ...    | password | password to login the ONT GUI |
#    ...    | wan_name | name of wan connection which you want to delete |
#    ...
#    ...    Example:
#    ...    | delete wan connection | firefox | http://192.168.1.1 | support | support | mgmt_tr069
#    login ont    ${browser}    ${url}    ${username}    ${password}
#    cpe click    ${browser}    link=Support
#    cpe click    ${browser}    link=Service WAN VLANs
#    ${path}    set variable    xpath=//td[contains(., "${wan_name}")]/..//button[contains(.,"Remove")]
#    cpe_click    ${browser}    ${path}
#    wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
#    cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]

Delete Wan Connection
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${wan_name}
    [Documentation]    [Author:alu] delete the connection based on the wan service name
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | url | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | wan_name | name of dhcp wan connection |
    ...
    ...    Example:
    ...    | Change The Wan Connection Admin Status | firefox | http://192.168.1.1 | support | support | DHCP service
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=Service WAN VLANs
    : FOR    ${i}    IN RANGE    ${2}
    \    ${if_wan_exist}      ${status}     Run Keyword And Ignore Error     element should contain    ${browser}    xpath=//table[@id='tab_wan']    ${wan_name}
    \    RUN KEYWORD IF      '${if_wan_exist}'== 'PASS'      cpe click        ${browser}      xpath=//td[contains(., "${wan_name}")]/..//button[contains(., "Remove")]
    \    RUN KEYWORD IF      '${if_wan_exist}'== 'PASS'      wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
    \    RUN KEYWORD IF      '${if_wan_exist}'== 'PASS'      cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    \    RUN KEYWORD IF      '${if_wan_exist}'== 'PASS'      wait until keyword succeeds    10x    2s   element should not contain    ${browser}    xpath=//table[@id='tab_wan']    ${wan_name}



factory reset via console
    [Arguments]    ${dut_session}    ${browser}    ${login_url}
    [Documentation]    Factory reset the device and wait until it reboot end
    P800_factory_reset    ${dut_session}
    wait until keyword succeeds    5 min    15 sec    ont is login able    ${browser}    ${login_url}
    # when GUI is loginable, some service still starting, so wait some times...
    sleep    10


add dns host mapping
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}    ${hostname}    ${ipaddress}
    [Documentation]    [Author:aijiang] Add dns host mapping via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | hostname | hostname of ipaddress |
    ...    | ipaddress | ipaddress need to be provisioned |
    ...
    ...    Example:
    ...    | add dns host mapping | firefox | http://192.168.1.1 | support | support | www.ctest.com | 10.20.1.100
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Advanced
    cpe click    ${browser}    link=IP Addressing
    cpe click    ${browser}    link=DNS Host Mapping
    input text    ${browser}    id=Hostname    ${hostname}
    input text    ${browser}    id=IPAddress    ${ipaddress}
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

reomve dns host mapping
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}    ${hostname}
    [Documentation]    [Author:aijiang] Remove dns host mapping via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | hostname | hostname need to be deprovisioned |
    ...
    ...    Example:
    ...    | reomve dns host mapping | firefox | http://192.168.1.1 | support | support | a.com
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Advanced
    cpe click    ${browser}    link=IP Addressing
    cpe click    ${browser}    link=DNS Host Mapping
    ${path}    set variable    xpath=//td[contains(., "${hostname}")]/..//button
    cpe_click    ${browser}    ${path}
    wait until keyword succeeds    10x    2s    element_should_not_contain    ${browser}    xpath=//table[@id="dnsHostMappingTable"]    ${hostname}


create DHCP wan connection
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${wan_name}    ${vlan_id}     ${priority}=0    ${flag_default_gateway}=0    ${igmp_status}=disabled    ${ipv4_nat_status}=disabled
    [Documentation]    [Author:aijiang] add a dhcp wan connection via GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | wan_name | name of dhcp wan connection |
    ...    | vlan_id | vlan of dhcp wan connection |
    ...    | priority | priority of vlan, default value is 0 |
    ...    | flag_default_gateway | flag of default gateway, default value is 0, invalid value,0 or 1 |
    ...    | igmp_status | igmp status of wan connection, default value is disabled, invalid value:enabled disable  |
    ...    | ipv4_nat_status | nat status of wan connection, default value is disabled, invalid value:enabled disable |
    ...
    ...    Example:
    ...    | create DHCP wan connection | firefox | http://192.168.1.1 | support | support | mgmt-tr069 | 100
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=Service WAN VLANs
    ### create DHCP WAN
    cpe click    ${browser}    xpath=//button[text()='New']
    input text    ${browser}    id=service_label    ${wan_name}
    # fill vlan info
    select_radio_button    ${browser}    VLAN_config    tagged
    input text    ${browser}    id=vlan_config_vlan_id    ${vlan_id}
    input text    ${browser}    id=vlan_config_priority    ${priority}

    select_radio_button    ${browser}    is_dcs    ${flag_default_gateway}

    select_radio_button    ${browser}    ipv4_mode    dhcp

    select_radio_button    ${browser}    ipv4_igmp    ${igmp_status}

    select_radio_button    ${browser}    ipv4_nat    ${ipv4_nat_status}

    cpe_click    ${browser}    xpath=//button[text()='Apply']

    # get table cell location which contain the vlan just created
    @{location}    run webgui keyword with timeout    1    get_table_cell_contains_content    ${browser}    xpath=//table[@id='tab_wan']        ${wan_name}

    # verify vlan id
    ${page_vlan_id}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    2
    ${page_vlan_id_int}    convert to integer    ${page_vlan_id}
    should be equal as strings      ${page_vlan_id_int}    ${vlan_id}

    ${page_priority}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    4
    ${page_priority_int}    convert to integer    ${page_priority}
    should be equal as strings     ${page_priority_int}    ${priority}

Edit wan connection
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${wan_name}     ${vlan_id}     ${priority}=0      ${flag_default_gateway}=0
    ...         ${ipv4_mode}=dhcp      ${igmp_status}=disabled      ${ipv4_nat_status}=disabled       ${ipv4_dns_mode}=auto
    [Documentation]    [Author:alu] edit a dhcp wan connection via GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | wan_name | name of wan connection which you want to delete |
    ...
    ...    Example:
    ...    | delete wan connection | firefox | http://192.168.1.1 | support | support | mgmt_tr069
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=Service WAN VLANs
    ${path}    set variable    xpath=//td[contains(., "${wan_name}")]/..//button[contains(.,"Edit")]
    cpe_click    ${browser}    ${path}
    select_radio_button    ${browser}    VLAN_config    tagged
    input text    ${browser}    id=vlan_config_vlan_id    ${vlan_id}
    input text    ${browser}    id=vlan_config_priority    ${priority}
    select_radio_button    ${browser}    is_dcs    ${flag_default_gateway}
    select_radio_button    ${browser}    ipv4_mode    ${ipv4_mode}
    select_radio_button    ${browser}    ipv4_igmp    ${igmp_status}
    select_radio_button    ${browser}    ipv4_nat    ${ipv4_nat_status}
    select_radio_button    ${browser}    ipv4_name_server_mode    ${ipv4_dns_mode}
    cpe_click    ${browser}    xpath=//button[text()='Apply']
     # get table cell location which contain the vlan just created
    @{location}    run webgui keyword with timeout    1    get_table_cell_contains_content    ${browser}    xpath=//table[@id='tab_wan']        ${wan_name}

    # verify vlan id
    ${page_vlan_id}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    2
    ${page_vlan_id_int}    convert to integer    ${page_vlan_id}
    should be equal as strings      ${page_vlan_id_int}    ${vlan_id}

    ${page_priority}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    4
    ${page_priority_int}    convert to integer    ${page_priority}
    should be equal as strings     ${page_priority_int}    ${priority}

verify table cell by column name
    [Arguments]      ${browser}    ${table_locator}    ${row_index}    ${column_name}    ${expected_value}    ${cell_search_timeout}=1
    @{loc}     run webgui keyword with timeout    ${cell_search_timeout}    get_table_cell_contains_content    ${browser}    ${table_locator}        ${column_name}
    ${page_value}    run webgui keyword with timeout    ${cell_search_timeout}    get table cell    ${browser}    xpath=//table[@id='tab_wan']    ${row_index}    @{loc}[1]
    should be equal as strings     ${page_value}    ${expected_value}

Create the L2-bridge WAN
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${vlan_name}    ${vlan_id}   ${priority}    ${lan_port}    ${igmp_status}
    [Documentation]    [Author:bfan] add a L2 bridge video wan
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | url | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | vlan_name | name of dhcp wan connection |
    ...    | vlan_id | the l2-bridge VLAN |
    ...    | priority | the pbit of the VLAN|
    ...
    ...    Example:
    ...    | Create the L2-bridge video WAN | firefox | http://192.168.1.1 | support | support | l2-bridge wan | 100 | 4
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click     ${browser}    link=Support
    cpe click    ${browser}     link=Service WAN VLANs
    #click links    ${browser}    Support    Service WAN VLANs
    ### create DHCP WAN
    cpe click    ${browser}    xpath=//button[text()='New']
    # Connection Admin Status :
    select_radio_button    ${browser}    conn_admin_status    enabled
    # Define Service VLAN :
    input text    ${browser}    id=service_label    ${vlan_name}
    # VLAN Configuration :
    select_radio_button    ${browser}    VLAN_config    tagged
    # VLAN ID [1-4093] :
    input text    ${browser}    id=vlan_config_vlan_id    ${vlan_id}
    # Priority [0-7] :
    input text    ${browser}    id=vlan_config_priority    ${priority}
    # Dscp To Pbit :
    select_radio_button    ${browser}    dscp2pbit_enabled    disabled
    # Connection Type :
    select_radio_button    ${browser}    conn_type    layer2bridged

    #config L2 bridge
    select from list by label    ${browser}    id=l2bridgeSelObj    ${lan_port}

    #enable IGMP in L2-bridge WAN
    select_radio_button    ${browser}    ipv4_igmp    ${igmp_status}

    # Apply
    cpe_click    ${browser}    xpath=//button[text()='Apply']
    #sleep      2
    #get table cell location which contain the vlan just created
    @{location}    run webgui keyword with timeout    1    get_table_cell_contains_content    ${browser}    xpath=//table[@id='tab_wan']        ${vlan_name}

    # verify vlan id
    verify table cell by column name    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    VID     ${vlan_id}

    # verify priority
    verify table cell by column name    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    Priority     ${priority}

    # verify connection type
    verify table cell by column name    ${browser}    xpath=//table[@id='tab_wan']    @{location}[0]    Connection Type    L2 Bridged


successfully exit cli
    [Arguments]    ${device}
    ${res}=    cli    ${device}    exit
    should contain    ${res}    nice day

GenerateNameBaseTime
    [Arguments]        ${linux_session}
    [Documentation]    Return a file name based on the system current time of Linux
    cli                ${linux_session}         sh
    ${datestring}      cli                      ${linux_session}     date +%s
    @{filenames}       Get Regexp Matches       ${datestring}        [\\d]{10,11}
    ${filename}        set variable             file@{filenames}[0]
    cli                ${linux_session}         exit
    [Return]           ${filename}

Get WAN IP_MAC_interface_name
    [Arguments]    ${dut_session}    ${wan_name}
    [Documentation]    [Author:bfan] get the wan ip address, mac address,interface name based on the wan service name
    ${list}    Create list
    wait until keyword succeeds    10x    1s    successfully exit cli    ${dut_session}
     ${result1}    cli    ${dut_session}    wan show
    log    ${result1}
    ${lines}=    get lines containing string    ${result1}    ${wan_name}
    log to console    ${lines}

    #Get the wan ip address by above output
    ${wan_ip_address}=    Should Match Regexp    ${lines}    \\d+\\.\\d+\\.\\d+\\.\\d+
    log to console    ${wan_ip_address}

    #Get the wan interface name by above output
    ${wan_interface_name}=    Should Match Regexp    ${lines}    \\s[A-Za-z]{3,5}\[0-9]+\\.\[0-9]
    log to console         ${wan_interface_name}

    #Get the wan mac address by interface name
#    ${result2}    cli  ${dut_session}     ifconfig ${wan_interface_name}
    ${result2}    cli  ${dut_session}     ifconfig ${wan_interface_name}
    log to console    ${result2}
    ${wan_mac_address}    Should Match Regexp    ${result2}    [0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}
    #${wan_mac_address}    Should Match Regexp    ${result2}     ([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}
    log to console    ${wan_mac_address}

    Append to list    ${list}    ${wan_ip_address}    ${wan_mac_address}    ${wan_interface_name}
    [Return]    ${list}

Provison TR69 Parameters
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${acs_url}    ${tr069_username}    ${tr069_password}    ${tr069_periodic_inform_interval}    ${tr069_wan_name}
    [Documentation]    [Author:bfan] Provision TR69 parameters
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    input text    ${browser}    id=acs_url_field    ${acs_url}
    input text    ${browser}    id=username_field    ${tr069_username}
    input text    ${browser}    id=password_password_field    ${tr069_password}
    select_radio_button    ${browser}    periodic_inform_state_enable    periodic_inform_state_enabled_radio
    input text    ${browser}    id=periodic_inform_interval_field   ${tr069_periodic_inform_interval}
    select from list by label    ${browser}    id=tr069_ifname    ${tr069_wan_name}
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ProvisonTR69EditWAN
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${acs_url}    ${tr069_username}    ${tr069_password}    ${tr069_periodic_inform_interval}    ${tr069_wan_name}
    [Documentation]    [Author:bfan] Provision TR69 parameters
    login ont              ${browser}    ${url}    ${username}    ${password}
    cpe click              ${browser}    link=Support
    cpe click              ${browser}    link=Service WAN VLANs
    cpe click              ${browser}    xpath=//button[text()='Edit']
    input text             ${browser}    id=service_label                ${tr069_wan_name}
    select_radio_button    ${browser}    conn_admin_status               enabled
    select_radio_button    ${browser}    VLAN_config                     tagged
    input text             ${browser}    id=vlan_config_vlan_id          ${dut_mgmt_vlan}
    input text             ${browser}    id=vlan_config_priority         1
    select_radio_button    ${browser}    framing                         IPoE
    select_radio_button    ${browser}    ipv4_name_server_mode           auto
    select_radio_button    ${browser}    ipv4_remote                     enabled
    cpe_click              ${browser}    xpath=//button[text()='Apply']
    cpe click              ${browser}    link=TR-069
    input text    ${browser}    id=acs_url_field    ${acs_url}
    input text    ${browser}    id=username_field    ${tr069_username}
    input text    ${browser}    id=password_password_field    ${tr069_password}
    select_radio_button    ${browser}    periodic_inform_state_enable    periodic_inform_state_enabled_radio
    input text    ${browser}    id=periodic_inform_interval_field   ${tr069_periodic_inform_interval}
    select from list by label    ${browser}    id=tr069_ifname    ${tr069_wan_name}
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]


hpingtcl
    [Arguments]         ${linux_session}     @{args}
    [Documentation]     This function will take the args as the hping tcl script line, it will generate a tcl hping file, and excute the script file on the linux_session

    #Generate the script name based current time
    ${filename}    GenerateNameBaseTime      ${linux_session}
    ${path}        ${file}                   split path             ${SUITE_SOURCE}
    ${script}      join path                 ${path}                ${filename}.htcl

    #Create the content of scrits according to the arguments
    :FOR           ${line}                   IN                     @{args}
    \              Append To File            ${script}              ${line}\n

    #Excute the script by hping3
    cli            ${linux_session}          sh
    ${output}      cli                       ${linux_session}       sudo hping3 exec ${script}
    cli            ${linux_session}          exit

    #Remove the script file
    Remove File    ${script}

    [Return]       ${output}


TR69_ccplus_cc_cpe
    [Arguments]    ${linux_shell}    ${DUT_sn}
    [Documentation]    [Author:xlai] Description: check if cpe managed by ccplus
    ${result}    cli    ${linux_shell}    curl -X GET "${g_cc_acs_server}/cc/device?orgId=${g_org_id}&serialNumber=${DUT_sn}"    \\}    10
    should match regexp    ${result}    id.+${DUT_sn}

TR69_ccplus_connected
    [Arguments]    ${DUT_sn}    ${linux_shell}
    [Documentation]    [Author:xlai] Description: check if cpe can connected to ccplus after configuration
    ${result}=    Wait Until Keyword Succeeds    20x    10s    TR69_ccplus_cc_cpe    ${linux_shell}    ${DUT_sn}

TR69_ccplus_delete_cpe
    [Arguments]    ${DUT_sn}    ${linux_shell}
    [Documentation]    [Author:xlai] Description: delete cpe from ccplus
    ${result}    cli    ${linux_shell}    curl -X DELETE "${g_cc_acs_server}/cc/device?orgId=${g_org_id}&serialNumber=${DUT_sn}"



Edit the default WAN IP and DNS
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${ip_address}    ${gateway}    ${subnet_mask}    ${premary dns}    ${secondary dns}
    [Documentation]  [Author:bfan]  Edit the defautl wan
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=Service WAN VLANs
    cpe click    ${browser}    xpath=//button[contains(., "Edit")]
    select radio button    ${browser}    ipv4_mode    static
    input text    ${browser}    xpath=//input[@id='static_ip_addr']    ${ip_address}
    input text    ${browser}    xpath=//input[@id='static_gateway']    ${gateway}
    input text    ${browser}    xpath=//input[@id='static_subnet_mask']    ${subnet_mask}

    select radio button    ${browser}    ipv4_name_server_mode    static
    input text    ${browser}    xpath=//input[@id='ipv4_primary_dns_field']    ${premary dns}
    input text    ${browser}    xpath=//input[@id='ipv4_secondary_dns_field']    ${secondary dns}

    cpe click    ${browser}    xpath=//button[contains(., "Apply")]

TR069_get_value_on_mdm
    [Arguments]    ${dut_session}    ${p_varible}
    [Documentation]  [Author:deding]  get value on mdm
    wait until keyword succeeds    10x    1s    successfully exit cli    ${dut_session}
    ${res}=    cli    ${dut_session}    mdm getpv ${p_varible}
    @{result}=    Get Regexp Matches    ${res}    .*Param value=(.*)\\r\\(Param.*      1
    log to console    @{result}[0]
    [Return]  @{result}

Incr IP Address
    [Arguments]        ${IP_Address}
    @{digital_list}    Split String      ${IP_Address}      .
    ${digital4}        Evaluate          @{digital_list}[3] + 1
    ${digital3}        Evaluate          @{digital_list}[2] + 1
    ${digital2}        Evaluate          @{digital_list}[1] + 1
    ${digital1}        Evaluate          @{digital_list}[0] + 1
    ${next}            Run Keyword If    ${digital4} < 255     set variable     @{digital_list}[0].@{digital_list}[1].@{digital_list}[2].${digital4}
    ...                ELSE IF           ${digital3} < 256     set variable     @{digital_list}[0].@{digital_list}[1].${digital3}.1
    ...                ELSE IF           ${digital2} < 256     set variable     @{digital_list}[0].${digital2}.0.1
    ...                ELSE IF           ${digital1} < 255     set variable     ${digital1}.0.0.1
    ...                ELSE              set variable          nonext
    [Return]           ${next}

set igmp version
    [Arguments]    ${browser}    ${version}=3
    [Documentation]    [Author:aijiang] set igmp max multicast limits
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | version | igmp version need to set, 1 for IGMPv1, 2 for IGMPv2 and 3 for IGMPv3 |
    ...
    ...    Example:
    ...    | set igmp version| firefox | 2
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=IGMP
    select from list by value    ${browser}    id=igmpVerSelObj    ${version}
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

set igmp snooping status
    [Arguments]    ${browser}    ${status}
    [Documentation]    [Author:aijiang] set igmp snooping status
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | status | status need to set: enable or disable |
    ...
    ...    Example:
    ...    | set igmp snooping status | firefox | enable
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=IGMP
    run keyword if    '${status}' == 'enable'    select checkbox    ${browser}    id=EnableIGMPSnoopFuncCheckBoxObj
    ...    ELSE    unselect checkbox    ${browser}     id=EnableIGMPSnoopFuncCheckBoxObj
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

set igmp query interval
    [Arguments]    ${browser}    ${query_interval}    ${response_interval}=100    ${last_member_query_interval}=10
    [Documentation]    [Author:aijiang] set igmp igmp query interval
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | query_interval | gerneal query interval,  unit s|
    ...    | response_interval | response interval for general query,  unit 0.1s|
    ...    | last_member_query_interval | last member quert interval,  invalid for IGMPv1, unit 0.1s|
    ...
    ...    Example:
    ...    | set igmp query interval | firefox | 125 | 50 | 20
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=IGMP
    input text    ${browser}    id=queryIntervalTxtObj    ${query_interval}
    input text    ${browser}    id=queryIntervalRespTxtObj    ${response_interval}
    input text    ${browser}    id=LastMemberQueryIntervalTxtObj    ${last_member_query_interval}
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

get genquerytx value
    [Arguments]    ${browser}    ${igmp_version_no}
    [Documentation]    [Author:aijiang] get genquerytx value
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | igmp_version_no | igmp version NO|
    ...
    ...    Example:
    ...    | get genquerytx value | firefox | 3
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=IGMP
    cpe click    ${browser}    link=IGMP Statistics
    ${general_query_count}    run webgui keyword with timeout    1    get table cell    ${browser}
    ...   xpath=(//p[contains(., "LAN Interface Counters")]/..//table)[3]    3    ${igmp_version_no}
    [Return]    ${general_query_count}

set fast leave status
    [Arguments]    ${browser}    ${status}
    [Documentation]    [Author:aijiang] set fast leave state
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | status | status need to set, enable or disable |
    ...
    ...    Example:
    ...    | set fast leave status | firefox | enable
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=IGMP
    run keyword if    '${status}' == 'enable'    select checkbox    ${browser}    id=FastLeavesEnableCheckBoxObj
    ...    ELSE    unselect checkbox    ${browser}    id=FastLeavesEnableCheckBoxObj
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

Ont Exit From Sh
    [Arguments]    ${dut_session}
    [Documentation]    [Author:alu] exit 800 Series ONT to BCM CLI
    #Should Be True    ${result_add_service}
    : FOR    ${i}    IN RANGE    ${5}
    \    ${outputs}       cli  ${dut_session}  exit
    \    ${status}    ${reg_result}=    Run Keyword And Ignore Error    Should Match Regexp    ${outputs}    Bye[\\d]+
    \    Run Keyword if    '${status}'=='PASS'    Exit For Loop


844 shell cli
    [Arguments]  ${dut}   @{args}
    [Teardown]  ont exit from sh  ${dut}
    [Return]  ${result}
    cli  ${dut}   sh   prompt=~\\\s#   timeout=20
    ${result}  cli  ${dut}   @{args}   prompt=~\\\s#   timeout=20
