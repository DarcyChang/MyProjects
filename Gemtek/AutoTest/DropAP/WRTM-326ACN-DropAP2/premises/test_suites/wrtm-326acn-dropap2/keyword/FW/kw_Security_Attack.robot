*** Settings ***

*** Variables ***

*** Keywords ***
Get WAN IP On GUI
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${value}
    [Timeout]    10s
    ${value} =  Wait Until Keyword Succeeds    5x    3s    Retry Get WAN Status    web
    ${value} =   Get Line    ${value}    1
    ${value} =   Fetch From Right    ${value}    Address:
    ${value} =   Strip String    ${value}
    log    ${value}

Checking DUT CPU State
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${ret}
    [Timeout]    10s
    Wait Until Keyword Succeeds    5x    3s    cli    dut1    top > pfile &
    sleep    1s
    Wait Until Keyword Succeeds    5x    3s    cli    dut1    killall top
    ${ret} =  Wait Until Keyword Succeeds    5x    3s    cli    dut1   cat pfile
    ${ret} =  Wait Until Keyword Succeeds    5x    3s    cli    dut1   cat pfile

    ${ret} =   Get Line    ${ret}    2
    ${ret} =   Fetch From Right    ${ret}    nic
    ${ret} =   Fetch From Left    ${ret}    idle
    ${ret} =   Fetch From Left    ${ret}    %
    ${ret} =   Strip String    ${ret}
    ${ret} =   Convert To Integer    ${ret}

Ping Of Death
    [Arguments]    ${Packet_Size}
    [Documentation]    Using large quantity ping with packet size is 65507(65535-28)
    [Tags]    @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =  Get WAN IP On GUI
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} -1 -I ${DEVICES.wanhost.interface} -d ${Packet_Size} -i u20 &
    sleep    5s

SYN Flood Attack
    [Documentation]    Using hping3 with SYN flood to attack DUT
    [Tags]    @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =    Wait Until Keyword Succeeds    5x    3s    Get DUT DHCP WAN IP
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} -S --flood &
    sleep    5s

Xmas Attack
    [Arguments]
    [Documentation]
    [Tags]    @AUTHOR=Jujung_Chang

    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =  Get WAN IP On GUI
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} -V -p 80 -s 5050 -M 0 -UPF --faster &
    sleep    5s

LAND Attack
    [Arguments]
    [Documentation]
    [Tags]    @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =  Get WAN IP On GUI
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 -a ${IP} ${IP} -i u20 &
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 -a ${IP} ${IP} -i u20 &
    sleep    5s

UDP Flood Attack
    [Documentation]    Using hping3 with UDP flood to attack DUT
    [Tags]    @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =    Wait Until Keyword Succeeds    5x    3s    Get DUT DHCP WAN IP
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} --udp -p 68 --flood &
    sleep    5s

Lanhost Traceroute to Gateway by through DUT
    [Documentation]    Lanhost Traceroute to Gateway by through DUT
    [Tags]    @AUTHOR=Hans_Sun
    Run Keyword And Ignore Error    Wait Until Keyword Succeeds    3x    1s    cli    lanhost    echo ${DEVICES.lanhost.password} | sudo -S route add -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.dut1.ip}
    Wait Until Keyword Succeeds    3x    2s    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sudo hping3 --traceroute -V -1 ${DEVICES.cisco.gateway} --faster &
    Wait Until Keyword Succeeds    3x    2s    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sudo hping3 --traceroute -V -1 ${DEVICES.cisco.gateway} --faster &
    sleep    5s

Black Nurse Attack
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =    Wait Until Keyword Succeeds    5x    3s    Get DUT DHCP WAN IP
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} --icmp -C 3 -K 3 -i u10 &
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${IP} --icmp -C 3 -K 3 -i u10 &
    sleep    5s

Null Scan Attack
    [Arguments]
    [Documentation]
    [Tags]    @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =  Get WAN IP On GUI
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 -p 80 -s 5050 -Y ${IP} -i u10 &
    sleep    5s

IP Spoofing Attack
    [Arguments]
    [Documentation]
    [Tags]    @AUTHOR=Jujung_Chang
    Wait Until Keyword Succeeds    10x    2s    click links    web    Status  Overview
    ${IP} =  Get WAN IP On GUI
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 -p 80 ${IP} -S --spoof 0.0.0.0 -i u10 &
    Wait Until Keyword Succeeds    3x    2s    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 -p 80 ${IP} -S --spoof 0.0.0.0 -i u10 &
    sleep    7s