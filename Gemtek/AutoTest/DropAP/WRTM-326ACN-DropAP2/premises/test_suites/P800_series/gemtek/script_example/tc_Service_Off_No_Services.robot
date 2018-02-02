*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Hans_Sun    norun

Suite Setup    Run keywords    Enter Shell Mode
Suite Teardown    Run keywords    Exit Shell Mode
*** Variables ***
${844fb_dump_led_register}     dw fffe8114

*** Test Cases ***
tc_Verify_Service_Off_when_No_Service
    [Documentation]   tc_Verify_Service_Off_when_No_Service.
    ...    1.Verify if the Service LED stay in OFF state when no service provisioned.
    ...    2.Check no IP address received from DHCP Server, Service LED is off.
    [Tags]   @TCID=PREMS-TC-7875   @globalid=1597595LED844F   @DUT=844FB   @DUT=844F
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Disable WAN Service
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    conn_admin_status    disabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check IPv4 IP Address
    Page Should Contain Element    web    xpath=//table[contains(., '0.0.0.0')]
    #Check WAN Service LED off and 6 & 21 bit is 1
    ${result} =   Get Service$ Green LED Status From Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1
    ${result} =   Get Service Red LED Status From Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    1

*** Keywords ***
Get Service Green LED Status From Register Value
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

Get Service Red LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    when red on Register Value is 174adfef  => should retrive third hex: 4->0100, bit 21 is 0
    ...                when red off Register Value is 176adfef  => should retrive third hex: 6->0110, bit 21 is 1
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

Enter Shell Mode
    [Arguments]
    [Documentation]    Go to shell mode
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

    Wait Until Keyword Succeeds    5x    3s   cli    n1    sh

Exit Shell Mode
    [Arguments]
    [Documentation]    exit from shell mode
    [Tags]    @AUTHOR=Gemteks_Hans_Sun

    cli    n1    exit
*** comment ***