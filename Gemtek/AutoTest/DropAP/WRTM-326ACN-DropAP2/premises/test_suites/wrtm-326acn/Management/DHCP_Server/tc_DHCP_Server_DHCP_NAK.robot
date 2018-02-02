*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${assigned_id}    0
${assigned_ip_1}    192.168.55.249
${assigned_ip_2}    192.168.55.120


*** Test Cases ***
tc_DHCP_Server_DHCP_NAK
    [Documentation]    DHCP server returns the same IP Address when client renews
    [Tags]    @tcid=WRTM-326ACN-87   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    At the LAN PC01 sniffer the DHCP packet.
    Configure the LAN01 IP Address as 192.168.15.120 form the Static DHCP Client Table.
    Typing the ipconifg/renew in windows command.
    The PC01 will send out the DHCP Request packet with IP Address 192.168.15.xxx.
    DUT DHCP Server will send out the DHCP NACK packet to reject the request.


*** Keywords ***
Login the DUT’s GUI to enable the DUT DHCP Server.
    [Arguments]
    [Documentation]    Test Step
    
    Config DEVICE DHCP Server Switch    web    on
    Unconfig Static DHCP Client    web    ${assigned_id}
    Config DHCP Server IP Range    web    ${g_dut_gw_dhcp_server_start_ip}    ${g_dut_gw_dhcp_server_end_ip}
    Config DHCP Server Lease Time    web    2    hours
    # Remove lease file so that dhcp client can forget old ip
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases
    
LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    Config Static DHCP Client    web    ${assigned_id}    ${assigned_ip_1}    ${DEVICES.lanhost.interface_mac}
    ${val_static_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log many    ${val_static_dhcpc_ip}
    Should Match    ${val_static_dhcpc_ip}    ${assigned_ip_1}
    
At the LAN PC01 sniffer the DHCP packet.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo tcpdump -i ${DEVICES.lanhost.interface} port 67 or port 68 -e -n -c 10 > dhcp_pkg.log &

Configure the LAN01 IP Address as 192.168.15.120 form the Static DHCP Client Table.
    [Arguments]
    [Documentation]    Test Step
    
    
    Config Static DHCP Client    web    ${assigned_id}    ${assigned_ip_2}    ${DEVICES.lanhost.interface_mac}
    #${val_static_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    #log many    ${val_static_dhcpc_ip}
    #Should Match    ${val_static_dhcpc_ip}    ${assigned_ip_2}
    
Typing the ipconifg/renew in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface} -r
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface}
    
The PC01 will send out the DHCP Request packet with IP Address 192.168.15.xxx.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo killall tcpdump
    ${pkg_log}=    cli    lanhost    cat dhcp_pkg.log
    Set Global Variable    ${g_pkg_log}    ${pkg_log}
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    BOOTP/DHCP, Request from ${DEVICES.lanhost.interface_mac}

    
DUT DHCP Server will send out the DHCP NACK packet to reject the request.
    [Arguments]
    [Documentation]    Test Step

    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    ${g_dut_gw}.67 > ${lanhost_dhcpc_ip}.68: BOOTP/DHCP, Reply
    
    
Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
    
    Login Web GUI
    
    
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
   
Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Unconfig Static DHCP Client    web    ${assigned_id}
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases
    cli    lanhost    sudo killall dhclient
    Restore Lanhost IP

Restore Lanhost IP
    [Arguments]
    [Documentation]    Restore Lanhost IP
    [Tags]        
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}
    

    
    
*** comment ***
2017-09-10     Gemtek_Thomas_Chen
Init the script
