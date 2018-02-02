*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=Port_Forwarding    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_count}    5
@{Port_Fordward_List}    10  11
#@{Port_Fordward_List}    1  2  3  4  5  6  7  8  9  10  11  12  13

*** Test Cases ***
tc_Verify_No_Traffic_Passing_Through_When_Port_Forwarding_Rule_is_Disabled_Static_IP
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]    @tcid=WRTM-326ACN-39    @tcid=WRTM-326ACN-55    @tcid=WRTM-326ACN-56    @tcid=WRTM-326ACN-57    @tcid=WRTM-326ACN-58    @tcid=WRTM-326ACN-59
    ...    @tcid=WRTM-326ACN-60    @tcid=WRTM-326ACN-62    @tcid=WRTM-326ACN-63    @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Setting the WAN IP Address, Subnet Mask, Default Gateway and DNS Address which ISP provided.
    Verify the WAN IP Address Information at the WAN Status if correct.
    Disabled Default Port Forward Rule and Check No Traffic Passing Through on TCP.
    Disabled Default Port Forward Rule and Check No Traffic Passing Through on UDP.
    
    
*** Keywords ***
Setting the WAN IP Address, Subnet Mask, Default Gateway and DNS Address which ISP provided.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    10x    2s    Config Static WAN    web    ${g_dut_static_ipaddr}    ${g_dut_static_netmask}    ${g_dut_static_gateway}    ${g_dut_static_dns1}
    
Verify the WAN IP Address Information at the WAN Status if correct.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web
    
Disabled Default Port Forward Rule and Check No Traffic Passing Through on TCP.
    [Arguments]    
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    log    ${Port_Fordward_List}

    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_List}    off

    #Use for-loop to get all port forward list and check no traffic passing through
    :FOR    ${Port_Forward_ID}    IN    @{Port_Fordward_List}
    \    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}    Get Port Forward Setting From Specified Index    web    ${Port_Forward_ID}
    \    log Many    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}
    \    Should Not Be True    ${ret_switch_ret}
    \    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    \    log    ${dut_wan_ip}
    \    Start Send Traffic and Check No Packet Received    ${dut_wan_ip}    ${ret_pf_int_ip}    ${ret_pf_ext_port}    ${ret_pf_int_port}    tcp

Disabled Default Port Forward Rule and Check No Traffic Passing Through on UDP.
    [Arguments]    
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    log    ${Port_Fordward_List}

    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_List}    off

    #Use for-loop to get all port forward list and check no traffic passing through
    :FOR    ${Port_Forward_ID}    IN    @{Port_Fordward_List}
    \    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}    Get Port Forward Setting From Specified Index    web    ${Port_Forward_ID}
    \    log Many    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}
    \    Should Not Be True    ${ret_switch_ret}
    \    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    \    log    ${dut_wan_ip}
    \    Start Send Traffic and Check No Packet Received    ${dut_wan_ip}    ${ret_pf_int_ip}    ${ret_pf_ext_port}    ${ret_pf_int_port}    udp
    
    
Start Send Traffic and Check No Packet Received
    [Arguments]    ${dut_wan_ip}    ${lanhost_ip}    ${ext_Port}    ${int_Port}    ${datagram_type}=tcp
    [Documentation]    Check send packet is failed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    #Config lanhost IP
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${lanhost_ip}
    Is Linux Ping Successful    lanhost    ${DEVICES.dut1.ip}    5
    
    #Lanhost use tcpdump command line waitting for reciving 10 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sudo killall tcpdump
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.lanhost.interface} ${datagram_type} dst port ${int_Port} -c ${Traffic_count} -q > pfile &
    #Verify tcpdump is completed ,so sleep here.
    sleep    2s
    #wanhost use hping command line to send 10 packets
    Run Keyword If    '${datagram_type}' == 'tcp'    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${dut_wan_ip} -S -p ${ext_Port} -c ${Traffic_count} -i u500 &
    ...    ELSE      cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${dut_wan_ip} -S -p ${ext_Port} -c ${Traffic_count} -i u500 -2 &
    
    sleep    2s
    ${result} =   cli    lanhost    cat pfile
    log    ${result}
    Should Not Contain   ${result}    ${int_Port}
    cli    wanhost    killall tcpdump

    
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
    
    Enable Default Port Forward Rule
    Restore WAN Setting
    Delete Routing On Hosts
    Restore Lanhost IP
    
    
Restore Lanhost IP
    [Arguments]
    [Documentation]    Restore Lanhost IP
    [Tags]        
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    
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

Enable Default Port Forward Rule
    [Arguments]    
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    

    #Use for-loop to get all port forward list and check no traffic passing through	
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_List}    on
    
    

*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-28     Gemtek_Thomas_Chen
Init the script
