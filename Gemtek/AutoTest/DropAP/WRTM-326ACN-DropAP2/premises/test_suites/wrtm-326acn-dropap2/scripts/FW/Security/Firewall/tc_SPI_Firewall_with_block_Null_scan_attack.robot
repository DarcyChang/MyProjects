*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Firewall    @AUTHOR=Jujung_Chang
Test Teardown    Kill Ping Command
*** Variables ***
*** Test Cases ***
tc_SPI_Firewall_with_block_Null_scan_attack
    [Documentation]  tc_SPI_Firewall_with_block_Null_scan_attack
    ...    1. Setup WAN host and connected DUT WAN side.
    ...    2. WAN host simulate block null scan to DUT and DUT can block this attack.

    [Tags]   @TCID=WRTM-326ACN-398    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup WAN host and connected DUT WAN side
    WAN host simulate block null scan to DUT and DUT can block this attack

*** Keywords ***
Setup WAN host and connected DUT WAN side
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    Login Web GUI
    Config DHCP Client

WAN host simulate block null scan to DUT and DUT can block this attack
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    sudo killall -9 hping3
    ${CPUStatueBeforeAttack} =  Checking DUT CPU State
    Null Scan Attack
    ${CPUStatueAfterAttack} =  Checking DUT CPU State

    ${diff} =  Evaluate    ${CPUStatueBeforeAttack} - ${CPUStatueAfterAttack}
    run keyword if    ${diff} > 30    Fail    After attack,the CPU is busy in the DUT.

Kill Ping Command
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    sudo killall -9 hping3

*** comment ***
2018-1-3     Jujung_Chang
Init the script
