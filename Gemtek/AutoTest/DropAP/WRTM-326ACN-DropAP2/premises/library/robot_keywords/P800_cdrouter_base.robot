*** Settings ***
Resource          caferobot/cafebase.robot
Resource          premises/library/robot_keywords/common/E7_base.robot
Resource          premises/library/robot_keywords/common/P800_python_kwd.robot
Resource          premises/test_suites/P800_series/P800_GUI/keyword/webgui_kw.robot
 
*** Variables ***

*** Keywords ***
ONT_login_gui
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang] login 800G/800E GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_login_gui | firefox | http://192.168.1.1 | support | support |
    delete all cookies    ${browser}
    go to page    ${browser}    ${ontip}/login.html
    input text    ${browser}    name=Username    ${username}
    input text    ${browser}    name=Password    ${password}
    cpe click    ${browser}    xpath=//button[contains(., "Login")]
    page_should_contain_element    ${browser}    link=Logout

ONT_login_main_menu
    [Arguments]    ${browser}    ${ontip}    ${mainmenu}    ${username}    ${password}
    [Documentation]    [Author:blwang]  login 800G/800E GUI main menu Status/Quick Start/Wireless/Utilities/Advanced/Support
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | mainmenu | mainmenu of ONT GUI |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_login_main_menu | firefox | http://192.168.1.1 | Advanced | support | support |
    ONT_login_gui    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}     link=${mainmenu}


ONT_provision_dmz
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}    ${dmzhost}
    [Documentation]    [Author:blwang]  config DMZ Hosting
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
	...    | dmzhost | dmzhost ip |
    ...
    ...    Example:
    ...    | ONT_provision_dmz | firefox | http://192.168.1.1 | support | support | 192.168.1.253 |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}     link=Security
    cpe click    ${browser}     link=DMZ Hosting
    select radio button     ${browser}    dmz    on
    radio button should be set to     ${browser}    dmz    on
    select radio button    ${browser}    devicetype    2
    radio button should be set to     ${browser}    devicetype    2
    input text    ${browser}    name=ip_address     ${dmzhost}
    cpe click    ${browser}    xpath=//button[contains(., "Apply")]

ONT_deprovision_dmz
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  Deprovision DMZ Hosting
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_deprovision_dmz | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}     link=Security
    cpe click    ${browser}    link=Firewall
    select radio button     ${browser}    firewall_security_level    Basic
    radio button should be set to     ${browser}    firewall_security_level    Basic
    cpe click    ${browser}    xpath=//button[contains(., "Apply")]
    cpe click    ${browser}     link=DMZ Hosting
    cpe click    ${browser}    xpath=//button[contains(., "Remove")]

ONT_provision_igmp
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  provision IGMPv3
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_provision_igmp | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}     link=IGMP
    cpe click    ${browser}     link=IGMP Setup
    select_from_list_by_index    ${browser}    xpath=//select[@id="igmpVerSelObj"]    2
    ${value}=    get_selected_list_value    ${browser}    xpath=//select[@id="igmpVerSelObj"]
    should be equal    ${value}    3
    input text    ${browser}    id=queryIntervalTxtObj    120
    input text    ${browser}    id=queryIntervalRespTxtObj    100
    input text    ${browser}    id=RobustnessValueTxtObj    1
    input text    ${browser}    id=MaxMultiGrpsTxtObj    32
    select checkbox    ${browser}    xpath=//input[@id="FastLeavesEnableCheckBoxObj"]
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_provision_firewalloutbound
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  provision firewall outbound
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_provision_firewalloutbound | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Security
    cpe click    ${browser}    link=Firewall
    select radio button     ${browser}    firewall_security_level    High
    radio button should be set to     ${browser}    firewall_security_level    High
