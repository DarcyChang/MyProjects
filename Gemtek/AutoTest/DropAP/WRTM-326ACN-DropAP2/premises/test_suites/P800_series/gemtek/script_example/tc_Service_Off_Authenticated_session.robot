*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Hans_Sun    norun

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${times}    3
${pppoe_username}    test
${pppoe_password}    test

*** Test Cases ***
tc_Verify_Service_Off_when_Authenticated_session
    [Documentation]   tc_Verify_Service_Off_when_Authenticated_session
    ...    1.Verify if the Service LED stay in OFF state when no service provisioned.
    ...    2.No IP address received or PPPoE session authentication has occurred, Service LED is off.
    [Tags]   @TCID=PREMS-TC-7888   @globalid=1597608LED844F   @DUT=844FB   @DUT=844F
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
    select radio button    web    framing    IPoE
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check IPv4 IP Address if DHCP server allocate ip to device
    Check Server Allocate IP To Device By Loop    ${times}
    #Check WAN Service LED off and 6 & 21 bit is 1
    ${result} =   Get Service_green_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1
    ${result} =   Get Service_red_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1
    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    web    framing    PPPoE
    input_text    web    id=pppoe_username    ${pppoe_username}
    input_text    web    id=pppoe_password    ${pppoe_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check IPv4 IP Address if PPPoE server allocate ip to device
    Check Server Allocate IP To Device By Loop    ${times}
    #Check WAN Service LED off and 6 & 21 bit is 1
    ${result} =   Get Service_green_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1
    ${result} =   Get Service_red_off_on Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1

*** Keywords ***
Get Service_green_off_on Register Value
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

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
    ...                 when red off Register Value is 176adfef  => should retrive third hex: 6->0110, bit 21 is 1
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

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

Check Server Allocate IP To Device By Loop
    [Arguments]    ${times}
    [Documentation]    Every 5 seconds to re-check ip addres if DHCP/PPPoE server allocate ip to device
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

    : FOR    ${INDEX}    IN RANGE    0    ${times}
        #Wait 5 seconds to re-check
    \    Sleep     5
    \    Page Should Contain Element    ${844fb_gui_session}    xpath=//table[contains(., 'Disconnected')]

*** comment ***