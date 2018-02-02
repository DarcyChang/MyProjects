*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Exit Shell Mode
*** Variables ***
${844fb_dump_led_register}    dw fffe8114
${vlan}    913
${priority}    1
${pppoe_username}    test
${pppoe_password}    test

*** Test Cases ***
tc_Service_Solid_Green_RG_Mode_PPPoE_connection
    [Documentation]   Verify if the Service LED stay in Solid Green state when the ONT authentication via PPPoE.
    ...    1. Connect a ONT which has the WAN interface configured to PPPoE.
    ...    2. Check that the ONT got an IP and it is working properly.
    [Tags]    @TCID=PREMS-TC-7879    @globalid=1597599LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
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
    #priority is 1
    input_text    web    id=vlan_config_priority    ${priority}
    #Select PPPoE and insert username and password
    select radio button    web    framing    PPPoE
    input_text    web    id=pppoe_username    ${pppoe_username}
    input_text    web    id=pppoe_password    ${pppoe_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check IPv4 IP Address if DHCP server allocate ip to device
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    Wait Until Keyword Succeeds    20x    2s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connected
    ${my_ip} =  Wait Until Keyword Succeeds    5x    2s     Get Non Empty Cell Value    web    xpath=//table[@id='gateway_tab']    10    2
    #check led register green is off
    ${result} =   Wait Until Keyword Succeeds    5x    3s    Check LED On in Certain Tries    n1
    log    ${result}
    Should Be Equal    ${result}    0
    #check led register red is on, because it's connected fail
    ${result} =   Wait Until Keyword Succeeds    5x    3s    Get Service Red LED Status Register Value    n1
    log    ${result}
    Should Be Equal    ${result}    1

*** Keywords ***
Get Service Green LED Status Register Value
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

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

Get Service Red LED Status Register Value
    [Arguments]    ${device}
    [Documentation]    when red on Register Value is 174adfef  => should retrive third hex: 4->0100, bit 21 is 0
    ...                when red off Register Value is 176adfef  => should retrive third hex: 6->0110, bit 21 is 1
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

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

Check LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when led flashing transfer to solid, retry to check register value
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Service Green LED Status Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Enter Shell Mode
    [Arguments]
    [Documentation]    Go to shell mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    Wait Until Keyword Succeeds    5x    3s   cli    n1    sh

Exit Shell Mode
    [Arguments]
    [Documentation]    exit from shell mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    n1    exit

*** comment ***