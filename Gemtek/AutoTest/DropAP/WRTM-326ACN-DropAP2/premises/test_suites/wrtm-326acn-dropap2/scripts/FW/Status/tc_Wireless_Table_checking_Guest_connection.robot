*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Status    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_Wireless_Table_checking_Guest_connection
    [Documentation]  tc_Wireless_Table_checking_Guest_connection
    ...    1. Enable Wireless 2.4G and 5G
    ...    2. Wireless clients associate with DUT
    ...    3. Verify Wireless clients should be displayed ( For Guest Network)
    [Tags]   @TCID=WRTM-326ACN-282    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on Wireless 2.4G and 5G
    Wireless clients associate with DUT
    Verify Wireless clients should be displayed ( For Guest Network)

*** Keywords ***
Turn on Wireless 2.4G and 5G
    [Documentation]  Turn on Wireless 2.4G and 5G
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Config Wireless Guest Network    web    on

Wireless clients associate with DUT
    [Documentation]  Wireless clients associate with DUT
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    3s    Retry Wifi Client Connect to DUT
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value
    Wait Until Keyword Succeeds    5x    3s    Is Linux wget Successful    dut1    ${wifi_ip}

Verify Wireless clients should be displayed ( For Guest Network)
    [Tags]   @AUTHOR=Hans_Sun
    ${r}  run keyword and return status    Verify Wifi Client On Wireless Status GUI    ${Lease_status_table}    ${DEVICES.wifi_client.hostname}
    run keyword if  '${r}'=='False'    Wait Until Keyword Succeeds    3x    1s    Retry to Check DHCP Leases

Retry Wifi Client Connect to DUT
    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_dut_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    wifi_client    ${g_dut_guest_ssid}

*** comment ***
2017-11-21     Hans_Sun
Init the script
