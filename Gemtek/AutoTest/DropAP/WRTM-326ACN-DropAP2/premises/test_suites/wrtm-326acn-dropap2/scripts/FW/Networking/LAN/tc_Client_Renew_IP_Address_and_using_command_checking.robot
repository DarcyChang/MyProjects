*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=LAN    @AUTHOR=Jujung_Chang

Test Setup    LAN Host Release DHCP from DUT
Test teardown    LAN Host Release DHCP from DUT
*** Variables ***
${getIP}
*** Test Cases ***
tc_Client_Renew_IP_Address_and_using_command_checking
    [Documentation]  tc_Client_Renew_IP_Address_and_using_command_checking
    ...    1. Connect the LAN PC01 to the DUT LAN port.
    ...    2. LAN host can get the IP Address from the DUT DHCP Server.
    ...    3. Check the LAN host IP Address by typing ifconfig in command.
    ...    4. At the LAN host sniffer the DHCP packet.
    ...    5. Typing the dhclient -r command and set default IP.
    ...    6. Check the LAN host IP Address is the same by typing ifconfig in command.

    [Tags]   @TCID=WRTM-326ACN-447    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    Connect the LAN PC01 to the DUT LAN port
    LAN host can get the IP Address from the DUT DHCP Server
    Check the LAN host IP Address by typing ifconfig in command
    At the LAN host sniffer the DHCP packet
    Typing the dhclient -r command and set default IP
    Check the LAN host IP Address is the same by typing ifconfig in command

*** Keywords ***
Connect the LAN PC01 to the DUT LAN port
    [Documentation]  Connect the LAN PC01 to the DUT LAN port
    [Tags]   @AUTHOR=Jujung_Chang
    Is Linux Ping Successful    lanhost    ${DEVICES.dut1.ip}

LAN host can get the IP Address from the DUT DHCP Server
    [Documentation]  LAN host can get the IP Address from the DUT DHCP Server
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    LAN Host Request DHCP from DUT

    #workaround for lease IP from DUT to LAN host
    sleep    3s
    cli    lanhost    sudo dhclient -r ${DEVICES.lanhost.interface}
    sleep    3s
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S dhclient ${DEVICES.lanhost.interface}
    sleep    3s

Check the LAN host IP Address by typing ifconfig in command
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

At the LAN host sniffer the DHCP packet
    [Documentation]  At the LAN host sniffer the DHCP packet
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    Is Linux Ping Successful    lanhost    ${gui_url}

Typing the dhclient -r command and set default IP
    [Documentation]  Typing the ipconifg/renew in command
    [Tags]   @AUTHOR=Jujung_Chang
    LAN Host Release DHCP from DUT

Check the LAN host IP Address is the same by typing ifconfig in command
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
    should be equal    ${getIP}    ${DEVICES.lanhost.traffic_ip}

*** comment ***
2017-11-28     Jujung_Chang
Init the script
