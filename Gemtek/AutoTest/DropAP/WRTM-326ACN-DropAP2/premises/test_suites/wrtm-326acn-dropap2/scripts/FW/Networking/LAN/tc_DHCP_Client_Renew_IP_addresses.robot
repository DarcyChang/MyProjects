*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=LAN    @AUTHOR=Jujung_Chang

Test Setup    LAN Host Release DHCP from DUT
Test teardown    LAN Host Release DHCP from DUT

*** Variables ***
${getIP}
*** Test Cases ***
tc_DHCP_Client_Renew_IP_addresses
    [Documentation]  tc_DHCP_Client_Renew_IP_addresses
    ...    1. Renew IP address from the LAN side PC.
    ...    2. Verify - DHCP client returns same IP address when LAN host renews.

    [Tags]   @TCID=WRTM-326ACN-444    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Renew IP address from the LAN side PC
    Verify - DHCP client returns same IP address when LAN host renews

*** Keywords ***
Renew IP address from the LAN side PC
    [Documentation]  Renew IP address from the LAN side PC
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    LAN Host Request DHCP from DUT

    #workaround for lease IP from DUT to LAN host
    sleep    3s
    cli    lanhost    sudo dhclient -r ${DEVICES.lanhost.interface}
    sleep    3s
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S dhclient ${DEVICES.lanhost.interface}
    sleep    3s

Verify - DHCP client returns same IP address when LAN host renews
    [Documentation]  1. go to console to check IP.  2. Compare IP between GUI and console.
    [Tags]   @AUTHOR=Jujung_Chang
    cli    lanhost    ifconfig ${DEVICES.lanhost.interface} | grep "inet addr:" > pfile
    cli    lanhost    ifconfig ${DEVICES.lanhost.interface} | grep "inet addr:" > pfile
    ${getIP} =  cli    lanhost    cat pfile
    ${getIP} =  Get Line    ${getIP}    1
    log    ${getIP}
    ${getIP} =  Fetch From Right  ${getIP}    addr:
    ${getIP} =  Fetch From Left    ${getIP}    Bcast
    ${getIP} =  Strip String    ${getIP}
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status
    DHCP client returns same IP address when LAN host renews    ${getIP}

*** comment ***
2017-11-27     Jujung_Chang
Init the script
