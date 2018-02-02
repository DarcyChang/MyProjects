*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=L2TP/PPTP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    50
${ppp_username}    test
${ppp_password}    test
${L2TP_TYPE_FULL}    full
${L2TP_START_WHEN_BOOT}    False
${L2TP_FORCE_ENCRYPTION}    False

*** Test Cases ***
tc_L2TP_Full
    [Documentation]    Configure L2TP and check status
    [Tags]    @tcid=WRTM-326ACN-154    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Reset DUT and Config DHCP WAN
    Configure L2TP including server ip, username, password, Select "Full" mode and save the settings.
    Press "Click" to start the service, then status change "Connected"
    From Console, Check the L2TP status. Check traffic from lan to vpn internal lan

*** Keywords ***
Reset DUT and Config DHCP WAN
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    5x    3s    Config DHCP WAN    web
    Wait Until Keyword Succeeds    10x    5s    Internet Status Should be Up    web
    
Configure L2TP including server ip, username, password, Select "Full" mode and save the settings.
    [Arguments]
    [Documentation]    Test Step    
    
    Config PPTP_L2TP    web    l2tp    ${DEVICES.cisco.gateway}    ${ppp_username}    ${ppp_password}    ${L2TP_TYPE_FULL}    ${L2TP_START_WHEN_BOOT}    ${L2TP_FORCE_ENCRYPTION}
    
Press "Click" to start the service, then status change "Connected"
    [Arguments]
    [Documentation]    Test Step  
    
    Config PPTP_L2TP Connect    web
    Wait Until Keyword Succeeds    5x    5s    Check PPTP_L2TP Connected    web

From Console, Check the L2TP status. Check traffic from lan to vpn internal lan
    [Arguments]
    [Documentation]    Test Step  
    # Get L2TP ip so we can check if wanhost can received packet from this L2TP address
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    5s     Get IP Value From Device SSH Connection    dut1_ssh     ${DEVICES.rf1.l2tp_interface}

    #Wanhost check 50 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Hping_TCP_Traffic_Test     ${dut_wan_ip}
    
Hping_TCP_Traffic_Test
    [Arguments]    ${sender_ip}
    [Documentation]    Hping_TCP_Traffic_Test
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #Wanhost use tcpdump command line waitting for reciving 50 packets
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.wanhost.interface} tcp dst port ${Traffic_port} -c 5 -q > pfile &

    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #lanhost use hping command line to send 50 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S hping3 ${DEVICES.wanhost.traffic_ip} -S -p ${Traffic_port} -c ${Traffic_count} -i u100 -I ${DEVICES.lanhost.interface}
    sleep    2s
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    ${result} =   cli    wanhost    cat pfile
    log    ${result}
    Should Contain    ${result}    ${sender_ip}


Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
    
    Add Routing On Hosts
    Login Web GUI
    
    
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

    
Add Routing On Hosts
    [Arguments]
    [Documentation]    Configure routing to lanhost and wanhost
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    Config Traffic IP to TGN Interface    wanhost    ${DEVICES.lanhost.password}    ${DEVICES.wanhost.interface}    ${DEVICES.wanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}

   
Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Restore WAN Setting
    Delete Routing On Hosts
    
    
Restore WAN Setting    
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Config PPTP_L2TP    web    l2tp    ${DEVICES.cisco.gateway}    ${ppp_username}    ${ppp_password}    full    False    False
    Config PPTP_L2TP Disconnect    web
    Wait Until Keyword Succeeds    5x    3s    Check PPTP_L2TP Disconnected    web
    Config DHCP WAN and Check Internet     web
    
Delete Routing On Hosts
    [Arguments]
    [Documentation]    Unconfigure routing to lanhost and wanhost
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump

    

*** comment ***
2017-09-08     Gemtek_Thomas_Chen
Init the script
