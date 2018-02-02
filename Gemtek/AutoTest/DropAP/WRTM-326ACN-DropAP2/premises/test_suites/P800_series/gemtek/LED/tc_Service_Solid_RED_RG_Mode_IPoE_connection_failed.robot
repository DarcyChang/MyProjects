*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Jujung_Chang    stable

Suite Setup    Run keywords    Enter Shell Mode And Cisco Prejob Config
Suite Teardown  Run keywords    Exit Shell Mode And Cisco

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${times}    3
${dummy_pppoe_username}    test1
${dummy_pppoe_password}    test1

*** Test Cases ***
tc_Service_Solid_RED_RG_Mode_IPoE_connection_failed
    [Documentation]   tc_Service_Solid_RED_RG_Mode_IPoE_connection_failed
    ...    Check DHCP and PPPoE don't get IP and Service LED will solid red.
    ...    =====DHCP=====
    ...    1.We shutdown cisco log message
    ...    2.We shutdown cisco FastEthernet6 port.
    ...    3.We check IPv4 internet access status by checking cell value is "Connecting".
    ...    4.We check IP is 0.0.0.0
    ...    5.We check Service LED.Red is on. Green is off.
    ...    =====PPPoE=====
    ...    6.We open cisco fastEthernet 6
    ...    7.We set dummy username and password for PPPoE server.
    ...    8.We check IPv4 internet sccess status by checking cell value is "Connecting".
    ...    9.We check Service LED.Red is on. Green is off.

    [Tags]   @TCID=PREMS-TC-7880   @globalid=1597600LED844F   @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Jujung_Chang
    [Timeout]
    #shutdown fastethernet 6
    cli    cisco_ip_server    config t    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    interface range fastEthernet 6    C1800-DHCP\\(config-if-range\\)#
    cli    cisco_ip_server    sh    C1800-DHCP\\(config-if-range\\)#
    #check interface status
    ${ret}    cli    cisco_ip_server    do show ip int brief FastEthernet6    C1800-DHCP\\(config-if-range\\)#
    log   ${ret}
    Should Contain    ${ret}    administratively down

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Disable WAN Service and Select IPoE Service
    select radio button    web    conn_admin_status    disabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    web    conn_admin_status    enabled
    select radio button    web    framing    IPoE
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check IPv4 IP Address if DHCP server allocate ip to device
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    #Check IPv4 Internet Access status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connecting
    #Check IPv4 IP Address if DHCP server allocate ip to device
    Page Should Contain Element    web    xpath=//table[contains(., '0.0.0.0')]

    #Check WAN Service LED off and 6 & 21 bit is 1
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED Off in Certain Tries    n1
#    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Service_green_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1

    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED On in Certain Tries    n1
#    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Service_red_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    0

    #no shutdown fastethernet 5-7
    cli    cisco_ip_server    interface range fastEthernet 6    C1800-DHCP\\(config-if-range\\)#
    cli    cisco_ip_server    no sh    C1800-DHCP\\(config-if-range\\)#

#    cli    cisco_ip_server    exit    C1800-DHCP\\(config\\)#
#    cli    cisco_ip_server    exit    C1800-DHCP#

    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    web    framing    PPPoE
    input_text    web    id=pppoe_username    ${dummy_pppoe_username}
    input_text    web    id=pppoe_password    ${dummy_pppoe_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Go to Status Page and check Disconnected
    #Check IPv4 IP Address if PPPoE server allocate ip to device
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    #Check IPv4 Internet Access status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connecting
    #Check IPv4 IP Address if DHCP server allocate ip to device
    Wait Until Keyword Succeeds     5x    2s    Cell Value Should Be Empty    web    xpath=//table[@id='gateway_tab']    10    2

    #Check WAN Service LED off and 6 & 21 bit is 1
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED Off in Certain Tries    n1
#    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Service_green_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1

    #service red will bright ,when PPPoE connected fail
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED On in Certain Tries    n1
#    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Service_red_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    0


*** Keywords ***
Check LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Service_red_off_on Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Check LED Off in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Service_green_off_on Register Value    ${device}
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
    ...    ELSE    No Operation
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
    [Documentation]    Enter shell mode and cisco prejob config
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    Wait Until Keyword Succeeds    3x   10 sec    cli    n1    sh
    #cisco prejob config
    Wait Until Keyword Succeeds    3x   10 sec    cli    cisco_ip_server    enable
    cli    cisco_ip_server    terminal length 0    C1800-DHCP#
    cli    cisco_ip_server    config t    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    no logging console    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    line console 0    C1800-DHCP\\(config-line\\)#
    cli    cisco_ip_server    no exec-timeout    C1800-DHCP\\(config-line\\)#
    cli    cisco_ip_server    exit    C1800-DHCP\\(config\\)#

Exit Shell Mode And Cisco
    [Arguments]
    [Documentation]    Exit CPE shell mode and cisco privilege mode
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    cli    n1    exit

    #no shutdown fastethernet 5-7
    cli    cisco_ip_server    interface range fastEthernet 6    C1800-DHCP\\(config-if-range\\)#
    cli    cisco_ip_server    no sh    C1800-DHCP\\(config-if-range\\)#

    cli    cisco_ip_server    exit    C1800-DHCP\\(config\\)#
    cli    cisco_ip_server    exit    C1800-DHCP#



