*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi_Setup    @AUTHOR=Gemtek_Gavin_Chang

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup
*** Variables ***
${5g_ssid}    myvita_5G_test1
${security_type}    wpa2-psk-mixed
${security_key}    1234abcd

*** Test Cases ***
tc_WiFi_Authentication_5G_2
    [Documentation]    NB Connect to HA device with WPA/WPA2 AES authentication
    [Tags]    @tcid=WRTM-326ACN-108    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Gavin_Chang
    [Timeout]

    Change "Authentication " to WPA/WPA2 AES
    NB can connect to HA Devcie

*** Keywords ***
Change "Authentication " to WPA/WPA2 AES
    [Arguments]
    [Documentation]    Test Step

    Config 5G Wireless    web    on    ${5g_ssid}    0    ${security_type}    ${security_key}

NB can connect to HA Devcie
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    10x    3s    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${5g_ssid}  ${security_key}  ${DEVICES.wifi_client.int}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}

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


Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]

    Config 5G Wireless    web    on
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant


*** comment ***
2017-08-31    Gemtek_Gavin_Chang
1. Add new script
