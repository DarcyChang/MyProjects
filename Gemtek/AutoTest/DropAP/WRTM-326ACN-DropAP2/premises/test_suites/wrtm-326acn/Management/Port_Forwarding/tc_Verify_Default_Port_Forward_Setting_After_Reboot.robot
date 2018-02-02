*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=Port_Forwarding    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_count}    10
@{Port_Fordward_Disabled_List}    1  2 
@{Port_Fordward_Enabled_List}    4  5

*** Test Cases ***
tc_Verify_Default_Port_Forward_Setting_After_Reboot
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]   @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Configure WAN Internet connection type to be DHCP mode.
    Disabled Some Port Forward Rules.
    Enabled Some Port Forward Rules.
    Reboot Device and Check Login.
    Verify the WAN IP Address Information at the WAN Status if correct.
    Verify Disabled Port Forward Rules No Traffic Passing Through.
    Verify Enabled Port Forward Rules Has Traffic Passing Through.
    
*** Keywords ***
Configure WAN Internet connection type to be DHCP mode.
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    10x    2s    Config DHCP WAN    web

Disabled Some Port Forward Rules.
    [Arguments]
    [Documentation]    Test Step

    #Use for-loop to get all port forward list and check no traffic passing through
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_Disabled_List}    off

Enabled Some Port Forward Rules.
    [Arguments]
    [Documentation]    Test Step

    #Use for-loop to get all port forward list and check no traffic passing through
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_Enabled_List}    on

Reboot Device and Check Login.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Reboot Device and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

Verify the WAN IP Address Information at the WAN Status if correct.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web

Verify Enabled Port Forward Rules Has Traffic Passing Through.
    [Arguments]
    [Documentation]    Test Step    

    #Use for-loop to get all port forward list and check no traffic passing through
    :FOR    ${Port_Forward_ID}    IN    @{Port_Fordward_Enabled_List}
    \    Verify Default Port Forward Rule    ${Port_Forward_ID}
    
    
Verify Default Port Forward Rule
    [Arguments]    ${pf_index}
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${ret_switch_on}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}    Get Port Forward Setting From Specified Index    web    ${pf_index}
    log Many    ${ret_switch_on}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}
    
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    Run Keyword If    ${ret_switch_on}    Start Send Traffic and Check Packet Status    ${dut_wan_ip}    ${ret_pf_int_ip}    ${ret_pf_ext_port}    ${ret_pf_int_port}
    

Start Send Traffic and Check Packet Status
    [Arguments]    ${dut_wan_ip}    ${lanhost_ip}    ${ext_Port}    ${int_Port}
    [Documentation]    Check send packet is failed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    #Config lanhost IP
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${lanhost_ip}
    Is Linux Ping Successful    lanhost    ${DEVICES.dut1.ip}    5
    
    #Lanhost use tcpdump command line waitting for reciving 10 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sudo killall tcpdump
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.lanhost.interface} tcp dst port ${int_Port} -c ${Traffic_count} -q > pfile &
    #Verify tcpdump is completed ,so sleep here.
    sleep    2s
    #wanhost use hping command line to send 10 packets
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${dut_wan_ip} -S -p ${ext_Port} -c ${Traffic_count} -i u500
    
    sleep    2s
    ${result} =   cli    lanhost    cat pfile
    log    ${result}
    Should Contain   ${result}    ${int_Port}

Verify Disabled Port Forward Rules No Traffic Passing Through.
    [Arguments]    
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    
    log    ${Port_Fordward_Disabled_List}

    #Use for-loop to get all port forward list and check no traffic passing through
    :FOR    ${Port_Forward_ID}    IN    @{Port_Fordward_Disabled_List}
    \    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}    Get Port Forward Setting From Specified Index    web    ${Port_Forward_ID}
    \    log Many    ${ret_switch_ret}    ${ret_pf_ext_port}    ${ret_pf_int_port}    ${ret_pf_int_ip}
    \    Should Not Be True    ${ret_switch_ret}
    \    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    2s     Get Wan IP Value From Device SSH Connection    dut1_ssh
    \    log    ${dut_wan_ip}
    \    Start Send Traffic and Check No Packet Received    ${dut_wan_ip}    ${ret_pf_int_ip}    ${ret_pf_ext_port}    ${ret_pf_int_port}
    
    
Start Send Traffic and Check No Packet Received
    [Arguments]    ${dut_wan_ip}    ${lanhost_ip}    ${ext_Port}    ${int_Port}
    [Documentation]    Check send packet is failed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    #Config lanhost IP
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${lanhost_ip}
    Is Linux Ping Successful    lanhost    ${DEVICES.dut1.ip}    5
    
    #Lanhost use tcpdump command line waitting for reciving 10 packets
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S sudo killall tcpdump
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S tcpdump -n -i ${DEVICES.lanhost.interface} tcp dst port ${int_Port} -c ${Traffic_count} -q > pfile &
    #Verify tcpdump is completed ,so sleep here.
    sleep    2s
    #wanhost use hping command line to send 10 packets
    cli    wanhost    echo '${DEVICES.wanhost.password}' | sudo -S hping3 ${dut_wan_ip} -S -p ${ext_Port} -c ${Traffic_count} -i u500
    
    sleep    2s
    ${result} =   cli    lanhost    cat pfile
    log    ${result}
    Should Not Contain   ${result}    ${int_Port}
    
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
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_Disabled_List}    on

*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-28     Gemtek_Thomas_Chen
Init the script
