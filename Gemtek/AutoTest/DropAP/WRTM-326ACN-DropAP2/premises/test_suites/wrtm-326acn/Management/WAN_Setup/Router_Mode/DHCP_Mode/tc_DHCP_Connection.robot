*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_DHCP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    50

*** Test Cases ***
tc_DHCP_Connection
    [Documentation]    The DUT WAN interface should get a DHCP lease with IP, DNS lease-time and Gateway Address.
    [Tags]    @tcid=WRTM-326ACN-7    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Configure WAN Internet connection type to be DHCP mode.
    #Connect WAN port to a DHCP Server and configure the DHCP Server Lease Time as 10 mins.
    #At WAN PC sniffer the WAN DHCP packet.
    DUT will follow the DHCP packet procedure to get IP Address.
    #DUT send out the DHCP Discovery packet, DHCP Server send out the DHCP Offer packet, DUT send   out the DHCP Request packet and DHCP Server send out the DHCP ACK packet.
    #Check both the DHCP Discovery and DHCP Request packet are broadcast packet.
    #Verify WAN Port IP information.
    #LAN PC can have the Internet access properly.
    #Verify the DUT will send out the DHCP Request packet after 5 mins.
    #Check the DUT will lease the same IP Address.
    LAN PC can have the Internet access properly.

*** Keywords ***
Configure WAN Internet connection type to be DHCP mode.
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    5x    3s    Config DHCP WAN    web
    
DUT will follow the DHCP packet procedure to get IP Address.
    [Arguments]
    [Documentation]    Test Step    
    
    Wait Until Keyword Succeeds    10x    5s    Internet Status Should be Up    web
    
LAN PC can have the Internet access properly.
    [Arguments]
    [Documentation]    Test Step

    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh

    #Wanhost check 50 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Hping_TCP_Traffic_Test     ${dut_wan_ip}
    

Hping_TCP_Traffic_Test
    [Arguments]    ${sender_ip}
    [Documentation]    Hping_TCP_Traffic_Test
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #Wanhost use tcpdump command line waitting for reciving 50 packets
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.wanhost.interface} tcp dst port ${Traffic_port} -c ${Traffic_count} -q > pfile &

    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #lanhost use hping command line to send 50 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S hping3 ${DEVICES.wanhost.traffic_ip} -S -p ${Traffic_port} -c ${Traffic_count} -i u100 -I ${DEVICES.lanhost.interface}

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
    
    Config DHCP WAN and Check Internet     web
    
Delete Routing On Hosts
    [Arguments]
    [Documentation]    Unconfigure routing to lanhost and wanhost
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.network_route} netmask ${g_dut_ip_mask} gw ${g_dut_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S route del -net ${DEVICES.wanhost.route} netmask ${DEVICES.wanhost.route_mask} gw ${DEVICES.wanhost.default_gw}
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}

*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-24     Gemtek_Thomas_Chen
Init the script
