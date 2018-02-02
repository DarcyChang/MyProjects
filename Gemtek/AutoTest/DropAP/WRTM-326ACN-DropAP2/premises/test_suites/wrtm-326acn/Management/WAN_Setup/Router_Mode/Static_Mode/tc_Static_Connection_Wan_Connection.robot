*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_Static_IP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    50

*** Test Cases ***
tc_Static_Connection_Wan_Connection
    [Documentation]    LAN to WAN communication success in Static ip mode
    [Tags]    @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    
    Setting the WAN IP Address, Subnet Mask, Default Gateway and DNS Address which ISP provided.
    Verify the WAN IP Address Information at the WAN Status if correct.
    Make sure the LAN PC can have the Internet access properly.
    
*** Keywords ***
Setting the WAN IP Address, Subnet Mask, Default Gateway and DNS Address which ISP provided.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Config Static WAN    web    ${g_dut_static_ipaddr}    ${g_dut_static_netmask}    ${g_dut_static_gateway}    ${g_dut_static_dns1}
    
Verify the WAN IP Address Information at the WAN Status if correct.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Internet Status Should be Up    web
    
Make sure the LAN PC can have the Internet access properly.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh

    #Wanhost check 50 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Hping_TCP_Traffic_Test     ${dut_wan_ip}
    
Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}    
    
    # Add routing to lan and wan host
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route add -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}


Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
        
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    Config Traffic IP to TGN Interface    wanhost    ${DEVICES.lanhost.password}    ${DEVICES.wanhost.interface}    ${DEVICES.wanhost.traffic_ip}
    # Unconfigure routing to lanhost and wanhost
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    
    #Config default device wan setting back
    Config DHCP WAN and Check Internet     web


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

    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    ${result} =   cli    wanhost    cat pfile
    log    ${result}
    Should Contain    ${result}    ${sender_ip}

*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-24     Gemtek_Thomas_Chen
Init the script
