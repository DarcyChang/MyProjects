*** Settings ***
Resource      ./base.robot
Force Tags    @FEATURE=Wireless

#Suite Setup  Routing setup
#Suite Teardown  Routing teardown

*** Variables ***
*** Test Cases ***
tc_Wireless_Init
    Routing setup

*** Keywords ***
Routing setup
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client    echo '${DEVICES.wifi_client.password}' | sudo -S sudo route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client_5g    echo '${DEVICES.wifi_client_5g.password}' | sudo -S sudo route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}

Routing teardown
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client    echo '${DEVICES.wifi_client.password}' | sudo -S sudo route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    wificlient cli    wifi_client_5g    echo '${DEVICES.wifi_client_5g.password}' | sudo -S sudo route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
