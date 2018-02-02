*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
*** Variables ***

*** Test Cases ***
tc_5G_WLAN_PC_can_connected_to_LAN_PC
    [Documentation]  tc_5G_WLAN_PC_can_connected_to_LAN_PC
    ...    1. Turn on wireless radio and setting SSID on the DUT
    ...    2. Setting security type is Open on the DUT
    ...    3. 5GWIFI client connect to the DUT, verify DUT leased IP to WIFI client, 5GWIFI client send traffic to the DUT successfully
    ...    4. 5G WIFI client can send traffic to LAN host
    [Tags]   @TCID=WRTM-326ACN-440    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on wireless radio and setting SSID on the DUT
    Setting security type is Open on the DUT
    5GWIFI client connect to the DUT, verify DUT leased IP to WIFI client, 5GWIFI client send traffic to the DUT successfully
    5G WIFI client can send traffic to LAN host

*** Keywords ***
Turn on wireless radio and setting SSID on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless

Setting security type is Open on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web

5GWIFI client connect to the DUT, verify DUT leased IP to WIFI client, 5GWIFI client send traffic to the DUT successfully
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    1s    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_dut_home_ssid}-5G    ${DEVICES.wifi_client.int}    ${g_dut_gw}

5G WIFI client can send traffic to LAN host
    [Tags]   @AUTHOR=Hans_Sun
    Use Iperf Send Traffic and Verify Connection Successful    wifi_client    lanhost    ${DEVICES.lanhost.traffic_ip}

*** comment ***
2017-12-1     Hans_Sun
Init the script
