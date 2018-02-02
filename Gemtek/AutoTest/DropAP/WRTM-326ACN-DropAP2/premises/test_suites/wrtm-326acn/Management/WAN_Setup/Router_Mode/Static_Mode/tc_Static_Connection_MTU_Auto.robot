*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=WAN_Static_IP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
*** Variables ***
${Traffic_count}    5
${MTU_Packet_size_maximum}    1452   #1480-28
${MTU_Packet_size_over_than_maximum}    1453   #1480-27

${Default_MTU}    1480

*** Test Cases ***
tc_Static_Connection_MTU_Auto
    [Documentation]    Ping greater than 1480 bytes packet from LAN to WAN side, check WAN side packet size and occur segment.
    [Tags]    @tcid=WRTM-326ACN-22   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Configure DUT with WAN Internet connection type to be Static IP mode, and MTU Auto mode.
    Wait Until Keyword Succeeds    5x    2s    Enable the Sniffer to capture Fragmented Packets after ping [1480 - 27] bytes packet from LAN to WAN side PC and Verify that packets of Fragmented IP Protocol which sent from DUT/Server both sides can be captured.
    Wait Until Keyword Succeeds    5x    2s    Enable the Sniffer to capture Fragmented Packets after ping [1480 - 28] bytes packet from LAN to WAN side PC and Verify that no packets of Fragmented IP Protocol which sent from DUT/Server both sides can be captured.
    Wait Until Keyword Succeeds    5x    2s    Configure mtu size of server side to 1480 bytes and Enable the Sniffer to capture Fragmented Packets after ping [1480 - 28] bytes packet from LAN to WAN side PC.

    
*** Keywords ***
Configure DUT with WAN Internet connection type to be Static IP mode, and MTU Auto mode.
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    10x    2s    Config WAN MTU     web    ${Default_MTU} 
    Config Static WAN and Check Internet    web    ${g_dut_static_ipaddr}    ${g_dut_static_netmask}    ${g_dut_static_gateway}    ${g_dut_static_dns1}
    
Enable the Sniffer to capture Fragmented Packets after ping [1480 - 27] bytes packet from LAN to WAN side PC and Verify that packets of Fragmented IP Protocol which sent from DUT/Server both sides can be captured.
    [Arguments]
    [Documentation]    Test Step
    
    sleep    15s
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    
    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    Check Recived ICMP Packet Status    ${dut_wan_ip}    ${MTU_Packet_size_over_than_maximum}    ${Traffic_count}
    Should Contain    ${val}    flags [+], proto ICMP (1)
    
Enable the Sniffer to capture Fragmented Packets after ping [1480 - 28] bytes packet from LAN to WAN side PC and Verify that no packets of Fragmented IP Protocol which sent from DUT/Server both sides can be captured.
    [Arguments]
    [Documentation]    Test Step

    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh

    #From dut, to check if packet is not fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    Check Recived ICMP Packet Status    ${dut_wan_ip}    ${MTU_Packet_size_maximum}    ${Traffic_count}
    Should Not Contain    ${val}    flags [+], proto ICMP (1)    

Configure mtu size of server side to 1480 bytes and Enable the Sniffer to capture Fragmented Packets after ping [1480 - 28] bytes packet from LAN to WAN side PC.    
    [Arguments]
    [Documentation]    Test Step
    
    #Check dhcp server's mtu to indicated value and test MTU_Packet_size_over_than_maximum again
    Config DHCP Server MTU    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.wan_vlan}     ${Default_MTU}
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    
    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    Check Recived ICMP Packet Status    ${dut_wan_ip}    ${MTU_Packet_size_over_than_maximum}    ${Traffic_count}
    Should Contain    ${val}    flags [+], proto ICMP (1)
    
Check Recived ICMP Packet Status
    [Arguments]    ${sender_ip}     ${ping_pkt_mtu}    ${ping_pkt_count}=5
    [Documentation]    Go to cli mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    #cli    dut1_ssh   killall tcpdump 
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump 
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S rm pfile
    # tcpdump will end the listening and push traffic log to /tmp/pfile if there are two packets received
    #cli    dut1_ssh   tcpdump -n -evvv -i ${DEVICES.dut1_ssh.wan_interface} 'ip[6] = 32' and dst host ${DEVICES.wanhost.traffic_ip} -c 2 -q > pfile &
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S tcpdump -n -evvv -i ${DEVICES.wanhost.interface} 'ip[6] = 32' and dst host ${DEVICES.wanhost.traffic_ip} -c 2 -q > pfile &

    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #lanhost use ping command line to send 5 packets with indicated size
    cli    lanhost    ping ${DEVICES.wanhost.traffic_ip} -s ${ping_pkt_mtu} -c ${ping_pkt_count} 

    ${df_val} =   cli    wanhost   cat pfile
    #${df_val} =   Get Line    ${df_val}    2
    log    ${df_val}
    [Return]    ${df_val}

    
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
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump

   
Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Restore WAN and DHCP Server Setting
    Delete Routing On Hosts
    
Restore WAN and DHCP Server Setting 
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Config WAN MTU     web    ${Default_MTU}
    Unconfig DHCP Server MTU    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.wan_vlan}
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
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-24     Gemtek_Thomas_Chen
Init the script
