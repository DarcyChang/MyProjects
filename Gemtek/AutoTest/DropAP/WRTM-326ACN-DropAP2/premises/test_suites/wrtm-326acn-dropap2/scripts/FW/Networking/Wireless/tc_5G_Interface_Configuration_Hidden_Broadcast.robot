*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_5G_Interface_Configuration_Hidden_Broadcast
    [Documentation]  tc_5G_Interface_Configuration_Hidden_Broadcast
    ...    1. Configure DUT to disable Hidden Broadcast with default setting
    ...    2. Verify wireless client can get SSID and it can associate to DUT or not
    ...    3. Configure DUT to enable Hidden Broadcast
    ...    4. Verify wireless client cannot get SSID but it still can associate to DUT or not
    [Tags]   @TCID=WRTM-326ACN-407    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Configure DUT to disable Hidden Broadcast with default setting
    Verify wireless client can get SSID and it can associate to DUT or not
    Configure DUT to enable Hidden Broadcast
    Verify wireless client cannot get SSID but it still can associate to DUT or not

*** Keywords ***
Configure DUT to disable Hidden Broadcast with default setting
    [Documentation]  Setting the SSID filed with 32 characters by all of the ASCII characters
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web

Verify wireless client can get SSID and it can associate to DUT or not
    [Documentation]  Verify wireless client can associate to DUT or not
    [Tags]   @AUTHOR=Hans_Sun
    cli    wifi_client_5g    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client_5g    ${g_dut_home_ssid}-5G    ${DEVICES.wifi_client_5g.int}    ${g_dut_gw}

Configure DUT to enable Hidden Broadcast
    [Documentation]  Configure DUT to enable Hidden Broadcast
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web    Hidden=yes

Verify wireless client cannot get SSID but it still can associate to DUT or not
    [Documentation]  Verify wireless client cannot get SSID but it still can associate to DUT or not
    [Tags]   @AUTHOR=Hans_Sun
    Verify Wireless Scan With Hidden or not    wifi_client    ${g_dut_home_ssid}    yes
    cli    wifi_client_5g    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client_5g    ${g_dut_home_ssid}-5G    ${DEVICES.wifi_client_5g.int}    ${g_dut_gw}

*** comment ***
2017-11-09     Hans_Sun
Init the script
