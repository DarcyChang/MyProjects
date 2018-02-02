*** Settings ***
Resource      ./base.robot

Suite Setup    Setup Route
Suite Teardown    Remove Route

*** Keywords ***
Setup Route
    [Documentation]
    Setting Route On WAN Host
    Setting Route On LAN Host
Remove Route
    Remove Route On WAN Host
    Remove Route On LAN Host

Setting Route On WAN Host
    [Documentation]  Setting Route On WAN Host
    [Tags]   @AUTHOR=Jujung_Chang

    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route add -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}

Setting Route On LAN Host
    [Documentation]  Setting Route On LAN Host
    [Tags]   @AUTHOR=Jujung_Chang

    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route add -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}

Remove Route On WAN Host
    [Documentation]  Remove Route On WAN Host
    [Tags]   @AUTHOR=Jujung_Chang

    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route del -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}

Remove Route On LAN Host
    [Documentation]  Remove Route On LAN Host
    [Tags]   @AUTHOR=Jujung_Chang

    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route del -net ${DEVICES.wanhost.network_route}/24 gw ${DEVICES.dut1.ip}