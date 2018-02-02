*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi_Setup    @AUTHOR=Gemtek_Gavin_Chang

Suite Setup    Run keywords    Common Setup

*** Variables ***
${5g_default_ssid}    myvita

*** Test Cases ***
tc_WiFi_Network_Name_SSID_5G_1
    [Documentation]    Check "5G WiFi-Network Name(SSID)" default name is myvita
    [Tags]    @tcid=WRTM-326ACN-103    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]

    Check "WiFi-Network Name(SSID)" default name

*** Keywords ***
Check "WiFi-Network Name(SSID)" default name
    [Arguments]
    [Documentation]    Test Step

    # Go to device setting page
    Go To Page    web    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s

    ${result}    Get Element Value    web    ssid_5g
    Should Be Equal    ${result}    ${5g_default_ssid}


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
