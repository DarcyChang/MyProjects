*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Check the original settings

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest

*** Test Cases ***
tc_AndroidAPP_075_MainScreen_Wireless_settings_Enable_Disable_Hide_SSID
    [Documentation]  tc_AndroidAPP_075_MainScreen_Wireless_settings_Enable_Disable_Hide_SSID
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Enable Hide SSID
    ...    4. Use mobile to search the DropAP SSID.
    ...    5. Try to connect the DropAP SSID by manual add via mobile
    ...    6. Disable the Hide SSID.
    ...    7. Check the SSID in WiFi list.
    [Tags]   @TCID=WRTM-326ACN-260    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Enable Hide SSID
    Use mobile to search the DropAP SSID
    Try to connect the DropAP SSID by manual add via mobile
    Disable the Hide SSID
    Check the SSID in WiFi list

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

Enable Hide SSID
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Hide SSID
    touch wireless ok
    wait main screen

Use mobile to search the DropAP SSID
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_home_ssid}    yes

Try to connect the DropAP SSID by manual add via mobile
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_app_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Disable the Hide SSID
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting
    touch Hide SSID
    touch wireless ok
    wait main screen

Check the SSID in WiFi list
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_home_ssid}

Check the original settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Close APP
    Launch APP
    Sign In
    wait main screen
    touch Device Settings
    touch Wireless Setting
    ${status}    run keyword and return status    Element Attribute Should Match    ${wireless_hide_ssid}    checked    false
    run keyword if    ${status}==False
    ...    Run keywords
    ...    touch Hide SSID
    ...    touch wireless ok
    ...    wait main screen
    Close APP



*** comment ***
2017-01-05 Gavin_Chang
1. Add teardown to check original setting be restored.

2017-12-18 Gavin_Chang
Init the script