#    click element    ${browser}    xpath=//button[@class="expand-collapse")]
    cpe click    ${browser}    xpath=//h1[text()="Blocked Services"]/parent::div//button
    select checkbox    ${browser}    xpath=//input[@id="ps23_out"]
    select checkbox    ${browser}    xpath=//input[@id="sftp_out"]
    select checkbox    ${browser}    xpath=//input[@id="pptp_out"]
    cpe click    ${browser}    xpath=//button[contains(., "Apply")]

ONT_deprovision_firewalloutbound
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  deprovision firewall outbound
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_deprovision_firewalloutbound | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Security
    cpe click    ${browser}    link=Firewall
    select radio button     ${browser}    firewall_security_level    Low
    radio button should be set to     ${browser}    firewall_security_level    Low
    cpe click    ${browser}    xpath=//button[contains(., "Apply")]


ONT_provision_URLFILTER
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  provision urlfilter
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_provision_URLFILTER | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Scheduling and Blocking
#    sleep    5
    cpe click    ${browser}    link=Website Blocking
    cpe click    ${browser}    xpath=//button[contains(.,"New")]
    input text    ${browser}    xpath=//label[text()="Website Address:"]/parent::div//input    http://www.gmail.com
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_deprovision_URLFILTER
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  deprovision urlfilter on 800G/800E GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_deprovision_URLFILTER | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Scheduling and Blocking
    cpe click    ${browser}    link=Website Blocking
    cpe click    ${browser}    xpath=//button[contains(.,"Remove")]
    cpe click    ${browser}    xpath=//button[contains(.,"Ok")]

ONT_provision_StaticRouting
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  provision static routing on 800G/800E GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_provision_StaticRouting | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Static Routing
    input text    ${browser}    xpath=//label[text()="Destination IP:"]/parent::div//input    192.168.14.0
    input text    ${browser}    xpath=//label[text()="Subnet Mask:"]/parent::div//input    255.255.255.0
    input text    ${browser}    xpath=//label[text()="Gateway IP:"]/parent::div//input    192.168.1.244
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]
    input text    ${browser}    xpath=//label[text()="Destination IP:"]/parent::div//input    192.168.12.0
    input text    ${browser}    xpath=//label[text()="Subnet Mask:"]/parent::div//input    255.255.255.0
    input text    ${browser}    xpath=//label[text()="Gateway IP:"]/parent::div//input    192.168.1.243
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_deprovision_StaticRouting
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  deprovision static routing on 800G/800E GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_deprovision_StaticRouting | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=Static Routing
    cpe click    ${browser}    xpath=//button[contains(.,"Remove")]
    cpe click    ${browser}    xpath=//button[contains(.,"Remove")]

ONT_PPPoE_provision
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  Config PPPoE via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_PPPoE_provision | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}    link=Service WAN VLANs
    cpe click    ${browser}    xpath=//button[contains(.,"Edit")]
    select radio button     ${browser}    framing    PPPoE
    radio button should be set to     ${browser}    framing    PPPoE
    input text    ${browser}    xpath=//span[text()="User Name : "]/parent::div//input    qacafe
    input text    ${browser}    xpath=//span[text()="Password : "]/parent::div//input    admin
    cpe click   ${browser}    xpath=//button[contains(.,"Apply")]

ONT_PPPoE_deprovision
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  deprovision PPPoE config via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_PPPoE_deprovision | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}    link=Service WAN VLANs
    cpe click    ${browser}    xpath=//button[contains(.,"Edit")]
    select radio button     ${browser}    framing    IPoE
    radio button should be set to     ${browser}    framing    IPoE
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_Dynamic_DNS_provision
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  provision dynamic dns via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_Dynamic_DNS_provision | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=IP Addressing
    cpe click    ${browser}    link=Dynamic DNS
    select radio button     ${browser}    ddnsEnable    ddns_enabled_radio
