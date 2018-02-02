*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Check the original settings

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest
${ipv6_server}    ff05::1:3
${ipv6_prefix}    4006:e024:680:1
${ipv4_prefix}    192.168.66

*** Test Cases ***
tc_AndroidAPP_080_MainScreen_Wireless_settings_Enable_Disable_IPv6
    [Documentation]  tc_AndroidAPP_080_MainScreen_Wireless_settings_Enable_Disable_IPv6
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Enable the IPv6
    ...    4. Use PC to connect DropAP
    ...    5. Check the IPv6 format on PC
    ...    6. Disable the IPv6
    ...    7. Check the IPv4 format on PC
    [Tags]   @TCID=WRTM-326ACN-317    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Enable the IPv6
    Use PC to connect DropAP
    Check the IPv6 format on PC
    Disable the IPv6
    Check the IPv4 format on PC

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

Enable the IPv6
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    touch IPv6 Switch

Use PC to connect DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    2x    2s    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_app_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Check the IPv6 format on PC
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5s    Check Get IP Address Format    wifi_client    ${DEVICES.wifi_client.int}    ${ipv6_prefix}
    Wait Until Keyword Succeeds    10x    3s    Get IPv6 Address Successful    wifi_client    ${ipv6_server}

Disable the IPv6
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting
    Swipe To Up
    touch IPv6 Switch

Check the IPv4 format on PC
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Use PC to connect DropAP
    Wait Until Keyword Succeeds    5x    2s    Check Get IP Address Format    wifi_client    ${DEVICES.wifi_client.int}    ${ipv4_prefix}
    Wait Until Keyword Succeeds    10x    3x    Is Linux Ping Successful    wifi_client    ${g_dut_gw}


Check Get IP Address Format
    [Arguments]    ${device}    ${interface}    ${ip_prefix}
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    cli    wifi_client    sudo ifconfig ${DEVICES.wifi_client.int} down
    cli    wifi_client    sudo ifconfig ${DEVICES.wifi_client.int} up
    sleep   5s
    ${result} =    cli    ${device}   ifconfig ${interface}
    Should Contain    ${result}    ${ip_prefix}

Get IPv6 Address Successful
    [Arguments]    ${device}    ${gw_ip}     ${ping_count}=3
    [Documentation]    To check ping6 ${gw_ip} is successful
    [Tags]    @AUTHOR=Gavin_Chang

    ${result} =    cli    ${device}   ping6 -I ${DEVICES.wifi_client.int} ${gw_ip} -c ${ping_count}
    log    ${result}
    Should contain    ${result}    bytes from

Check the original settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Close APP
    Launch APP
    Sign In
    wait main screen
    touch Device Settings
    touch Wireless Setting
    Swipe To Up
    ${status}    run keyword and return status    Element Attribute Should Match    ${ipv6_btn}    checked    false
    run keyword if    ${status}==False
    ...    touch IPv6 Switch
    Close APP
*** comment ***
2017-12-26 Gavin_Chang
Init the script
