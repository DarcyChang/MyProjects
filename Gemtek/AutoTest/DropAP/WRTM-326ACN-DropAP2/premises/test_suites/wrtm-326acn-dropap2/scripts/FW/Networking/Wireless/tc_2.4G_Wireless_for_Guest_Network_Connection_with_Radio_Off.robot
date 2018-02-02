*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_2.4G_Wireless_for_Guest_Network_Connection_with_Radio_Off
    [Documentation]  tc_2.4G_Wireless_for_Guest_Network_Connection_with_Radio_Off
    ...    1. Turn off wireless radio and setting SSID at Guest Network on DUT
    ...    2. Verify 2.4G WIFI client can't connect DUT successfully.
    ...    3. Verify Wifi client can't wget 192.168.67.1 successfully.
    [Tags]   @TCID=WRTM-326ACN-434    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn off wireless radio and setting SSID at Guest Network on DUT
    Verify 2.4G WIFI client can't connect DUT successfully
    Verify Wifi client can't wget 192.168.67.1 successfully

*** Keywords ***
Turn off wireless radio and setting SSID at Guest Network on DUT
    [Documentation]  Turn off wireless radio and setting SSID at Guest Network on DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Config Wireless Guest Network    web    off

Verify 2.4G WIFI client can't connect DUT successfully
    [Documentation]  Verify 2.4G WIFI client connect DUT successfully
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    1s    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_dut_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Down    wifi_client    ${g_dut_guest_ssid}

Verify Wifi client can't wget 192.168.67.1 successfully
    [Tags]   @AUTHOR=Hans_Sun
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    Wait Until Keyword Succeeds    5x    3s    Is Linux wget Failed    wifi_client    ${g_wifi_guest_gw}

*** comment ***
2017-11-23     Hans_Sun
Init the script
