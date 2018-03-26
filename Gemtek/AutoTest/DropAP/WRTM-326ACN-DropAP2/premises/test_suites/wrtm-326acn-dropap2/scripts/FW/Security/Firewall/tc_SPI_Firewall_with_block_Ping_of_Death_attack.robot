*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Firewall    @AUTHOR=Jujung_Chang
Test Teardown    Kill Ping Command
*** Variables ***
${Packet_Size}    70000
*** Test Cases ***
tc_SPI_Firewall_with_block_Ping_of_Death_attack
    [Documentation]  tc_SPI_Firewall_with_block_Ping_of_Death_attack
    ...    1. Setup WAN host and connected DUT WAN side.
    ...    2. WAN host simulate Ping of Death attack to DUT WAN IP and DUT can block this attack.

    [Tags]   @TCID=WRTM-326ACN-369    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup WAN host and connected DUT WAN side
    WAN host simulate Ping of Death attack to DUT WAN IP and DUT can block this attack

*** Keywords ***
Setup WAN host and connected DUT WAN side
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    Login Web GUI
    Config DHCP Client

WAN host simulate Ping of Death attack to DUT WAN IP and DUT can block this attack
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall -9 hping3
    ${CPUStatueBeforeAttack} =  Checking DUT CPU State
    Ping Of Death    ${Packet_Size}
    ${CPUStatueAfterAttack} =  Checking DUT CPU State

    ${diff} =    Evaluate    ${CPUStatueBeforeAttack} - ${CPUStatueAfterAttack}
    run keyword if    ${diff} > 30    Fail    After attack,the CPU is busy in the DUT.

Kill Ping Command
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall hping3

*** comment ***
2017-12-21     Jujung_Chang
Init the script