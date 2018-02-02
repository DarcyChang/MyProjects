*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Gavin_Chang

Suite Setup    Run keywords    Enter Shell
Suite Teardown    Run keywords    Exit Shell

*** Variables ***
${844fb_dump_led_register}     dw fffe8114
${count_wps_green_on}    0
${count_wps_green_off}    0
${count_wps_red_on}    0
${count_wps_red_off}    0
${times}    30
${sleep_seconds}    120
${video_ssid}    5GHz_IPTV_SSID040D1E

*** Test Cases ***
tc_WPS_Flashing_Amber_Slow_IPTV_5GHz_SSID
    [Documentation]    tc_WPS_Flashing_Amber_Slow_IPTV_5GHz_SSID
    ...    WPS LED must be in a Flashing Amber slow state during the process of associating.
    [Tags]    @TCID=PREMS-TC-7914    @globalid=1597640LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Check Video SSID is enable
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${video_ssid}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${video_ssid}
    select radio button    web    ssid_state    1
    radio_button_should_be_set_to    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Go to Wireless WPS Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Video WPS
    #Check WPS disable
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Connect')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Connect')]
    #Check WPS_Green_flashing Register Value : bit 14 is 1 or 0
    Wait Until Keyword Succeeds    10x    2s    Get WPS Green Flashing Register Value    n1    ${times}
    #Check WPS_Red_flashing Register Value : bit 8 is 1 or 0
    Wait Until Keyword Succeeds    10x    2s    Get WPS Red Flashing Register Value    n1    ${times}

*** Keywords ***
Enter Shell
    [Arguments]
    [Documentation]    To enter the shell
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    n1    sh

Exit Shell
    [Arguments]
    [Documentation]    To exit the shell, sleep 120 seconds to make sure the state of WPS can be triggered
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    n1    exit
    sleep    ${sleep_seconds}

Get WPS Green Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check WPS_Green_flashing Register Value 14 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{1}([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_wps_green_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_wps_green_on} + 1
        ...    ELSE    Set Variable    ${count_wps_green_on}
    \    ${count_wps_green_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_wps_green_off} + 1
        ...    ELSE    Set Variable    ${count_wps_green_off}
    log    ${count_wps_green_on}
    log    ${count_wps_green_off}
    Should not Be Equal    ${count_wps_green_on}    0
    Should not Be Equal    ${count_wps_green_off}    0

Get WPS Red Flashing Register Value
    [Arguments]    ${device}    ${times}
    [Documentation]   Check WPS_Green_flashing Register Value 8 bit is 0 or 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    : FOR    ${INDEX}    IN RANGE    1    ${times}
    \    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    \    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    \    log to console    ${register_value_list}
    \    ${length} =    Get Length    ${register_value_list}
    \    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
        ...    ELSE    Set Variable    false_default_str
    \    log   ${hex_register_value}
    \    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    \    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    \    ${ret} =    Get From List     ${ret_list}    0
    \    ${count_wps_red_on} =    Run Keyword If    ${ret} == 0    Evaluate    ${count_wps_red_on} + 1
        ...    ELSE    Set Variable    ${count_wps_red_on}
    \    ${count_wps_red_off} =    Run Keyword If    ${ret} == 1    Evaluate    ${count_wps_red_off} + 1
        ...    ELSE    Set Variable    ${count_wps_red_off}
    log    ${count_wps_red_on}
    log    ${count_wps_red_off}
    Should not Be Equal    ${count_wps_red_on}    0
    Should not Be Equal    ${count_wps_red_off}    0
*** comment ***
