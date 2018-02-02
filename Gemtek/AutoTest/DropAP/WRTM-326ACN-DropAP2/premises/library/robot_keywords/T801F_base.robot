*** Settings ***
Resource    caferobot/cafebase.robot
Resource    premises/test_configs/Gfast_801f/param.robot

*** Variables ***
${cli_prompt}    ~ #
${meta_prompt}    metacli>
${tftp_server_ip}    192.168.1.99

*** Keywords ***
meta_cli_login
    [Arguments]    ${cpe_device}
    [Documentation]    Description: \ \ \ \ \ \ \ Login to 801f metacli from root account
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | cpe_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    meta_cli_login \ \ \ \ 801f
    cli    ${cpe_device}    ${g_input_enter}
    ${result}=    cli    ${cpe_device}    metacli    ${cli_prompt}
    log to console    ${result}

meta_cli_logout
    [Arguments]    ${cpe_device}
    [Documentation]    Description: \ \ \ \ \ \ \ Logout from 801f metacli of root account
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | cpe_device | the one setting in your yaml |
    ...
    ...    Example:
    ...    meta_cli_logout \ \ \ \ 801f
    ${result}=    cli    ${cpe_device}    ${g_input_ctrl_c}    ${cli_prompt}
    log to console    ${result}
    #${result}=    cli    ${cpe_device}    exit    login:
    #log to console    ${result}

T801F_login
    [Arguments]    ${device}    ${user}=${g_801f_cli_user}    ${pwd}=${g_801f_cli_pwd}
    [Documentation]    [Author:cgao] Description: Login to 801f by account and password
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | user | username for login | ${g_801f_cli_user} setting in global parameter file |
	...    | pwd | password for login | ${g_801f_cli_pwd} setting in global parameter file |
    ...
    ...    Example:
    ...    | T801F_login | 801f | | |
	...    | T801F_login | 801f | root | root |
    ${result}=    cli    ${device}    ${user}
    ${result}=    cli    ${device}    ${pwd}
    [Return]    ${result}

T801F_logout
    [Arguments]    ${device}
    [Documentation]    [Author:cgao] Description: Logout from 801f
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ | \ =default Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    Example:
    ...    | T801F_logout | 801f | | |
    ${result}=    cli    ${device}    ${g_801f_cli_exit}
    [Return]    ${result}

T801F_meta_cli_set
    [Arguments]    ${device}    ${metakey}    ${value}
    [Documentation]    [Author:cgao] Description: 801F metacli set operation
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml  |
	...    | metakey | command key for metacli  |
	...    | value | command value to set for metacli |
    ...
    ...    Example:
    ...    | T801F_meta_cli_set | 801f | wan0_ip_assignment | 0 |
	...    | T801F_meta_cli_set | 801f | wan0_dhcp_client_option60 | test |
    # enter metacli
    meta_cli_login    ${device}
    # set value of metakey
    cli    ${device}    set ${metakey} ${value}
    cli    ${device}    commit    ${meta_prompt}
    log to console    metacli: set ${metakey} to ${value}
    # exit metacli
    cli    ${device}    ${g_input_ctrl_c}
    [Return]

T801F_meta_cli_get
    [Arguments]    ${device}    ${metakey}
    [Documentation]    [Author:cgao] Description: 801F metacli get operation
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml  |
	...    | metakey | command key for metacli  |
	...
    ...   Return:
    ...   The result you get from metacli get command
    ...
    ...    Example:
    ...    | T801F_meta_cli_get | 801f | wan0_ip_assignment |
	...    | T801F_meta_cli_get | 801f | wan0_dhcp_client_option60 |
    # enter metacli
    meta_cli_login    ${device}
    # get value of metakey
    ${result}    cli    ${device}    get ${metakey}    ${meta_prompt}    #10
    log to console    metacli: get ${metakey} is ${result}
    # exit metacli
    cli    ${device}    ${g_input_ctrl_c}
    [Return]    ${result}

T801F_set_wan_ip_assignment
    [Arguments]    ${device}    ${ip_mode}
    [Documentation]    [Author:cgao] Description: change wan ip assignment mode
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
    ...    | ip_mode | wan ip assignment method: {static,dhcp,pppoe} |
    ...
    ...    Example:
    ...    | T801F_change_wan_ip_assignment | 801f | dhcp |

    ${cmdkey}    set variable    wan0_ip_assignment
    ${ip_mode_value}    Set Variable If
    ...    '${ip_mode}'=='static'    0
    ...    '${ip_mode}'=='dhcp'    1
    ...    '${ip_mode}'=='pppoe'    2
    log to console    wan ip assignment mode ${ip_mode} set value to ${ip_mode_value}

    T801F_meta_cli_set    ${device}    ${cmdkey}      ${ip_mode_value}
    ${result}    T801F_meta_cli_get    ${device}    ${cmdkey}
    Run Keyword And Ignore Error     Should Match Regexp    ${result}    ${cmdkey}=${ip_mode_value}
