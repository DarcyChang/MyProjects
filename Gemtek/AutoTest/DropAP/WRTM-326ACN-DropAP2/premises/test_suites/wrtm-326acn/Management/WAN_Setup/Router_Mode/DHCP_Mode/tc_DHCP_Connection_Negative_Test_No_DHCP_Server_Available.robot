*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=WAN_DHCP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_count}    5
 
*** Test Cases ***
tc_DHCP_Connection_Negative_Test_No_DHCP_Server_Available
    [Documentation]    Verify has no any IP information on monitor page when DUT does not connect DHCP server.
    [Tags]    @tcid=WRTM-326ACN-16    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    
    Verify has no any IP information on monitor page when DUT does not connect DHCP server.
    
    
    
*** Keywords ***
Verify has no any IP information on monitor page when DUT does not connect DHCP server.
    [Arguments]
    [Documentation]    Test Step
    
    Config Cisco Vlan on Ethernet Port    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.test_ethernet_port}    ${DEVICES.cisco.wan_vlan} 

    Config DHCP WAN And Check Internet    web
    Test Ping from Lanhost to Wanhost Should Succeed

    Config Cisco Vlan on Ethernet Port    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.test_ethernet_port}    ${DEVICES.cisco.wan_vlan} 
    Test Internet Status Should be Up

    Config Cisco Vlan on Ethernet Port    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.test_ethernet_port}    ${DEVICES.cisco.false_wan_vlan} 
    Test Internet Status Should be Down

    Config Cisco Vlan on Ethernet Port    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.test_ethernet_port}    ${DEVICES.cisco.wan_vlan} 
    Test Internet Status Should be Up

    
Test Internet Status Should be Up
    [Arguments]
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web

Test Internet Status Should be Down
    [Arguments]
    [Documentation]    
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    Wait Until Keyword Succeeds    15x    3s    Internet Status Should be Down    web    

Test Ping from Lanhost to Wanhost Should Succeed
    [Arguments]
    [Documentation]    To get wan ip address from dut ssh connection
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    ${val} =    Wait Until Keyword Succeeds    5x    3s    ICMP Test    ${dut_wan_ip}    ${Traffic_count}
    Should Contain    ${val}    proto ICMP


ICMP Test
    [Arguments]    ${sender_ip}     ${ping_pkt_count}=5  
    [Documentation]    Go to cli mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    # Clean up previous possible tcpdump in the background
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S killall tcpdump 
    # tcpdump will end the listening and push traffic log to /tmp/pfile if there are two packets received
    cli    wanhost   echo '${DEVICES.wanhost.password}' | sudo -S tcpdump -n -evvv -i ${DEVICES.wanhost.interface} icmp and dst host ${DEVICES.wanhost.traffic_ip} -c 2 -q > pfile &

    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #lanhost use ping command line to send 5 packets with indicated size
    cli    lanhost    ping ${DEVICES.wanhost.traffic_ip} -c ${ping_pkt_count} 

    ${df_val} =   cli    wanhost   cat pfile
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
    
    Config Cisco Vlan on Ethernet Port    ${DEVICES.cisco.vendor}    ${DEVICES.cisco.test_ethernet_port}    ${DEVICES.cisco.wan_vlan} 
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

2017-08-25     Gemtek_Thomas_Chen
1. Create more common keywords for GUI configuration
2. Modify the test case itself to a clean format, and move rest to keywords

2017-08-24     Gemtek_Thomas_Chen
Init the script
