*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***

*** Test Cases ***
tc_DHCP_Server_Renew_IP
    [Documentation]    DHCP server returns the same IP Address when client renews
    [Tags]    @tcid=WRTM-326ACN-85   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    At the LAN PC01 sniffer the DHCP packet.
    Typing the ipconifg/renew in windows command.
    LAN PC01 will send out the DHCP Request packet for the current IP Address.
    Verify the DUT will response the DHCP ACK packet. Check the LAN PC01 IP Address is the same by typing ipconfig/all in windows command.

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

At the LAN PC01 sniffer the DHCP packet.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo tcpdump -i ${DEVICES.lanhost.interface} port 67 or port 68 -e -n -c 10 > dhcp_pkg.log &
    
Typing the ipconifg/renew in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface} -r
    cli    lanhost    sudo dhclient ${DEVICES.lanhost.interface}
    
LAN PC01 will send out the DHCP Request packet for the current IP Address.
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
