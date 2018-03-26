*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_5G_Wireless_WPA2_PSK_MIXED_connection_with_uncorrect_password
    [Documentation]  tc_5G_Wireless_WPA2_PSK_MIXED_connection_with_uncorrect_password
    ...    1. Turn on wireless radio and setting SSID on the DUT.
    ...    2. Setting security type is WPA2-PSK MIXED on the DUT.
    ...    3. 5GWIFI client using inconnect password to associate with DUT and verify client can't send traffic to the DUT successfully.
    [Tags]   @TCID=WRTM-326ACN-431    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on wireless radio and setting SSID on the DUT
    Setting security type is WPA2-PSK MIXED on the DUT
    5GWIFI client using inconnect password to associate with DUT and verify client can't send traffic to the DUT successfully

*** Keywords ***
Turn on wireless radio and setting SSID on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless

Setting security type is WPA2-PSK MIXED on the DUT
    [Tags]   @AUTHOR=Hans_Sun
    Config Wireless Home Network    web    Security=WPA2-PSK MIXED

5GWIFI client using inconnect password to associate with DUT and verify client can't send traffic to the DUT successfully
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT With Unmatched Security Key    wifi_client    ${g_dut_home_ssid}-5G    ${g_dut_dummy_ssid_pw}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

*** comment ***
2017-11-16     Hans_Sun
Init the script