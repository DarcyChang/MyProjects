*** Settings ***

Resource      ./base.robot
    
Force Tags    Force Tags    @FEATURE=DHCP_Server    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***

*** Test Cases ***
tc_DHCP_Server_On_OFF
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]    @tcid=WRTM-326ACN-79   @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login the DUT’s GUI to enable the DUT DHCP Server.
    LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    Login the DUT’s GUI to disable the DUT DHCP Server.
    Release the LAN PC01 IP Address by typing ipconfig/release in windows command. Renew the LAN PC01 IP Address by typing ipconfig/renew in windows command.
    LAN PC01 cannot get the IP Address form DUT DHCP Server.
    
*** Keywords ***
Login the DUT’s GUI to enable the DUT DHCP Server.
    [Arguments]
    [Documentation]    Test Step

    Config DEVICE DHCP Server Switch    web    on
    log    passlog
    
LAN PC01 can get the IP Address from the DUT DHCP Server. Check the LAN PC01 IP Address by typing ipconfig/all in windows command.
    [Arguments]
    [Documentation]    Test Step
    
    #${lanhost_dhcpc_ip}=    Get IP Value From Device SSH Connection    lanhost    ${DEVICES.lanhost.interface}
    ${lanhost_dhcpc_ip}=    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    
    log    ${lanhost_dhcpc_ip}
    
    Check IP and Hostname Exist in the DHCP Client Table    web    dhcp_table    ${lanhost_dhcpc_ip}    ${DEVICES.lanhost.hostname}

Login the DUT’s GUI to disable the DUT DHCP Server.
    [Documentation]    Test Step
    
    Config DEVICE DHCP Server Switch    web    off
    
Release the LAN PC01 IP Address by typing ipconfig/release in windows command. Renew the LAN PC01 IP Address by typing ipconfig/renew in windows command.
    [Documentation]    Test Step
    
    ${status}=    Run Keyword And Return Status    Config Host To Get DHCP IP    lanhost    ${DEVICES.lanhost.interface}
    
    log    ${status}
    Set Global Variable    ${dhcp_status}    ${status}
    
LAN PC01 cannot get the IP Address form DUT DHCP Server.
    [Documentation]    Test Step
    
    Should Not Be True    ${dhcp_status}    
    
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
