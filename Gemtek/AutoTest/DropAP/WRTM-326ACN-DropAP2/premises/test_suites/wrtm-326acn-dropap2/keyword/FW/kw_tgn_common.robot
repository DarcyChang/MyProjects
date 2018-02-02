*** Settings ***

*** Variables ***

*** Keywords ***
Is Linux Ping Successful
    [Arguments]    ${device}    ${gw_ip}     ${ping_count}=3
    [Documentation]    To check ping ${gw_ip} is successful
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c ${ping_count}
    log    ${result}
    Should contain    ${result}    bytes from

Is Linux Ping Fail
    [Arguments]    ${device}    ${gw_ip}    ${ping_count}=3
    [Documentation]    To check ping ${gw_ip} is fail
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c ${ping_count}    timeout=15    timeout_exception=0
    log    ${result}
    Should Contain    ${result}    100% packet loss

Is Linux Ping URL Fail
    [Arguments]    ${device}    ${gw_ip}    ${ping_count}=3
    [Documentation]    To check ping ${gw_ip} is fail
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c ${ping_count}    timeout=15    timeout_exception=0
    log    ${result}
    Should Contain    ${result}    unknown host

Using Hping with TCP Port Successful Or Not
    [Arguments]    ${src_device}    ${dst_device}    ${dstip}    ${EnabledPort}
    [Documentation]    Using Hping with TCP Port

    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S killall tcpdump
    sleep    3s
    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S tcpdump -n -i ${DEVICES.${dst_device}.interface} tcp port ${EnabledPort} > pfile -c 2 &
    sleep    3s
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -p ${EnabledPort} -I ${DEVICES.${src_device}.interface} -c 1
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -p ${EnabledPort} -I ${DEVICES.${src_device}.interface} -c 1
    sleep    3s
    ${ret}   cli    ${dst_device}   cat pfile
    ${ret}   cli    ${dst_device}   cat pfile
    log    ${ret}

    Should contain    ${ret}    ${dstip}.${EnabledPort}

Using Hping with UDP Port Successful Or Not
    [Arguments]    ${src_device}    ${dst_device}    ${dstip}    ${EnabledPort}
    [Documentation]    Using Hping with TCP Port

    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S killall tcpdump
    sleep    3s
    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S tcpdump -n -i ${DEVICES.${dst_device}.interface} udp port ${EnabledPort} > pfile -c 2 &
    sleep    3s
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -2 -p ${EnabledPort} -I ${DEVICES.${src_device}.interface} -c 1
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -2 -p ${EnabledPort} -I ${DEVICES.${src_device}.interface} -c 1
    sleep    3s
    ${ret}   cli    ${dst_device}   cat pfile
    ${ret}   cli    ${dst_device}   cat pfile
    log    ${ret}

    Should contain    ${ret}    ${dstip}.${EnabledPort}

Using Hping with TCP AND UDP Port At the Same Time Successful Or Not
    [Arguments]    ${src_device}    ${dst_device}    ${dstip}    ${EnabledTCPPort}    ${EnabledUDPPort}
    [Documentation]    Using Hping with TCP and UDP Port at the same time.

    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S killall tcpdump
    sleep    3s
    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S tcpdump -n -i ${DEVICES.${dst_device}.interface} tcp port ${EnabledTCPPort} > pfile1 -c 3 &
    cli    ${dst_device}    echo '${DEVICES.${dst_device}.password}' | sudo -S tcpdump -n -i ${DEVICES.${dst_device}.interface} udp port ${EnabledUDPPort} > pfile2 -c 3 &
    sleep    3s

    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -p ${EnabledTCPPort} -I ${DEVICES.${src_device}.interface} -c 3 &
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -2 -p ${EnabledUDPPort} -I ${DEVICES.${src_device}.interface} -c 3 &
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -p ${EnabledTCPPort} -I ${DEVICES.${src_device}.interface} -c 3 &
    cli    ${src_device}    echo '${DEVICES.${src_device}.password}' | sudo -S hping3 ${dstip} -S -2 -p ${EnabledUDPPort} -I ${DEVICES.${src_device}.interface} -c 3 &

    sleep    7s
    ${ret1}   cli    ${dst_device}   cat pfile1
    ${ret1}   cli    ${dst_device}   cat pfile1
    ${ret1}   cli    ${dst_device}   cat pfile1
    log    ${ret1}
    ${ret2}   cli    ${dst_device}   cat pfile2
    ${ret2}   cli    ${dst_device}   cat pfile2
    ${ret2}   cli    ${dst_device}   cat pfile2
    log    ${ret2}

    Should contain    ${ret1}    ${dstip}.${EnabledTCPPort}
    Should contain    ${ret2}    ${dstip}.${EnabledUDPPort}

