*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=WebGUI    @AUTHOR=Gemteks_Jujung_Chang    norun

*** Variables ***
${844fb_gui_session}    web
${844fb_dump_led_register}     dw fffe8114

*** Test Cases ***
tc_844FB_Broadband_solid_green
    [Documentation]    tc_844FB_Broadband_solid_green
    ...    When bonding line is connected, then broadband LED will bright(solid green)
    [Tags]    @TCID=PREMS-TC-7868   @globalid= 1597587RGGUI844FB    @DUT=844F    @DUT=844FB
    [Timeout]
    login ont    ${844fb_gui_session}    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    ${844fb_gui_session}    Support
    Wait Until Keyword Succeeds    5x    3s    click links    ${844fb_gui_session}    Service WAN VLANs
    Wait Until Element Is Visible    ${844fb_gui_session}    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    ${844fb_gui_session}    name=conn_admin_status
    #Disable WAN Service and Select IPoE Service
    select radio button    ${844fb_gui_session}    conn_admin_status    disabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    ${844fb_gui_session}    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    ${844fb_gui_session}    conn_admin_status    enabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    ${844fb_gui_session}    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    ${844fb_gui_session}    id=gateway_tab
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected
    #Check IPv4 Internet Access status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connected

    #Check Broadband Register Value 4 bit is 0
    ${result} =   Wait Until Keyword Succeeds    5x    1s   Check LED On in Certain Tries    n1
    log    ${result}
    Should Be Equal     ${result}    0

*** Keywords ***
Check LED On in Certain Tries
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 4 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1111, bit 4 is 1
    ${result} =   Wait Until Keyword Succeeds    5x    3s   Get Broadband Green LED Register Value    ${device}
    log    ${result}
    Should Be Equal    ${result}    0
    [Return]    ${result}

Get Broadband Green LED Register Value
    [Arguments]    ${device}
    [Documentation]

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{6}([\\w]{1})     1   #bit 4    0xFFFE8114 : 17eaefaf  => should retrive second hex: 7->0111, bit 4 is 0
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4     #something like 10101111
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0

    log to console    ${ret}
    [Return]    ${ret}