#    Sleep    30

T801F_check_interface_ip
    [Arguments]    ${device}    ${iface}    ${ip}    ${mask}=255.255.255.0
    [Documentation]    [Author:cgao] Description: Using ifconfig command to check interface ip and mask by interface name by Regexp
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | iface | interface name |
	...    | ip | interface ip |
    ...    | mask |  interface mask |
    ...
    ...    Example:
    ...    | T801F_check_interface_ip | 801f | pon0.85 | 10.245.85.1 | 255.255.255.0 |
	...    | T801F_check_interface_ip | 801f | eth0.2 | 192.168.1.1 | 255.255.255.0 |
    ${result}    cli    ${device}    ifconfig ${iface}    ${cli_prompt}
    Should Match Regexp    ${result}    (inet addr:${ip})+[\\s\\S]*(Mask:${mask})
    [Return]    ${result}

T801F_check_route
    [Arguments]    ${device}    ${dest}    ${gw}    ${mask}    ${iface}
    [Documentation]    [Author:cgao] Description: Using route command to check route info by Regexp in IP routing table
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
	...    | dest | Destination information in IP routing table |
	...    | gw | Gateway in IP routing table |
    ...    | mask | Genmask in IP routing table |
    ...    | iface | Interface name in IP routing table |
    ...
    ...    Example:
    ...    | T801F_check_route | 801f | 10.245.0.0 | \\* | 255.255.0.0 | pon0.85 |
	...    | T801F_check_route | 801f | default | 10.245.85.1 | 255.255.255.0 | pon0.85 |
    ${result}    cli    ${device}    route    ${cli_prompt}
    Should Match Regexp    ${result}    ${dest}.*${gw}.*${mask}.*${iface}
    [Return]    ${result}

T801F_check_memory
    [Arguments]    ${device}
    [Documentation]    [Author:cgao] Description: check 801f free memory and buddyinfo
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
    ...
    ...    Example:
    ...    | T801F_check_memory | 801f |

    cli    ${device}    ${g_input_enter}
    ${result}    cli    ${device}    free    ${cli_prompt}
    ${status}    ${info}    Run Keyword And Ignore Error     Should Match Regexp    ${result}    Mem:(\\s+\\d+){5}
    log to console    check free memory ${status}: ${info}
    Sleep    3

    cli    ${device}    ${g_input_enter}
    ${result}    cli    ${device}    cat /proc/meminfo    ${cli_prompt}
    ${status}    ${info}    Run Keyword And Ignore Error     Should Match Regexp    ${result}    MemFree:(\\s+\\d+\\s)?
    log to console    check meminfo ${status}: ${info}
    Sleep    3

    cli    ${device}    ${g_input_enter}
    ${result}    cli    ${device}    cat /proc/buddyinfo    ${cli_prompt}
    ${status}    ${info}    Run Keyword And Ignore Error     Should Match Regexp    ${result}    Normal(\\s+\\d+){11}
    log to console    check buddyinfo ${status}: ${info}
    Sleep    3

T801F_upgrade_from_lan
    [Arguments]    ${telnet_server}   ${sw_name}
    [Documentation]    [Author:wywang] Description: upgrade 801f from lan use tftp_update.sh + IP + sw_name
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |
    ...    | sw_name | sw name you want upgrade to |
    ...
    ...    Example:
    ...    | T801F_upgrade_from_lan | telnet_server(10.245.7.40) | Pre801F_1.1.8.0.oneimage

    ${my_cmd}=    catenate    ${g_801f_tftp_update}    ${tftp_server_ip}    ${sw_name}
    cli    ${telnet_server}    ${my_cmd}    foreign host    none        90
    sleep    20

TR69_acs_configure
    [Arguments]    ${801f_device}=${g_801f_device}
    [Documentation]    Author: Xiaoting Lai
    ...    801F-SR-2158 The 801F MUST limit TR-69 access to only the WAN interface.
    ...
    ...    801F-tr69_Management-18 The 801F MUST default to DHCPv4 address allocation of the management address
    ...
    ...    Global ID: 1146001
    META_CLI_login    ${g_801f_device}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_url ${g_acs_url}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_username ${g_acs_usr}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_password ${g_acs_pwd}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_request_username ${g_acs_req_usr}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_request_password ${g_acs_req_pwd}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    set cwmp_acs_inform_interval ${g_acs_interval}    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    commit    ${meta_prompt}
    log to console    ${result}
    ${result}=    cli    ${g_801f_device}    find_by_key cwmp_acs_url    ${meta_prompt}
    log to console    ${result}
    Should Match Regexp    ${result}    cwmp_acs_url=${g_acs_url}
    META_CLI_logout    ${g_801f_device}
    ${result}=    cli    ${g_801f_device}    exit    ogin:
    log to console    ${result}