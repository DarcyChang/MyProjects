*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Internet_Connection    @AUTHOR=Jujung_Chang

*** Variables ***
${getIP}
*** Test Cases ***
tc_Default_WAN_mode
    [Documentation]  tc_Default_WAN_mode
    ...    1. Reset the DUT to factory default setting from the DUT reset button.
    ...    2. WAN host connect to the DUT WAN port.  [Hardware Setup]
    ...    3. At WAN host sniffer the WAN DHCP packets.
    ...    4. Verify the DUT WAN obtain IP address correctly.
    [Tags]   @TCID=WRTM-326ACN-389    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]
    [setup]    Setting Company DNS Only on Cisco Server    ${g_dut_DNS_from_company}
    [teardown]    Adding Default DNS Setting On Cisco Server

    Reset the DUT to factory default setting from the DUT reset button
    At DUT sniffer the WAN DHCP packets
    Verify the DUT WAN obtain IP address correctly

*** Keywords ***
Reset the DUT to factory default setting from the DUT reset button
    [Documentation]  Reset the DUT to factory default setting from the DUT reset button
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Click Reset Button And Verify Function Is Work

At DUT sniffer the WAN DHCP packets
    [Documentation]  At WAN host sniffer the WAN DHCP packets
    [Tags]   @AUTHOR=Jujung_Chang
    Config Setup DropAP
    Go to Diagnostics
    Ping Using DropAP GUI    ${DEVICES.wanhost.traffic_ip}
    sleep   3s
    Should Be Contain Text At Diagnostics Page    ${DEVICES.wanhost.traffic_ip}

Verify the DUT WAN obtain IP address correctly
    [Documentation]  Verify the DUT WAN obtain IP address correctly
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ${getIP} =  Check Address on the IPv4 WAN Status Table Is Valid    web
    ${r} =  Wait Until Keyword Succeeds    5x    3s    cli    dut1    ifstatus wan | grep address
    should contain    ${r}    ${getIP}

*** comment ***
2017-11-22     Jujung_Chang
Init the script
