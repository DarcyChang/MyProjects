*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***


*** Test Cases ***
tc_DHCP_Server_Lease_Time
    [Documentation]    DHCP server returns the same IP Address when client renews
    [Tags]    @tcid=WRTM-326ACN-88   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    Configure the DHCP Lease Time as 59 minutes.
    Check the LAN PC01 IP Address information by typing ipconfig/all in windows command and check the Lease Time is 59 minutes.
    Configure the DHCP Lease Time as 2 minutes.
    Enable sniffer to catch the DHCP packet.
    LAN PC01 releases/renew the IP Address by typing ipconfig/release in windows command.
    Verify the PC01 will send out the DHCP Release packet.
    Verify the DUT will response the DHCP ACK packet. Check the LAN PC01 IP Address is the same by typing ipconfig/all in windows command.
    After 1 minutes, the LAN PC01 will send out the DHCP Request packet. DUT DHCP Server will send out the DHCP ACK packet to agree the request.
    LAN PC01 will lease the IP Address for 2 minutes.
    

*** Keywords ***
Login the DUT’s GUI to enable the DUT DHCP Server.
    [Arguments]
    [Documentation]    Test Step
    
    Config DEVICE DHCP Server Switch    web    on
    # Remove lease file so that dhcp client can forget old ip
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases

    
Configure the DHCP Lease Time as 59 minutes.
    [Arguments]
    [Documentation]    Test Step
    
    Config DHCP Server Lease Time    web    59    minutes
    
Check the LAN PC01 IP Address information by typing ipconfig/all in windows command and check the Lease Time is 59 minutes.
    [Arguments]
    [Documentation]    Test Step
    
    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${lanhost_dhcpc_ip}
    Wait Until Keyword Succeeds    5x    3s    Check IP and Hostname Exist in the DHCP Client Table    web    dhcp_table    ${lanhost_dhcpc_ip}    ${DEVICES.lanhost.hostname}
    
    # Get DHCP Lease Timeout
    ${dhcpc_lease_time}=    Get DHCP Server Lease Time    web
    log    ${dhcpc_lease_time}
    Check DHCP Client Configuration   lanhost    ${g_lanhost_lease_file}    ${g_dut_gw_network_prefix}    ${g_dut_ip_mask}   ${g_dut_gw}    ${dhcpc_lease_time}    ${g_dut_gw}

Configure the DHCP Lease Time as 2 minutes.
    [Arguments]
    [Documentation]    Test Step
    
    Config DHCP Server Lease Time    web    2    minutes
    
Enable sniffer to catch the DHCP packet.    
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo tcpdump -i ${DEVICES.lanhost.interface} port 67 or port 68 -e -n -c 10 > dhcp_pkg.log &


LAN PC01 releases/renew the IP Address by typing ipconfig/release in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface} -r
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface}
    sleep    3s
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases
    
    
Verify the PC01 will send out the DHCP Release packet.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo killall tcpdump
    ${pkg_log}=    cli    lanhost    cat dhcp_pkg.log
    Set Global Variable    ${g_pkg_log}    ${pkg_log}
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    BOOTP/DHCP, Request from ${DEVICES.lanhost.interface_mac}

    
Verify the DUT will response the DHCP ACK packet. Check the LAN PC01 IP Address is the same by typing ipconfig/all in windows command.
    [Arguments]
    [Documentation]    Test Step

    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    ${g_dut_gw}.67 > ${lanhost_dhcpc_ip}.68: BOOTP/DHCP, Reply
    
After 1 minutes, the LAN PC01 will send out the DHCP Request packet. DUT DHCP Server will send out the DHCP ACK packet to agree the request.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo tcpdump -i ${DEVICES.lanhost.interface} port 67 or port 68 -e -n -c 10 > dhcp_pkg.log &
    log to console    sleep 60 seconds to wait for dhcp lease
    sleep    60s
    cli    lanhost    sudo killall tcpdump
    ${g_pkg_log}=    cli    lanhost    cat dhcp_pkg.log
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    BOOTP/DHCP, Request from ${DEVICES.lanhost.interface_mac}

    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${g_pkg_log}
    Should Contain    ${g_pkg_log}    ${g_dut_gw}.67 > ${lanhost_dhcpc_ip}.68: BOOTP/DHCP, Reply
    
LAN PC01 will lease the IP Address for 2 minutes.
    [Arguments]
    [Documentation]    Test Step
    
    # Get DHCP Lease Timeout
    ${dhcpc_lease_time}=    Wait Until Keyword Succeeds    5x    2s    Get DHCP Server Lease Time    web
    log    ${dhcpc_lease_time}
    Check DHCP Client Configuration   lanhost    ${g_lanhost_lease_file}    ${g_dut_gw_network_prefix}    ${g_dut_ip_mask}   ${g_dut_gw}    ${dhcpc_lease_time}    ${g_dut_gw}

    

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
    
    cli    lanhost    sudo killall dhclient
    Restore Lanhost IP
    Config DHCP Server Lease Time    web    2    hours
    Config DHCP Server IP Range    web    ${g_dut_gw_dhcp_server_start_ip}    ${g_dut_gw_dhcp_server_end_ip}

Restore Lanhost IP
    [Arguments]
    [Documentation]    Restore Lanhost IP
    [Tags]        
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}
    

    
    
*** comment ***
2017-09-10     Gemtek_Thomas_Chen
Init the script
