*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Restore SSID

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest

*** Test Cases ***
tc_AndroidAPP_071_MainScreen_Wireless_settings_Edit_Settings_Change_the_2.4G_and_5G_SSID
    [Documentation]  tc_AndroidAPP_071_MainScreen_Wireless_settings_Edit_Settings_Change_the_2.4G_and_5G_SSID
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Change the Network name then press OK button
    ...    4. Check the status
    [Tags]   @TCID=WRTM-326ACN-253    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Change the Network name then press OK button
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

Change the Network name then press OK button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Change Wireless SSID name    ${g_app_rename_home_ssid}
    touch wireless ok
    Wait Until Keyword Succeeds    2x    3s    wait main screen

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_rename_home_ssid}
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_rename_home_ssid}-5G

Restore SSID
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting
    Change Wireless SSID name    ${g_app_home_ssid}
    touch wireless ok
    Wait Until Keyword Succeeds    2x    3s    wait main screen
    Close APP

*** comment ***
2017-12-12 Gavin_Chang
Init the script
