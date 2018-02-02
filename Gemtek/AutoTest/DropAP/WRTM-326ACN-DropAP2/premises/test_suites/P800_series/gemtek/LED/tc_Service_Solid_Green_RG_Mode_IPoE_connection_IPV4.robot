*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Jujung_Chang    stable

Suite Setup    Run keywords    Enter Shell Mode And Cisco Prejob Config
Suite Teardown  Run keywords    Exit Shell Mode And Cisco

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${times}    3
${vlan}    913
${priority}    0
${gateway_ip}    1.1.1.254
${dut_gw}    192.168.1.1
*** Test Cases ***
tc_Service_Solid_Green_RG_Mode_IPoE_connection_IPV4
    [Documentation]   tc_Service_Solid_Green_RG_Mode_IPoE_connection_IPV4
    ...    1.If physical line is connection ,then status will show 'connected'.
    ...    2.And CPE will received a IPv4 IP.
    [Tags]   @TCID=PREMS-TC-7882   @globalid=1597602LED844F   @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Jujung_Chang
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    web    conn_admin_status    enabled
    select radio button    web    VLAN_config    tagged
    #set vlan id is 913
    input_text    web    id=vlan_config_vlan_id    ${vlan}
    #priority is 0
    input_text    web    id=vlan_config_priority    ${priority}
    select radio button    web    version    ipv4
    select radio button    web    framing    IPoE

    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    5s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    #Check IPv4 Internet Access status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connected
    #Check IPv4 IP Address if DHCP server allocate ip to device
    ${my_ip} =    Wait Until Keyword Succeeds     5x    2s    Get Non Empty Cell Value    web    xpath=//table[@id='gateway_tab']    9    2
    log    ${my_ip}

    #Go to Internet Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Internet
    #check getway ip by checking cell value
    ${gateway_ip} =    Wait Until Keyword Succeeds    10x    1s     Get Non Empty Cell Value    web    xpath=//table[@id='ipv4_addr_tab_obj']    6    2
    log    ${gateway_ip}

    #check led register green is on
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED On in Certain Tries    n1
    log    ${result}
    Should Be Equal    ${result}    0
    #check led register red is off
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED Off in Certain Tries    n1
    log    ${result}
    Should Be Equal    ${result}    1

*** Keywords ***
Check LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Service_green_off_on Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check LED Off in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Service_red_off_on Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    1
    [Return]    ${result}

Get Service_green_off_on Register Value
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{6}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{1}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

Get Service_red_off_on Register Value
    [Arguments]    ${device}
    [Documentation]    when red on Register Value is 174adfef  => should retrive third hex: 4->0100, bit 21 is 0
    ...                when red off Register Value is 176adfef  => should retrive third hex: 6->0110, bit 21 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{2}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{2}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

Enter Shell Mode And Cisco Prejob Config
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    Wait Until Keyword Succeeds    3x   10 sec    cli    n1    sh
    #cisco prejob config
    Wait Until Keyword Succeeds    3x   10 sec    cli    cisco_ip_server    enable    C1800-DHCP#
    cli    cisco_ip_server    terminal length 0    C1800-DHCP#
    cli    cisco_ip_server    config t    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    no logging console    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    line console 0    C1800-DHCP\\(config-line\\)#
    cli    cisco_ip_server    no exec-timeout    C1800-DHCP\\(config-line\\)#
    cli    cisco_ip_server    exit    C1800-DHCP\\(config\\)#

    #no shutdown fastethernet 6
    cli    cisco_ip_server    interface range fastEthernet 6    C1800-DHCP\\(config-if-range\\)#
    cli    cisco_ip_server    no sh    C1800-DHCP\\(config-if-range\\)#
    ${ret}    cli    cisco_ip_server    do show ip int brief FastEthernet6     C1800-DHCP\\(config-if-range\\)#
    log   ${ret}
    Should Contain    ${ret}    up

Exit Shell Mode And Cisco
    [Arguments]
    [Documentation]     Exit CPE shell mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    cli    n1    exit
    cli    cisco_ip_server    exit    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    exit    C1800-DHCP#
