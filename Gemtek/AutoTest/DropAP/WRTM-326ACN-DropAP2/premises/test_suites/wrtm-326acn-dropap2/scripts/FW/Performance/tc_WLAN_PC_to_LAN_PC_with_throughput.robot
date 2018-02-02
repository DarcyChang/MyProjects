*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Performance    @AUTHOR=Hans_Sun
*** Variables ***
${transfer_time}    60

*** Test Cases ***
tc_WLAN_PC_to_LAN_PC_with_throughput
    [Documentation]  tc_WLAN_PC_to_LAN_PC_with_throughput
    ...    1. WLAN PC connected to DUT
    ...    2. Verify DUT leaseed IP to WLAN PC, and WLAN send traffic to DUT succesfully
    ...    3. Using LAN PC and repeat Step1~Step3
    ...    4. WLAN PC check throughput to LAN PC using iperf tool
    [Tags]   @TCID=WRTM-326ACN-453    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    WLAN PC connected to DUT
    Verify DUT leaseed IP to WLAN PC, and WLAN send traffic to DUT succesfully
    Using LAN PC and repeat Step1~Step3
    WLAN PC check throughput to LAN PC using iperf tool

*** Keywords ***
WLAN PC connected to DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web

Verify DUT leaseed IP to WLAN PC, and WLAN send traffic to DUT succesfully
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_dut_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Using LAN PC and repeat Step1~Step3
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    lanhost    ${g_dut_gw}

WLAN PC check throughput to LAN PC using iperf tool
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    wifi_client    ${DEVICES.lanhost.traffic_ip}
    Use Iperf Send Traffic and Verify Connection Successful    wifi_client    lanhost    ${DEVICES.lanhost.traffic_ip}    ${transfer_time}

*** comment ***
2017-12-12     Hans_Sun
Init the script
