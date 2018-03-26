*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Firewall    @AUTHOR=Hans_Sun
Test Teardown    Kill Ping Command
*** Variables ***

*** Test Cases ***
tc_SPI_Firewall_with_block_UDP_Flood_attack
    [Documentation]  tc_SPI_Firewall_with_block_UDP_Flood_attack
    ...    1. Setup WAN host and connected DUT WAN side.
    ...    2. WAN host simulate UDP Flood attack to DUT WAN IP and DUT can block this attack
    [Tags]   @TCID=WRTM-326ACN-359    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Setup WAN host and connected DUT WAN side
    WAN host simulate UDP Flood attack to DUT WAN IP and DUT can block this attack

*** Keywords ***
Setup WAN host and connected DUT WAN side
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    Login Web GUI
    Config DHCP Client

WAN host simulate UDP Flood attack to DUT WAN IP and DUT can block this attack
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun

    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall -9 hping3
    ${CPUStatueBeforeAttack} =  Checking DUT CPU State
    UDP Flood Attack
    ${CPUStatueAfterAttack} =  Checking DUT CPU State

    ${diff} =    Evaluate    ${CPUStatueBeforeAttack} - ${CPUStatueAfterAttack}
    run keyword if    ${diff} > 30    Fail    After attack,the CPU is busy in the DUT.

Kill Ping Command
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall -9 hping3

*** comment ***
2017-12-26     Hans_Sun
Init the script