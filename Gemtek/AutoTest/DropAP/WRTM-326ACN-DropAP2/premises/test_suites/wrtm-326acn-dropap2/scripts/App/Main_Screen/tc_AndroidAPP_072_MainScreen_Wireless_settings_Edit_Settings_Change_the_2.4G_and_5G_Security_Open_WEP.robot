*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Restore Security

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest
${security}    WEP
${original_security}    Open

*** Test Cases ***
tc_AndroidAPP_072_MainScreen_Wireless_settings_Edit_Settings_Change_the_2.4G_and_5G_Security_Open_WEP
    [Documentation]  tc_AndroidAPP_072_MainScreen_Wireless_settings_Edit_Settings_Change_the_2.4G_and_5G_Security_Open_WEP
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Change the WiFi security from open to WEP then press OK button
    ...    4. Check the status
    [Tags]   @TCID=WRTM-326ACN-257    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Change the WiFi security from open to WEP then press OK button
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Wireless Settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting

Change the WiFi security from open to WEP then press OK button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Change Security    ${security}    ${g_dut_wep_ssid_pw}
    touch wireless ok
    wait main screen

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Login Linux Wifi Client To Connect To DUT Using WEP Encryption    wifi_client    ${g_app_home_ssid}    ${g_dut_wep_ssid_pw}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Restore Security
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting
    Change Security    ${original_security}
    touch wireless ok
    wait main screen
    Close APP

*** comment ***
2017-12-18 Gavin_Chang
Init the script
