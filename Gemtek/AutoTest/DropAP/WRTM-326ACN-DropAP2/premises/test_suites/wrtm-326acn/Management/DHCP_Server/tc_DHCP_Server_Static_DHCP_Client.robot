*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${assigned_id}    0
${assigned_ip_1}    192.168.55.249
${assigned_ip_2}    192.168.55.240

*** Test Cases ***
tc_DHCP_Server_Static_DHCP_Client
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]    @tcid=WRTM-326ACN-91   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    Manually Assign IP Address with MAC Address for the LAN PC01
    Check the PC01 IP Address will be the assigned IP Address.
    Manually Assign 2nd IP Address with MAC Address for the LAN PC01
    Check the PC01 IP Address will be the 2nd assigned IP Address.
    
*** Keywords ***
Login the DUT’s GUI to enable the DUT DHCP Server.
    [Arguments]
    [Documentation]    Test Step
    
    Config DEVICE DHCP Server Switch    web    on
    Unconfig Static DHCP Client    web    ${assigned_id}
    cli    lanhost    sudo rm -rf /var/lib/dhcp/dhclient.leases
    
LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log    ${lanhost_dhcpc_ip}
    Check IP and Hostname Exist in the DHCP Client Table    web    dhcp_table    ${lanhost_dhcpc_ip}    ${DEVICES.lanhost.hostname}
    
Manually Assign IP Address with MAC Address for the LAN PC01
    [Arguments]
    [Documentation]    Test Step

    Config Static DHCP Client    web    ${assigned_id}    ${assigned_ip_1}    ${DEVICES.lanhost.interface_mac}

Check the PC01 IP Address will be the assigned IP Address.
    [Arguments]
    [Documentation]    Test Step
    
    ${val_static_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log many    ${val_static_dhcpc_ip}
    Should Match    ${val_static_dhcpc_ip}    ${assigned_ip_1}

Manually Assign 2nd IP Address with MAC Address for the LAN PC01
    [Arguments]
    [Documentation]    Test Step
    
    Config Static DHCP Client    web    ${assigned_id}    ${assigned_ip_2}    ${DEVICES.lanhost.interface_mac}

Check the PC01 IP Address will be the 2nd assigned IP Address.
    [Arguments]
    [Documentation]    Test Step
    
    ${val_static_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    log many    ${val_static_dhcpc_ip}
    Should Match    ${val_static_dhcpc_ip}    ${assigned_ip_2}
    
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
    Config DEVICE DHCP Server Switch    web    on
    cli    lanhost    sudo killall dhclient
    Restore Lanhost IP

Restore Lanhost IP
    [Arguments]
    [Documentation]    Restore Lanhost IP
    [Tags]        
    
    Config Traffic IP to TGN Interface    lanhost    ${DEVICES.lanhost.password}    ${DEVICES.lanhost.interface}    ${DEVICES.lanhost.traffic_ip}
    cli    lanhost    echo '${DEVICES.lanhost.password}' | sudo -S route del default gw ${g_dut_gw}
    
*** comment ***
2017-09-07     Gemtek_Thomas_Chen
Init the script
