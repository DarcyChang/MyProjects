*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Jujung_Chang    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown  Run keywords    Exit Shell Mode

*** Variables ***
${844fb_gui_session}    web
${844fb_dump_led_register}     dw fffe8114
${times}    10
${vlan}    913
${priority}    0
${gateway_ip}    0
${count_service_green_on}    0
${count_service_green_off}    0
*** Test Cases ***
tc_Service_Flashing_Green_Activity_RG_Mode_connected_and_traffic_IPV4
    [Documentation]   tc_Service_Flashing_Green_Activity_RG_Mode_connected_and_traffic_IPV4
    ...    1.If physical line is connection ,then status will show 'connected'.
    ...    2.And CPE will received a IPv4 IP.
    ...    3.When starting traffic, green LED will flashing.
    [Tags]   @TCID=PREMS-TC-7878   @globalid=1597598LED844F   @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Jujung_Chang
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
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    20x    2s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    #Check IPv4 Internet Access status by checking cell value
    Wait Until Keyword Succeeds    20x    2s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connected
    #Check IPv4 IP Address if DHCP server allocate ip to device
    ${my_ip} =    Wait Until Keyword Succeeds     5x    2s    Get Non Empty Cell Value    web    xpath=//table[@id='gateway_tab']    9    2
    log    ${my_ip}

    #Go to Internet Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Internet
    #check getway ip by checking cell value
    ${gateway_ip} =    Wait Until Keyword Succeeds    5x    1s     Get Non Empty Cell Value    web    xpath=//table[@id='ipv4_addr_tab_obj']    6    2
    log    ${gateway_ip}

    #check service led register is flashing
    Ping Gateway by GUI    ${gateway_ip}
    Wait Until Keyword Succeeds    3x    1s    Get Service_flashing Register Value    n1    ${times}    ${gateway_ip}

*** Keywords ***
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

Get Service_flashing Register Value
    [Arguments]    ${device}    ${times}    ${gateway_ip}
    [Documentation]   Check Service_flashing Register Value 6 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{6}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{1}([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_service_green_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_service_green_on} + 1
        ...    ELSE    Set Variable    ${count_service_green_on}
    \    ${count_service_green_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_service_green_off} + 1
        ...    ELSE    Set Variable    ${count_service_green_off}
    Should not Be Equal    ${count_service_green_on}    0
    Should not Be Equal    ${count_service_green_off}    0

Ping Gateway by GUI
    [Arguments]    ${gateway_ip}
    [Documentation]    Enter Ping Test to ping Gateway in GUI
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    #Go to Utilites Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Ping Test
    select radio button    web    version    ipv4
    input_text    web    id=ip_addr    ${gateway_ip}
    input_text    web    id=packet_size    1440
    cpe click    web    xpath=//button[contains(., 'Test')]

Enter Shell Mode
    [Arguments]
    [Documentation]    Enter shell mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    Wait Until Keyword Succeeds    3x   10 sec    cli    n1    sh

Exit Shell Mode
    [Arguments]
    [Documentation]     Exit CPE shell mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    cli    n1    exit
