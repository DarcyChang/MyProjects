*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=LAN    @AUTHOR=Jujung_Chang

Test Setup    LAN Host Release DHCP from DUT
Test teardown    run keywords    LAN Host Release DHCP from DUT
                 ...    AND
                 ...    Default IP Reset
*** Variables ***
${getIP}
${getIP1}
${LAN_PC1}    lanhost
${LAN_PC2}    wifi_client
*** Test Cases ***
tc_DHCP_Client_assign_IP_for_mutiple_LAN_host
    [Documentation]  tc_DHCP_Client_assign_IP_for_mutiple_LAN_host
    ...    1. Connect the LAN host to the DUT LAN port.  [Hardware Setup]
    ...    2. All the LAN host can get the IP Address from the DUT DHCP Server.
    ...    3. Check the Assign IP Address on GUI. [down for step2.]
    ...    4. All the DHCP Clients can access DUT.

    [Tags]   @TCID=WRTM-326ACN-446    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    All the LAN host can get the IP Address from the DUT DHCP Server
    All the DHCP Clients can access DUT

*** Keywords ***
All the LAN host can get the IP Address from the DUT DHCP Server
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Verify DUT leaseed IP to LAN PC1
    Verify DUT leaseed IP to LAN PC1(wifi_client)

Verify DUT leaseed IP to LAN PC1
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${getIP1} =  Leaseed IP to LAN PC    ${LAN_PC1}

Leaseed IP to LAN PC
    [Arguments]    ${host}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [return]    ${r}
    Renew IP address from the LAN side PC    ${host}
    ${r} =  Verify - DHCP client returns same IP address when LAN host renews    ${host}

Renew IP address from the LAN side PC
    [Arguments]    ${host}
    [Documentation]  Renew IP address from the LAN side PC
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    LAN Host Request DHCP from DUT

    #workaround for lease IP from DUT to LAN host
    sleep    3s
    cli    ${host}    echo '${DEVICES.${host}.password}' | sudo -S dhclient -r ${DEVICES.${host}.interface}
    sleep    3s
    cli    ${host}    echo '${DEVICES.${host}.password}' | sudo -S dhclient ${DEVICES.${host}.interface}
    sleep    3s

Verify - DHCP client returns same IP address when LAN host renews
    [Arguments]    ${host}
    [Documentation]  1. go to console to check IP.  2. Compare IP between GUI and console.
    [Tags]   @AUTHOR=Jujung_Chang
    [return]    ${getIP}
    cli    ${host}    ifconfig ${DEVICES.${host}.interface} | grep "inet addr:" > pfile
    cli    ${host}    ifconfig ${DEVICES.${host}.interface} | grep "inet addr:" > pfile
    ${getIP} =  cli    ${host}    cat pfile
    ${getIP} =  Get Line    ${getIP}    1
    log    ${getIP}
    ${getIP} =  Fetch From Right  ${getIP}    addr:
    ${getIP} =  Fetch From Left    ${getIP}    Bcast
    ${getIP} =  Strip String    ${getIP}
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status
    DHCP client returns same IP address when LAN host renews    ${getIP}

Verify DUT leaseed IP to LAN PC1(wifi_client)
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    1s    click links    web    Networking  Wireless
    Config Wireless Home Network    web
    Login Linux Wifi Client To Connect To DUT Without Security Key    wifi_client    ${g_dut_home_ssid}    ${DEVICES.wifi_client.int}    ${gui_url}
    ${getIP1} =  Leaseed IP to LAN PC    ${LAN_PC2}

All the DHCP Clients can access DUT
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    ${LAN_PC1}    ${g_dut_gw}
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    ${LAN_PC2}    ${g_dut_gw}

Default IP Reset
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S ifconfig ${DEVICES.lanhost.interface} ${DEVICES.lanhost.traffic_ip}
    cli    wifi_client    echo '${DEVICES.wifi_client.password}' | sudo -S ifconfig ${DEVICES.wifi_client.interface} ${DEVICES.wifi_client.assign_static_ip}

*** comment ***
2017-11-29     Jujung_Chang
Init the script
