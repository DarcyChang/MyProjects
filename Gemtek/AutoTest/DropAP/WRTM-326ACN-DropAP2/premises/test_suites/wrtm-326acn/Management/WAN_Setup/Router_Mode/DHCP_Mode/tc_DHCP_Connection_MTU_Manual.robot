*** Settings ***

Resource    ./base.robot

Force Tags    @FEATURE=WAN_DHCP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_count}    5
${Default_MTU}    1500
 
${Test_MTU_Size1}    576
${Test_MTU_Packet_size1}    548    #${Test_MTU_Size1} - 28    
${Test_MTU_Packet_over_than_maximum_size1}=     549    #${Test_MTU_Packet_size1} - 27

${Test_MTU_Size2}    1492
${Test_MTU_Packet_size2}    1464    #${Test_MTU_Size2} - 28    
${Test_MTU_Packet_over_than_maximum_size2}    1465     #${Test_MTU_Packet_size2} - 27


*** Test Cases ***
tc_DHCP_Connection_MTU_Manual
    [Documentation]    DHCP mode MTU value should be from 576 to 1492 Bytes, check setting result and meet segment packet size.
    [Tags]    @tcid=WRTM-326ACN-10    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    #Enable DHCP Server of WAN side.
    Configure DUT with WAN Internet connection type to be DHCP mode, and minute MTU size equal 576. 
    Ping (576- 27) bytes packet from LAN to WAN side PC and verify that packets should be fragmented and Enable the Sniffer to capture Fragmented Packets after ping (576- 27) bytes packet from LAN to WAN side PC.Verify that packets for Fragmented IP Protocol can be captured.
    Enable the Sniffer to capture Fragmented Packets after ping (576 - 28) bytes packet from LAN to WAN side PC and Check that Fragmented IP Protocol should NOT be captured.
    #Varify that Total Lan size of ICMP packets will be 576 bytes.
    Configure DUT with MTU size up to 1492.
    Ping greater than 1464 bytes packet from LAN to WAN side PC and verify that packets should be fragmented and Enable the Sniffer to capture Fragmented Packets after ping 1465 bytes packet from LAN to WAN side PC. Verify that packets for Fragmented IP Protocol can be captured.
    Enable the Sniffer to capture Fragmented Packets after ping 1464 bytes packet from LAN to WAN side PC and Check that Fragmented IP Protocol should NOT be captured.
    #Varify that Total Lan size of ICMP packets will be 1492 bytes.


*** Keywords ***
Configure DUT with WAN Internet connection type to be DHCP mode, and minute MTU size equal 576. 
    [Arguments]
    [Documentation]    Test Step
    
    Config WAN MTU     web    ${Test_MTU_Size1}    
    Wait Until Keyword Succeeds    10x    5s    Config DHCP WAN And Check Internet    web
    
Ping (576- 27) bytes packet from LAN to WAN side PC and verify that packets should be fragmented and Enable the Sniffer to capture Fragmented Packets after ping (576- 27) bytes packet from LAN to WAN side PC. Verify that packets for Fragmented IP Protocol can be captured.
    [Arguments]
    [Documentation]    Test Step
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    
    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_wan_ip}   ${Test_MTU_Packet_over_than_maximum_size1}    ${Traffic_count}
    Should Contain    ${val}    flags [+], proto ICMP (1)
    
Enable the Sniffer to capture Fragmented Packets after ping (576 - 28) bytes packet from LAN to WAN side PC and Check that Fragmented IP Protocol should NOT be captured.
    [Arguments]
    [Documentation]    Test Step
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh

    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_wan_ip}   ${Test_MTU_Packet_size1}    ${Traffic_count}
    Should Not Contain    ${val}    flags [+], proto ICMP (1)
    
Configure DUT with MTU size up to 1492.
    [Arguments]
    [Documentation]    Test Step
    
    Config WAN MTU     web    ${Test_MTU_Size2}  
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web
    
Ping greater than 1464 bytes packet from LAN to WAN side PC and verify that packets should be fragmented and Enable the Sniffer to capture Fragmented Packets after ping 1465 bytes packet from LAN to WAN side PC. Verify that packets for Fragmented IP Protocol can be captured.
    [Arguments]
    [Documentation]    Test Step

    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    
    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_wan_ip}   ${Test_MTU_Packet_over_than_maximum_size2}    ${Traffic_count}
    Should Contain    ${val}    flags [+], proto ICMP (1)
    
    
Enable the Sniffer to capture Fragmented Packets after ping 1464 bytes packet from LAN to WAN side PC and Check that Fragmented IP Protocol should NOT be captured.
    [Arguments]
    [Documentation]    Test Step
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh

    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_wan_ip}   ${Test_MTU_Packet_size2}    ${Traffic_count}
    Should Not Contain    ${val}    flags [+], proto ICMP (1)
    
Verify MTU Size 
    [Arguments]    ${dut_ip}    ${mtu_size}    ${pkt_size_maximum}    ${pkt_size_over_maximum}
    [Documentation]    Configure MTU in Advanced setting
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    #From dut, to check if packet is not fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_ip}    ${pkt_size_maximum}    ${Traffic_count}
    Should Not Contain    ${val}    flags [+], proto ICMP (1)
    
    #From dut, to check if packet is fragmented if it's over indicated mtu size
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Fragmentation Test    ${dut_ip}    ${pkt_size_over_maximum}    ${Traffic_count}
    Should Contain    ${val}    flags [+], proto ICMP (1)
    

ICMP Fragmentation Test
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
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
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
