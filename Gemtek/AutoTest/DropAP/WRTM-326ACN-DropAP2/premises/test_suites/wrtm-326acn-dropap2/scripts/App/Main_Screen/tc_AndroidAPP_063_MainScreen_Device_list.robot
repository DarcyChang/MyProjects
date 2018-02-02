*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Check the original ZAP is disable

*** Variables ***
${mobile_device}    ASUS Zenfone 6


*** Test Cases ***
tc_AndroidAPP_063_MainScreen_Device_list
    [Documentation]  tc_AndroidAPP_063_MainScreen_Device_list
    ...    1. Launch the DropAP app into main screen
    ...    2. Press device list button
    ...    3. Check the device list
    [Tags]   @TCID=WRTM-326ACN-242    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the DropAP app into main screen
    Press device list button
    Check the device list

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen
    Connect to the ZAP network

Press device list button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device list

Check the device list
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Text    ${mobile_device}
    Page Should Contain Text    "${DEVICES.wifi_client.hostname}"
    touch left

Connect to the ZAP network
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
    Wait Until Keyword Succeeds    3x    1s    Associate To ZAP Networdk
    Press ZAP button via command
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${DEVICES.wifi_client.int}
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value
    Wait Until Keyword Succeeds    10x    3s    Is Linux Ping Successful    dut1    ${wifi_ip}

Associate To ZAP Networdk
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_app_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    5x    3s    Is WIFI Interface Up    wifi_client    ${g_app_guest_ssid}



*** comment ***
2018-01-02 Gavin_Chang
Init the script
