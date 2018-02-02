*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi_Setup    @AUTHOR=Gemtek_Gavin_Chang

Suite Setup    Run keywords    Common Setup

*** Variables ***
${2.4G_default_authentication}    wpa2-psk-mixed

*** Test Cases ***
tc_WiFi_Authentication_2_4G_3
    [Documentation]    Check "2.4G Authentication" default type is WPA/WPA2 AES mode
    [Tags]    @tcid=WRTM-326ACN-141    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]

    Check "Authentication" type

*** Keywords ***
Check "Authentication" type
    [Arguments]
    [Documentation]    Test Step

    # Go to device setting page
    Go To Page    web    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    ${result}    get_selected_list_value    web    security
    Should Be Equal    ${result}    ${2.4G_default_authentication}


Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]

    Login Web GUI

Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]

    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

*** comment ***
2017-08-31    Gemtek_Gavin_Chang
1. Add new script
