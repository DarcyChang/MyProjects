*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Wireless    @AUTHOR=Hans_Sun
Suite Teardown   Recover Wireless Page Settings
*** Variables ***

*** Test Cases ***
tc_2.4G_Wireless_for_Guest_Network_Connection_with_Radio_On
    [Documentation]  tc_2.4G_Wireless_for_Guest_Network_Connection_with_Radio_On
    ...    1. Turn on wireless radio and setting SSID at Guest Network on DUT
    ...    2. Verify 2.4G WIFI client connect DUT successfully.
    ...    3. Verify Wifi client will wget 192.168.67.1 successfully.
    [Tags]   @TCID=WRTM-326ACN-432    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on wireless radio and setting SSID at Guest Network on DUT
    Verify 2.4G WIFI client connect DUT successfully
    Verify Wifi client will wget 192.168.67.1 successfully

*** Keywords ***
Turn on wireless radio and setting SSID at Guest Network on DUT
    [Documentation]  Turn on wireless radio and setting SSID at Guest Network on DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Config Wireless Guest Network    web    on

Verify 2.4G WIFI client connect DUT successfully
    [Documentation]  Verify 2.4G WIFI client connect DUT successfully
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    3s    Retry Wifi Client Connect to DUT

Verify Wifi client will wget 192.168.67.1 successfully
    [Tags]   @AUTHOR=Hans_Sun
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient -r ${DEVICES.wifi_client.int}
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ${wifi_ip} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Client DHCP IP Value
    Wait Until Keyword Succeeds    5x    3s    Is Linux Ping Successful    dut1    ${wifi_ip}

Retry Wifi Client Connect to DUT
    Login Linux Wifi Client To Connect To DUT With Guest SSID    wifi_client    ${g_dut_guest_ssid}    ${DEVICES.wifi_client.int}
    Wait Until Keyword Succeeds    10x    3s    Is WIFI Interface Up    wifi_client    ${g_dut_guest_ssid}

*** comment ***
2017-12-11     Hans_Sun
Modify traffic from dut to wifi-client
2017-11-22     Hans_Sun
Init the script
