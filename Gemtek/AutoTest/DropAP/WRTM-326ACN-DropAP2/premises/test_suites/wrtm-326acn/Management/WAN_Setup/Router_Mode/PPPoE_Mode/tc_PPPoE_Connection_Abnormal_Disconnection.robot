*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_PPPoE    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***

${Traffic_port}    8888
${Traffic_count}    20
${pppoe_username}    test
${pppoe_password}    test

*** Test Cases ***
tc_PPPoE_Connection_Abnormal_Disconnection
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]   @tcid=WRTM-326ACN-40    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Connect a PPPoE Server on WAN side. Configure WAN Internet connection type to be PPPoE mode.
    LAN PC can have the Internet access properly.
    Disconnect the PPPoE connection from the PPPoE server.
    Check the DUT will build the PPPoE connection automatically.
    LAN PC can still have the Internet access properly.
    
*** Keywords ***
Connect a PPPoE Server on WAN side. Configure WAN Internet connection type to be PPPoE mode.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    5x    2s    Config PPPoE WAN    web    ${pppoe_username}    ${pppoe_password}
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web

    
LAN PC can have the Internet access properly.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    10x    6s     Get Wan IP Value From Device SSH Connection    dut1_ssh    pppoe
    log    ${dut_wan_ip}
    #Wanhost check 50 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Hping_TCP_Traffic_Test     ${dut_wan_ip}

Disconnect the PPPoE connection from the PPPoE server.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    
    cli    cisco     \r\n
    cli    cisco     enable     timeout=20
    cli    cisco     clear pppoe all
    cli    cisco     clear pppoe all
    
    sleep     3s
    
    Wait Until Keyword Succeeds    15x    2s    Internet Status Should be Down    web
    sleep    30s
    
Check the DUT will build the PPPoE connection automatically.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    10x    5s    Internet Status Should be Up    web

LAN PC can still have the Internet access properly.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    LAN PC can have the Internet access properly.
    
Hping_TCP_Traffic_Test
    [Arguments]    ${sender_ip}
    [Documentation]    Go to cli mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #Wanhost use tcpdump command line waitting for reciving 50 packets
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S rm pfile
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.wanhost.interface} tcp dst port ${Traffic_port} -c ${Traffic_count} -q > pfile &

    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #lanhost use hping command line to send 50 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S hping3 ${DEVICES.wanhost.traffic_ip} -S -p ${Traffic_port} -c ${Traffic_count} -i u100 -I ${DEVICES.lanhost.interface}

    
    # Sleep 2 seconds to wait for hping packets
    sleep    2s
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    sleep    2s
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
    
    Wait Until Keyword Succeeds    5x    2s    Config DHCP WAN and Check Internet     web
    
Delete Routing On Hosts
    [Arguments]
    [Documentation]    Unconfigure routing to lanhost and wanhost
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump

    

*** comment ***
2017-09-09     Gemtek_Thomas_Chen
Init the script