#    radio button should be set to     ${browser}    ddnsEnable    ddns_enabled_radio
    input text    ${browser}    xpath=//label[text()="Username:"]/parent::div//input    qacafe
    input text    ${browser}    xpath=//label[text()="Password:"]/parent::div//input[@id="password_password_field"]    qacafe123
    input text    ${browser}    xpath=//label[text()="Dynamic DNS hostname:"]/parent::div//input    test.domain.com
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_Dynamic_DNS_deprovision
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  provision dynamic dns via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_Dynamic_DNS_deprovision | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Advanced    ${username}    ${password}
    cpe click    ${browser}    link=IP Addressing
    cpe click    ${browser}    link=Dynamic DNS
    select radio button     ${browser}    ddnsEnable    ddns_disabled_radio
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_TR069_http
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  provision tr069 http via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_TR069_http | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}    link=TR-069
    input text    ${browser}    xpath=//label[text()="ACS URL:"]/parent::div//input    6.0.0.1
    input text    ${browser}    xpath=//label[text()="Username:"]/parent::div//input    admin
    input text    ${browser}    xpath=//label[text()="Password:"]/parent::div//input[@id="password_password_field"]   admin
    select radio button     ${browser}    periodic_inform_state_enable    periodic_inform_state_enabled_radio
    input text    ${browser}    xpath=//label[text()="Periodic Inform Interval:"]/parent::div//input    100
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

ONT_TR069_https
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]   [Author:blwang]  provision tr069 http via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_TR069_https | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}    link=TR-069
    input text    ${browser}    xpath=//label[text()="ACS URL:"]/parent::div//input    https://acs.qacafe.com
    input text    ${browser}    xpath=//label[text()="Username:"]/parent::div//input    admin
    input text    ${browser}    xpath=//label[text()="Password:"]/parent::div//input[@id="password_password_field"]   admin
    select radio button     ${browser}    periodic_inform_state_enable    periodic_inform_state_enabled_radio
    input text    ${browser}    xpath=//label[text()="Periodic Inform Interval:"]/parent::div//input    100
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]

E7_add_port_to_vlan
    [Arguments]    ${device}    ${vlan_id}    ${e7_us_port}    ${e7_eth_port}
    [Documentation]    Add basic RG service via ONT GUI
    E7_create_vlan    ${device}    ${vlan_id}
    E7_prov_port    ${device}    ${e7_us_port}    ${vlan_id}   trunk
    E7_prov_port    ${device}    ${e7_eth_port}    ${vlan_id}   trunk


ONT_basic_provision
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:blwang]  Add basic RG service via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
	...    | username | username to login the ONT GUI |
	...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | ONT_basic_provision | firefox | http://192.168.1.1 | support | support |
    ONT_login_main_menu    ${browser}    ${ontip}    Support    ${username}    ${password}
    cpe click    ${browser}    link=Service WAN VLANs
    cpe click    ${browser}    xpath=//button[contains(.,"Edit")]
    input text    ${browser}    xpath=//label[text()="Service VLAN Label : "]/parent::div//input    ipoe-veip0-CDR
    select radio button     ${browser}    VLAN_config    tagged
    radio button should be set to     ${browser}    VLAN_config    tagged
    input text    ${browser}    xpath=//label[text()="VLAN ID [1-4093] : "]/parent::div//input    666
    input text    ${browser}    xpath=//label[text()="Priority [0-7] : "]/parent::div//input    0
    select radio button     ${browser}    conn_type    layer3routed
    radio button should be set to     ${browser}    conn_type    layer3routed
    select radio button     ${browser}    is_dcs    1
    radio button should be set to     ${browser}    is_dcs    1
    select radio button     ${browser}    framing    IPoE
    radio button should be set to     ${browser}    framing    IPoE
    select radio button     ${browser}    ipv4_mode    dhcp
    radio button should be set to     ${browser}    ipv4_mode    dhcp
    select radio button     ${browser}    ipv4_igmp    enabled
    radio button should be set to     ${browser}    ipv4_igmp    enabled
    select radio button     ${browser}    ipv4_name_server_mode    auto
    radio button should be set to     ${browser}    ipv4_name_server_mode    auto
    cpe click    ${browser}    xpath=//button[contains(.,"Apply")]
