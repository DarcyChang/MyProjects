*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Firewall    @AUTHOR=Jujung_Chang
Test Teardown    Kill Ping Command
*** Variables ***
*** Test Cases ***
tc_SPI_Firewall_with_block_IP_Spoofing_attack
    [Documentation]  tc_SPI_Firewall_with_block_IP_Spoofing_attack
    ...    1. Setup WAN host and connected DUT WAN side.
    ...    2. WAN host simulate IP Spoofing attack to LAN host and DUT can block this attack.

    [Tags]   @TCID=WRTM-326ACN-326    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Setup WAN host and connected DUT WAN side
    WAN host simulate IP Spoofing attack to LAN host and DUT can block this attack

*** Keywords ***
Setup WAN host and connected DUT WAN side
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    Login Web GUI
    Config DHCP Client

WAN host simulate IP Spoofing attack to LAN host and DUT can block this attack
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall -9 hping3
    ${CPUStatueBeforeAttack} =  Checking DUT CPU State
    IP Spoofing Attack
    ${CPUStatueAfterAttack} =  Checking DUT CPU State

    Run Keyword And Ignore Error    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall hping3
    ${diff} =  Evaluate    ${CPUStatueBeforeAttack} - ${CPUStatueAfterAttack}
    run keyword if    ${diff} > 30    Fail    After attack,the CPU is busy in the DUT.

Kill Ping Command
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    sudo killall -9 hping3

*** comment ***
2017-12-26     Jujung_Chang
Init the script
