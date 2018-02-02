*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest
${security}    Open


*** Test Cases ***
tc_AndroidAPP_074_MainScreen_Wireless_settings_Change_the_2.4G_and_5G_Security_WPA2_OPEN
    [Documentation]  tc_AndroidAPP_074_MainScreen_Wireless_settings_Change_the_2.4G_and_5G_Security_WPA2_OPEN
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Change the WiFi security from WPA2 to OPEN then press OK button
    ...    4. Check the status
    [Tags]   @TCID=WRTM-326ACN-259    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Change the WiFi security from WPA2 to OPEN then press OK button
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

Change the WiFi security from WPA2 to OPEN then press OK button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Change Security    ${security}
    touch wireless ok

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_app_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}


*** comment ***
2017-12-18 Gavin_Chang
Init the script
