*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***

*** Test Cases ***
tc_Wireless_Table_checking_home_connection
    [Documentation]  tc_Wireless_Table_checking_home_connection
    ...    1. Turn on Wireless 2.4G and 5G
    ...    2. Wireless clients associate with DUT
    ...    3. Verify Wireless status should be displayed (For HOME Network)
    [Tags]   @TCID=WRTM-326ACN-281    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Turn on Wireless 2.4G and 5G
    Wireless clients associate with DUT
    Verify Wireless status should be displayed (For HOME Network)

*** Keywords ***
Turn on Wireless 2.4G and 5G
    [Documentation]  Turn on Wireless 2.4G and 5G
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web

Wireless clients associate with DUT
    [Documentation]  Wireless clients associate with DUT
    [Tags]   @AUTHOR=Hans_Sun
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_dut_home_ssid}    ${DEVICES.wifi_client.int}    ${g_dut_gw}

Verify Wireless status should be displayed (For HOME Network)
    [Documentation]  Verify Wireless status should be displayed (For HOME Network)
    [Tags]   @AUTHOR=Hans_Sun
    ${r}  run keyword and return status    Verify Wifi Client On Wireless Status GUI    ${Lease_status_table}    ${DEVICES.wifi_client.hostname}
    run keyword if  '${r}'=='False'    Wait Until Keyword Succeeds    3x    1s    Retry to Check DHCP Leases

*** comment ***
2017-11-21     Hans_Sun
Add keyword "Retry to Check DHCP Leases" to improve stability
2017-11-06     Hans_Sun
Init the script