Checking Packet Not Greater Than MTU And Won't Be Freagment
    [Arguments]    ${MTU_Maximum}
    [Documentation]    MTU checking
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    sleep   3s
    cli    wanhost    sudo tcpdump -n -evvv -i ${DEVICES.wanhost.interface} 'ip[6] = 32' > pfile &
    sleep   3s
    cli    lanhost    sudo ping ${DEVICES.wanhost.traffic_ip} -s ${MTU_Maximum} -c 3
    cli    lanhost    sudo ping ${DEVICES.wanhost.traffic_ip} -s ${MTU_Maximum} -c 3
    sleep    3s
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    ${ret}    cli    wanhost    cat pfile
    ${ret}    cli    wanhost    cat pfile
    Should Not Contain    ${ret}    flags [+]

Checking Packet Greater Than MTU And Will Be Freagment
    [Arguments]    ${MTU_Maximum}
    [Documentation]    MTU checking
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    sleep   3s
    cli    wanhost    sudo tcpdump -n -evvv -i ${DEVICES.wanhost.interface} 'ip[6] = 32' > pfile &
    sleep   3s
    cli    lanhost    sudo ping ${DEVICES.wanhost.traffic_ip} -s ${MTU_Maximum} -c 3
    cli    lanhost    sudo ping ${DEVICES.wanhost.traffic_ip} -s ${MTU_Maximum} -c 3
    sleep    3s
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    ${ret}    cli    wanhost    cat pfile
    ${ret}    cli    wanhost    cat pfile
    Should Contain    ${ret}    flags [+]

LAN Host Request DHCP from DUT
    [Documentation]    MTU checking
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S killall dhclient
    sleep    1s
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S dhclient ${DEVICES.lanhost.interface}

LAN Host Release DHCP from DUT
    [Documentation]    MTU checking
    [Tags]    @AUTHOR=Gemtek_Jujung_Chang
    cli    lanhost    sudo dhclient -r ${DEVICES.lanhost.interface}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S ifconfig ${DEVICES.lanhost.interface} ${DEVICES.lanhost.traffic_ip}

Checking NTP packets When Modified NTP Server On GUI
    [Documentation]    To check NTP port =123 on console.
    [Tags]   @AUTHOR=Jujung_Chang

    Run Keyword And Ignore Error    cli    dut1    killall tcpdump
    cli    dut1    tcpdump -n -i ${DEVICES.dut1.wan_interface} | grep 123 > pfile &

    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

    #Modified a new NTP sverver on GUI. In order to check TCP port packets.
    Modify NTP Candidate Name    0    time.stdtime.gov.tw
    #Modified other NTP again. Sometimes we can not capture TCP packets.
    Modify NTP Candidate Name    0    tick.stdtime.gov.tw
    sleep    5s
    Run Keyword And Ignore Error    cli    dut1    killall tcpdump
    Modify NTP Candidate Name    0    0.openwrt.pool.ntp.org
    sleep    1s
    ${r} =  cli    dut1    cat pfile
    ${r} =  cli    dut1    cat pfile
    log    ${r}
    Should Contain    ${r}    .123

Checking NTP packets When Modified NTP Server On GUI Is Failed
    [Documentation]    To check NTP port =123 on console.
    [Tags]   @AUTHOR=Jujung_Chang

    Run Keyword And Ignore Error    cli    dut1    killall tcpdump
    cli    dut1    tcpdump -n -i ${DEVICES.dut1.wan_interface} port 123 > pfile &
    Modify NTP Candidate Name    0    ${Dummy_Candidate_Name_0}
    sleep    5s
    ${r} =  cli    dut1    cat pfile
    ${r} =  cli    dut1    cat pfile
    log    ${r}
    Should Not Contain    ${r}    .123

*** comment ***
2017-11-08     Gemtek_Jujung_Chang
Copy from wrtm-326acn project.