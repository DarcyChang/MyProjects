*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_2.4G_Wireless_WEP_Is_connection
    [Documentation]  tc_2.4G_Wireless_WEP_Is_connection
    ...    1. Turn on wireless radio and setting SSID on the DUT.
    ...    2. Setting security type is WEP on the DUT.
    ...    3. 2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client.
    ...    4. 2.4GWIFI client send traffic to the Wanhost successfully.
    [Tags]   @TCID=WRTM-326ACN-410    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on wireless radio and setting SSID on the DUT
    Setting security type is WEP on the DUT
    2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client
    2.4GWIFI client send traffic to the Wanhost successfully

*** Keywords ***
Turn on wireless radio and setting SSID on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless

Setting security type is WEP on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web    Security=WEP    password=${g_dut_wep_ssid_pw}

2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    3s    Login Linux Wifi Client To Connect To DUT Using WEP Encryption    wifi_client    ${g_dut_home_ssid}    ${g_dut_wep_ssid_pw}    ${DEVICES.wifi_client.int}    ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client    echo '${DEVICES.wifi_client.password}' | sudo -S sudo route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}

2.4GWIFI client send traffic to the Wanhost successfully
    [Tags]   @AUTHOR=Hans_Sun
    Use Iperf Send Traffic and Verify Connection Successful    wifi_client    wanhost    ${DEVICES.wanhost.traffic_ip}

*** comment ***
2017-11-15     Hans_Sun
Init the script
