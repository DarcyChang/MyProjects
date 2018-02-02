*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Gavin_Chang    stable

Suite Setup    Run keywords    Enter Shell
Suite Teardown    Run keywords    Exit Shell

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${sleep_seconds}    120

*** Test Cases ***
tc_WPS_Solid_Red_Error_to_Connect
    [Documentation]    tc_WPS_Solid_Red_Error_to_Connect
    ...    Verify if the WPS LED stay in SOLID RED state when WPS process fail to connect.
    ...    1.Press WPS button to start a connection.
    ...    2.No client available to connect.
    [Tags]    @TCID=PREMS-TC-7911    @globalid=1597637LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless WPS Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    WPS
    #Check WPS disable
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Connect')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Connect')]
    #The WPS button will count down form 121 seconds
    Sleep    ${sleep_seconds}
    Wait Until Page Does Not Contain Element    web    xpath=//button[contains(., 'seconds left')]
    #Check WPS_Green_OFF Register Value : bit 14 is 1
    Wait Until Keyword Succeeds    5x    10s    Check WPS Green OFF    n1
    #Check WPS_Red_ON Register Value : bit 8 is 0
    Wait Until Keyword Succeeds    5x    10s    Check WPS Red ON    n1

*** Keywords ***
Enter Shell
    [Arguments]
    [Documentation]    To enter the shell
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    cli    n1    sh    ~ #

Exit Shell
    [Arguments]
    [Documentation]    To exit the shell
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    n1    exit

Check WPS Green OFF
    [Arguments]    ${device}
    [Documentation]    Check WPS Green OFF
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =   Get WPS Green LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal     ${result}    1

Check WPS Red ON
    [Arguments]    ${device}
    [Documentation]    Check WPS Red ON
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =   Get WPS Red LED Status From Register Value    n1
    log    ${result}
    Should Be Equal     ${result}    0

Get WPS Green LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    When WPS green off, the register value is 17eadfef => Should retrive the 5th hex: d->1011, bit 14 is 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})     1
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

Get WPS Red LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    When WPS red off, the register value is 17eadfef => Should retrive the 6th hex: f->1111, bit 8 is 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

*** comment ***
