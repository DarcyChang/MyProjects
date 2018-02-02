*** Settings ***

*** Variables ***

*** Keywords ***
Check DHCP Client Configuration
    [Arguments]   ${Device}    ${dhcpc_least_file}    ${dhcpc_network}    ${dhcpc_ip_mask}   ${dhcpc_dhcp_server}    ${dhcpc_lease}    ${dhcpc_dns_server} 
    [Documentation]    Check UPNP Device Should be Discovered By host
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    ${dhcpc_option_val}    cli    ${Device}    cat ${dhcpc_least_file}
    
    Should Contain    ${dhcpc_option_val}    fixed-address ${dhcpc_network}   msg=DHCP Client Contain correct ip address info
    Should Contain    ${dhcpc_option_val}    option subnet-mask ${dhcpc_ip_mask}
    Should Contain    ${dhcpc_option_val}    option routers ${dhcpc_dhcp_server}
    Should Contain    ${dhcpc_option_val}    option dhcp-lease-time ${dhcpc_lease}
    Should Contain    ${dhcpc_option_val}    option domain-name-servers ${dhcpc_dns_server}

Check UPNP Device Should be Discovered By host
    [Arguments]   ${Device}    ${Device_INT}    
    [Documentation]    Check UPNP Device Should be Discovered By host
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Run Keyword And Ignore Error    cli    ${Device}    ls
    cli    ${Device}    sudo upnpc -s -m ${Device_INT} > upnp.log
    ${val}=    cli    ${Device}    sudo cat upnp.log
    log    ${val}
    Should Contain    ${val}    ${g_dut_gw}
    Should Contain    ${val}    Found valid IGD
    
Check UPNP Device Should Not be Discovered By host
    [Arguments]   ${Device}    ${Device_INT}
    [Documentation]    Disable UPNP and lanhost should not discover this device By host
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Run Keyword And Ignore Error    cli    ${Device}    ls
    cli    ${Device}    sudo upnpc -s -m ${Device_INT} > upnp.log &
    sleep    10s
    ${val}=    cli    ${Device}    sudo cat upnp.log
    log    ${val}
    Should Not Contain    ${val}    ${g_dut_gw}
    
    
Config Host To Get DHCP IP
    [Arguments]   ${Device}    ${Device_INT}
    [Documentation]    execute dhclient command to release and renew ip
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    cli    ${Device}    sudo killall dhclient
    cli    ${Device}    sudo rm -rf /var/lib/dhcp/dhclient.leases
    cli    ${Device}    sudo ifconfig ${Device_INT} down
    cli    ${Device}    sudo ifconfig ${Device_INT} up
    cli    ${Device}    sudo dhclient ${Device_INT} -r
    cli    ${Device}    sudo dhclient ${Device_INT}
    sleep    5s
    cli    ${Device}    sudo dhclient ${Device_INT} -r
    cli    ${Device}    sudo dhclient ${Device_INT}
    cli    ${Device}    cat /var/lib/dhcp/dhclient.leases
    cli    ${Device}    sudo ifconfig ${Device_INT}

    sleep    3s
    ${dhcp_ip_address}=    Wait Until Keyword Succeeds    5x    5s    Get IP Value From Device SSH Connection    ${Device}    ${Device_INT}
    
    [Return]    ${dhcp_ip_address}

Get IP Value From Device SSH Connection
    [Arguments]   ${Device}    ${Device_INT}
    [Documentation]    To get wan ip address from dut ssh connection
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Run Keyword And Ignore Error    cli    ${Device}    ls
    
    cli    ${Device}    ifconfig ${Device_INT}
    ${val} =    cli    ${Device}    ifconfig ${Device_INT} | awk \'/inet addr/ {gsub(\"addr:\", \"\", $2); print $2}\'

    log    ${val}

    ${val} =   Get Line    ${val}    1
    log    ${val}
    Should Match Regexp    ${val}    ^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$
    
    [Return]    ${val}
    
Config Traffic IP to TGN Interface
    [Arguments]    ${tgn}    ${tgn_sudopw}    ${tgn_int}   ${tgn_ip}
    [Documentation]    Config Lanhost Traffic IP
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Log Many    ${tgn}    ${tgn_int}   ${tgn_ip}
    cli    ${tgn}    echo '${tgn_sudopw}' | sudo -S sudo ifconfig ${DEVICES.lanhost.interface} down
    cli    ${tgn}    echo '${tgn_sudopw}' | sudo -S sudo ifconfig ${DEVICES.lanhost.interface} ${tgn_ip}
    cli    ${tgn}    echo '${tgn_sudopw}' | sudo -S sudo ifconfig ${DEVICES.lanhost.interface} up
    cli    ${tgn}    echo '${tgn_sudopw}' | sudo -S sudo ifconfig ${DEVICES.lanhost.interface}
    cli    ${tgn}    echo '${tgn_sudopw}' | sudo -S sudo route -n
    sleep    3s
    
Is Linux Ping Successful
    [Arguments]    ${device}    ${gw_ip}     ${ping_count}=3
    [Documentation]    To check ping ${gw_ip} is successful
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c ${ping_count}
    log    ${result}
    Should contain    ${result}    bytes from

Is Linux Ping Fail
    [Arguments]    ${device}    ${gw_ip}    ${ping_count}=3
    [Documentation]    To check ping ${gw_ip} is fail
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c ${ping_count}    timeout=15    timeout_exception=0
    log    ${result}
    Should Contain    ${result}    100% packet loss

*** comment ***
2017-09-02     Gemtek_Thomas_Chen
Add upnp keyword

2017-09-02     Gemtek_Thomas_Chen
1. Add firmware upgrade keywords

2017-08-26     Gemtek_Thomas_Chen
1. Init the script