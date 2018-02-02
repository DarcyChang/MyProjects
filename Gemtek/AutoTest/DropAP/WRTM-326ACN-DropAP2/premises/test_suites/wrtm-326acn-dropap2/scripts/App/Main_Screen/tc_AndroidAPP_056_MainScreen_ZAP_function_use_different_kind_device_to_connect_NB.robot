*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Check the original ZAP is disable

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_056_MainScreen_ZAP_function_use_different_kind_device_to_connect_NB
    [Documentation]  tc_AndroidAPP_056_MainScreen_ZAP_function_use_different_kind_device_to_connect_NB
    ...    1. Launch the app and login the user account
    ...    2. Enable the ZAP network
    ...    3. Use NB to connect with ZAP network
    ...    4. Press the ZAP button
    ...    5. Check the status
    [Tags]   @TCID=WRTM-326ACN-235    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Enable the ZAP network
    Use NB to connect with ZAP network
    Press the ZAP button
    Check the status

*** Keywords ***
Launch the app and login the user account
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Enable the ZAP network
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

Use NB to connect with ZAP network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    1s    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_app_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    wifi_client    ${g_app_guest_ssid}


Press the ZAP button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Press ZAP button via command


Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${DEVICES.wifi_client.int}
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value
    Wait Until Keyword Succeeds    10x    2s    Is Linux Ping Successful    dut1    ${wifi_ip}


*** comment ***
2018-01-15 Gavin_Chang
1. Release wifi_client interface and use dhclient to get new one.

2017-12-27 Gavin_Chang
1. Restore ZAP only when change be saved.

2017-12-12 Gavin_Chang
Init the script
