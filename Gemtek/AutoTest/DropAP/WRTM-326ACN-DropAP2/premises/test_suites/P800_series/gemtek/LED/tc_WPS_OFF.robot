*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Gavin_Chang    stable

Suite Setup    Run keywords    Enter Shell
Suite Teardown    Run keywords    Exit Shell

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${sleep_seconds}    120

*** Test Cases ***
tc_WPS_OFF
    [Documentation]    tc_WPS_OFF
    ...    WPS LED must be Off state when WPS not active or disable.
    [Tags]    @TCID=PREMS-TC-7908    @globalid=1597634LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless WPS Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    WPS
    #Check WPS disable
    Page Should Contain Element    web    xpath=//button[contains(., 'Connect')]
    #Check WPS_Green_OFF Register Value : bit 14 is 1
    Wait Until Keyword Succeeds    2x    120s    Check WPS Green OFF    n1
    #Check WPS_Red_OFF Register Value : bit 8 is 1
    Wait Until Keyword Succeeds    2x    120s    Check WPS Red OFF    n1

*** Keywords ***
Enter Shell
    [Arguments]
    [Documentation]    To enter the shell, sleep 120 seconds to make sure the state of WPS can be triggered.
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang
    cli    n1    sh
    sleep    ${sleep_seconds}

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

Check WPS Red OFF
    [Arguments]    ${device}
    [Documentation]    Check WPS Red OFF
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =   Get WPS Red LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal     ${result}    1

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
