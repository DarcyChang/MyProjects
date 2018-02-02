*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_2.4G_Wireless_WPA2_PSK_MIXED_connection
    [Documentation]  tc_2.4G_Wireless_WPA2_PSK_MIXED_connection
    ...    1. Turn on wireless radio and setting SSID on the DUT.
    ...    2. Setting security type is WPA2-PSK MIXED on the DUT.
    ...    3. 2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client.
    [Tags]   @TCID=WRTM-326ACN-411    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on wireless radio and setting SSID on the DUT
    Setting security type is WPA2-PSK MIXED on the DUT
    2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client

*** Keywords ***
Turn on wireless radio and setting SSID on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless

Setting security type is WPA2-PSK MIXED on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web    Security=WPA2-PSK MIXED

2.4GWIFI client connect to the DUT, verify DUT leased IP to WIFI client
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT With Matched Security Key    wifi_client    ${g_dut_home_ssid}    ${g_dut_repeater_ssid_pw}    ${DEVICES.wifi_client.int}    ${g_dut_gw}
    ${r}  run keyword and return status    Verify Wifi Client On Wireless Status GUI    ${Lease_status_table}    ${DEVICES.wifi_client.hostname}
    run keyword if  '${r}'=='False'    Wait Until Keyword Succeeds    3x    1s    Retry to Check DHCP Leases

*** comment ***
2017-11-10     Hans_Sun
Init the script
