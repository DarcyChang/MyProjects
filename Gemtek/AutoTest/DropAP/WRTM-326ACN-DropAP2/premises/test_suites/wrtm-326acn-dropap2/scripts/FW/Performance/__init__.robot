*** Settings ***
Resource      ./base.robot

Suite Setup  Routing setup

*** Keywords ***
Routing setup
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client    echo '${DEVICES.wifi_client.password}' | sudo -S sudo route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route add -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}
