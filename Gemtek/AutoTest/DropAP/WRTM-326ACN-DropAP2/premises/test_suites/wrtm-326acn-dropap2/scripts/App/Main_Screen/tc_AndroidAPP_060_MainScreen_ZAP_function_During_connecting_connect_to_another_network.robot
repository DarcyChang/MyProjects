*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Check the original ZAP is disable

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_060_MainScreen_ZAP_function_During_connecting_connect_to_another_network
    [Documentation]  tc_AndroidAPP_060_MainScreen_ZAP_function_During_connecting_connect_to_another_network
    ...    1. Launch the app and login the user account
    ...    2. Enable the guest network.
    ...    3. Use another device to connect with ZAP network
    ...    4. Press the ZAP button
    ...    5. During connecting, connect to another network
    ...    6. Check the status
    [Tags]   @TCID=WRTM-326ACN-239    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Enable the guest network
    Use another device to connect with ZAP network
    Press the ZAP button
    During connecting, connect to another network
    Check the status

*** Keywords ***
Launch the app and login the user account
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Enable the guest network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch ZAP setting
    ${status}    run keyword and return status    Element Attribute Should Match    ${zap_switch}    checked    false
    run keyword if    ${status}==False
    ...    Run keywords
    ...    touch left
    ...    wait main screen
    return from keyword if    ${status}==False
    touch ZAP Switch
    Change ZAP SSID name    ${g_app_guest_ssid}
    touch ZAP Save
    touch confirm
    wait main screen

Use another device to connect with ZAP network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    1s    Associate To ZAP Networdk
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${DEVICES.wifi_client.int}
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value

Press the ZAP button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Press ZAP button via command


During connecting, connect to another network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    2x    2x    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_app_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    wait main screen

Associate To ZAP Networdk
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_app_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    5x    3s    Is WIFI Interface Up    wifi_client    ${g_app_guest_ssid}


*** comment ***
2018-01-05 Gavin_Chang
1. Reduce the retry time of connecting to wifi to prevent from appium wait new command timeout

2018-01-04 Gavin_Chang
Init the script
