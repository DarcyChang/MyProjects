*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Performance    @AUTHOR=Hans_Sun
*** Variables ***
${transfer_time}    60

*** Test Cases ***
tc_LAN_PC_to_WAN_PC_with_throughput
    [Documentation]  tc_LAN_PC_to_WAN_PC_with_throughput
    ...    1. LAN PC connected to DUT
    ...    2. Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    ...    3. Using WAN PC and repeat Step1~Step3
    ...    4. LAN PC check throughput to WAN PC using iperf tool
    [Tags]   @TCID=WRTM-326ACN-452    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    LAN PC connected to DUT
    Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    Using WAN PC and repeat Step1~Step3
    LAN PC check throughput to WAN PC using iperf tool

*** Keywords ***
LAN PC connected to DUT
    [Tags]   @AUTHOR=Hans_Sun
    Check Lanhost IP

Verify DUT leaseed IP to LAN PC, and LAN send traffic to DUT succesfully
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    lanhost    ${g_dut_gw}

Using WAN PC and repeat Step1~Step3
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    ${WAN_IP} =    Wait Until Keyword Succeeds    5x    3s    Get DUT DHCP WAN IP
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    wanhost    ${WAN_IP}

LAN PC check throughput to WAN PC using iperf tool
    [Tags]   @AUTHOR=Hans_Sun
    Use Iperf Send Traffic and Verify Connection Successful    lanhost    wanhost    ${DEVICES.wanhost.traffic_ip}    ${transfer_time}

Check Lanhost IP
    [Tags]   @AUTHOR=Hans_Sun
    ${result} =    cli    lanhost    ifconfig ${DEVICES.lanhost.interface}
    ${IP} =    Get Regexp Matches    ${result}    192.168.66.(\\d+)
    log    ${IP}
    Should Contain    ${IP}[0]    192.168.66
*** comment ***
2017-12-15     Hans_Sun
Init the script
