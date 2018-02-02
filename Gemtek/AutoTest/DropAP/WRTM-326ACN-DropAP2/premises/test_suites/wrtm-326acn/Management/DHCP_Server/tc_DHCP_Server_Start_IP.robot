*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${dhcp_server_start_ip}    192.168.55.10



*** Test Cases ***
tc_DHCP_Server_Start_IP
    [Documentation]    User can specify start of address from LAN network segment.
    [Tags]    @tcid=WRTM-326ACN-83   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    Change the Start IP Address to 192.168.55.10.
    Renew PC01 IP Address by typing ipconfig/renew in windows command. Make sure the PC01 will get the IP Address 192.168.15.10.
    Change the Start IP Address to 192.168.55.1. The configuration cannot be saved and will pop-up a warning message.
    
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

Change the Start IP Address to 192.168.55.10.
    [Arguments]
    [Documentation]    Test Step
    
    ${config_status}=    Config DHCP Server IP Range    web    ${dhcp_server_start_ip}    ${dhcp_server_start_ip}
    log    ${config_status}
    Should Be True    ${config_status}
    
Renew PC01 IP Address by typing ipconfig/renew in windows command. Make sure the PC01 will get the IP Address 192.168.15.10.
    [Arguments]
    [Documentation]    Test Step
    
    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${lanhost_dhcpc_ip}
    Wait Until Keyword Succeeds    5x    3s    Check IP and Hostname Exist in the DHCP Client Table    web    dhcp_table    ${lanhost_dhcpc_ip}    ${DEVICES.lanhost.hostname}
    
Change the Start IP Address to 192.168.55.1. The configuration cannot be saved and will pop-up a warning message.
    [Arguments]
    [Documentation]    Test Step
    log    Start range should be the the gateway ip, should it should not be true here.
    ${config_status}=    Config DHCP Server IP Range    web    ${g_dut_gw}
    log    ${config_status}
    Should Not Be True    ${config_status}

    
    
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
