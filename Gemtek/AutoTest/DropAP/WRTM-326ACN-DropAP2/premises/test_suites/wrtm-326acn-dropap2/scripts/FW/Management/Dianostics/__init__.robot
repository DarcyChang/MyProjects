*** Settings ***
Resource      ./base.robot

Suite Setup    Routing setup
#Suite Teardown    Routing teardown

*** Keywords ***
Routing setup
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route add -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route add -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}

Routing teardown
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route del -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route del -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}
