*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Jujung_Chang    norun

*** Variables ***
${844fb_gui_session}    web
${844fb_dump_led_register}     dw fffe8114

*** Test Cases ***
tc_Service_Off_No_physical_connection
    [Documentation]   tc_Service_Off_No_physical_connection
    ...    1.If physical line is disconnection ,then status will show 'Disconnected'.
    ...    2.We connected physical line ,then status will show Connected.
    ...    3.We disconnection again,then status will show 'Disconnected'.
    [Tags]   @TCID=PREMS-TC-7872   @globalid= 1597592LED844F   @DUT=844FB  @DUT=844F
    [Timeout]
    #Login Web GUI
    login ont    ${844fb_gui_session}    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Status Page and check Wide Area Network (WAN) table
    Wait Until Keyword Succeeds    5x    3s    click links    ${844fb_gui_session}    Status
    Wait Until Element Is Visible    ${844fb_gui_session}    id=conn_tab
    #Check Wide Area Network (WAN) status
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible	   ${844fb_gui_session}    xpath=//td[@id="wan_conn_cell"]/div[contains(.,'Disconnected')]
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible	   ${844fb_gui_session}    xpath=//td[@id="ipv4_conn_cell"]/div[contains(.,'Disconnected')]
    #check led register
    ${result} =   Get Service_green_off_on Register Value    n1
    log    ${result}
    Should Be Equal    ${result}    1
    ${result} =   Get Service_red_off_on Register Value    n1
    log    ${result}
    Should Be Equal    ${result}    1

*** Keywords ***
Get Service_green_off_on Register Value
    [Arguments]    ${device}
    [Documentation]    when green on Register Value is 176adfaf  => should retrive third hex: a->1010, bit 6 is 0
    ...                when green off Register Value is 176adfef  => should retrive third hex: e->1110, bit 6 is 1
    [Tags]    @AUTHOR=Gemteks_Jujung_Chang

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
    [Tags]    @AUTHOR=Gemteks_Jujung_Chang

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
