*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Performance    @AUTHOR=Hans_Sun
*** Variables ***
${transfer_time}    50

*** Test Cases ***
tc_LAN_PC_to_WLAN_PC_with_throughput
    [Documentation]  tc_LAN_PC_to_WLAN_PC_with_throughput
    ...    1. LAN PC connected to DUT
    ...    2. Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    ...    3. Using WLAN PC and repeat Step1~Step3
    ...    4. LAN PC check throughput to WLAN PC using iperf tool
    [Tags]   @TCID=WRTM-326ACN-454    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    LAN PC connected to DUT
    Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    Using WLAN PC and repeat Step1~Step3
    LAN PC check throughput to WLAN PC using iperf tool

*** Keywords ***
LAN PC connected to DUT
    [Tags]   @AUTHOR=Hans_Sun
    Check Lanhost IP

Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    lanhost    ${g_dut_gw}

Using WLAN PC and repeat Step1~Step3
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web
    Wait Until Keyword Succeeds    3x    1s    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_dut_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

LAN PC check throughput to WLAN PC using iperf tool
    [Tags]   @AUTHOR=Hans_Sun
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value
    Wait Until Keyword Succeeds    5x    3s    Is Linux wget Successful    lanhost    ${wifi_ip}
    Wait Until Keyword Succeeds    3x    1s    Use Iperf Send Traffic and Verify Connection Successful    lanhost    wifi_client    ${wifi_ip}    ${transfer_time}

Check Lanhost IP
    [Tags]   @AUTHOR=Hans_Sun
    ${result} =    cli    lanhost    ifconfig ${DEVICES.lanhost.interface}
    ${IP} =    Get Regexp Matches    ${result}    192.168.66.(\\d+)
    log    ${IP}
    Should Contain    ${IP}[0]    192.168.66

*** comment ***
2017-12-12     Hans_Sun
Init the script
