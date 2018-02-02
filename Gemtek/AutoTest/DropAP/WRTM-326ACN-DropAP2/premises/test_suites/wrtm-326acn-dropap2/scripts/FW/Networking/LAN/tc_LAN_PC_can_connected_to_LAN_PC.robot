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
${LAN_PC2}    vm1
*** Test Cases ***
tc_LAN_PC_can_connected_to_LAN_PC
    [Documentation]  tc_LAN_PC_can_connected_to_LAN_PC
    ...    1. LAN PC1 connected to DUT.  [Hardware Setup]
    ...    2. Verify DUT leaseed IP to LAN PC1.
    ...    3. PC1 send traffic to DUT succesfully.
    ...    4. Connect the LAN PC02 to the DUT LAN port.
    ...    5. LAN PC1 send traffic to LAN PC2 is succesfully.

    [Tags]   @TCID=WRTM-326ACN-445    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    Connect the LAN PC01 to the DUT LAN port
    Verify DUT leaseed IP to LAN PC1
    PC1 send traffic to DUT succesfully
    Connect the LAN PC02 to the DUT LAN port
    LAN PC1 send traffic to LAN PC2 is succesfully

*** Keywords ***
Connect the LAN PC01 to the DUT LAN port
    [Documentation]  Connect the LAN PC01 to the DUT LAN port
    [Tags]   @AUTHOR=Jujung_Chang
    Is Linux Ping Successful    lanhost    ${DEVICES.dut1.ip}

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
    cli    ${host}    sudo dhclient -r ${DEVICES.${host}.interface}
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

PC1 send traffic to DUT succesfully
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    PC send traffic to DUT succesfully    ${LAN_PC1}

PC send traffic to DUT succesfully
    [Arguments]    ${host}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    ${host}    ${gui_url}

Connect the LAN PC02 to the DUT LAN port
    [Documentation]    PC2 is vagrant PC. We don't need to using dhclient to get IP, Because it's will cause remote disconnected.
    [Tags]   @AUTHOR=Jujung_Chang
    PC send traffic to DUT succesfully    ${LAN_PC2}

LAN PC1 send traffic to LAN PC2 is succesfully
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${DEVICES.vm1.traffic_ip}

Default IP Reset
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S ifconfig ${DEVICES.lanhost.interface} ${DEVICES.lanhost.traffic_ip}

*** comment ***
2017-11-27     Jujung_Chang
Init the script
