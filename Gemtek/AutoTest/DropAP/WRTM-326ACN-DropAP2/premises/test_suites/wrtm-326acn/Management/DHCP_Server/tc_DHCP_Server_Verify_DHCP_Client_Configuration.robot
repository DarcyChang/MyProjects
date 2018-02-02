*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    50

*** Test Cases ***
tc_DHCP_Server_Verify_DHCP_Client_Configuration
    [Documentation]    The DHCP Client IP Address will be 192.168.55.xxx, Subnet Mask is 255.255.255.0, the Default Gateway is 192.168.55.1, the DHCP Server is 192.168.55.1 and the DNS Server is 192.168.55.1.
    [Tags]    @tcid=WRTM-326ACN-81   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    Verify DHCP Client IP Address, Subnet Mask, the Default Gateway, the DHCP Server and the DNS Server.
    All the DHCP Clients PC01 can access Internet properly via DUT.
    
    
*** Keywords ***
Login the DUT’s GUI to enable the DUT DHCP Server.
    [Arguments]
    [Documentation]    Test Step
    
    Config DEVICE DHCP Server Switch    web    on
    # Remove lease file so that dhcp client can forget old ip
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases
    
LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${lanhost_dhcpc_ip}
    Wait Until Keyword Succeeds    5x    3s    Check IP and Hostname Exist in the DHCP Client Table    web    dhcp_table    ${lanhost_dhcpc_ip}    ${DEVICES.lanhost.hostname}

    
Verify DHCP Client IP Address, Subnet Mask, the Default Gateway, the DHCP Server and the DNS Server.
    [Arguments]
    [Documentation]    Test Step
    
    # Get DHCP Lease Timeout
    ${dhcpc_lease_time}=    Get DHCP Server Lease Time    web
    Check DHCP Client Configuration   lanhost    ${g_lanhost_lease_file}    ${g_dut_gw_network_prefix}    ${g_dut_ip_mask}   ${g_dut_gw}    ${dhcpc_lease_time}    ${g_dut_gw}
    
    
All the DHCP Clients PC01 can access Internet properly via DUT.
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
    
    cli    lanhost    sudo killall dhclient
    Restore WAN Setting
    Delete Routing On Hosts
    Restore Lanhost IP

Restore Lanhost IP
    [Arguments]
    [Documentation]    Restore Lanhost IP
    [Tags]        
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}
       
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
       
    
*** comment ***
2017-09-10     Gemtek_Thomas_Chen
Init the script
