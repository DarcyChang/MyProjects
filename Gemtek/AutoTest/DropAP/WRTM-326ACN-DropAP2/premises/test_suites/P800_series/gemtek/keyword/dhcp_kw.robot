*** Settings ***

*** Variables ***
${cli_prompt}    ~ #
${meta_prompt}    metacli>

${default_mask}    0.0.0.0
${dhcps_mac}      00:00:00:94:00:01
${dhcps_ip}       10.0.80.10
${dhcps_pool_ip}    10.0.80.11
${dhcps_gw}       10.0.80.1
${dhcps_subnet}    10.0.80.0
${dhcps_subnet_length}    24
${dhcps_subnet_mask}    255.255.255.0

${lease_time}    60
${primary_dns}      192.168.33.10
${secondary_dns}    172.23.41.10

${dnsmasq}    /etc/init.d/dnsmasq.sh

*** Keywords ***
T801F_wan_dhcp_operate
    [Arguments]    ${device}    ${operate}
    [Documentation]    [Author:cgao] Description: start or stop wan dhcp session
    # start/stop wan dhcp client process, ${operate} should be start or stop
    ${result}    cli    ${device}    /etc/init.d/wan.sh ${operate} 0    ${cli_prompt}    30
    cli    ${device}    ${g_input_enter}
    [Return]    ${result}

T801F_dhcp_restart
    [Arguments]    ${device}
    [Documentation]    [Author:rshang]
    ${result}    cli    ${device}    /etc/init.d/udhcpc.sh restart 0   ${cli_prompt}    30
    Sleep    2s
    cli    ${device}    ${g_input_enter}
    [Return]    ${result}

T801F_set_dhcp_option
    [Arguments]    ${device}    ${opt_id}    ${opt_value}
    [Documentation]    [Author:cgao] Description: set 801f dhcp option value
    # set dhcp option and check value
    ${cmdkey}    set variable    wan0_dhcp_client_option${opt_id}
    ${result}    T801F_meta_cli_set    ${device}    ${cmdkey}    ${opt_value}
    ${result}    T801F_meta_cli_get    ${device}    ${cmdkey}
    Run Keyword If   '${opt_value}'=='""'    Should Match Regexp    ${result}    ${cmdkey}=
    ...    ELSE    Should Match Regexp    ${result}    ${cmdkey}=${opt_value}
    [Return]    ${result}

setup_dhcp_server
    [Arguments]    ${device}    ${vlan}    ${option_item}    ${tmp}=default
    [Documentation]    [Author:cgao] Description: setup dhcp server on traffic generater
    # setup dhcp server
    Tg Create Dhcp Server On Port    ${device}    dhcps    ${g_tg_uport}    encapsulation=ETHERNET_II_VLAN    vlan_id=${vlan}    vlan_user_priority=0
    ...    local_mac=${dhcps_mac}    ip_address=${dhcps_ip}    ipaddress_pool=${dhcps_pool_ip}    &{option_item}
    TG Control DHCP Server    ${device}    dhcps    connect
    Tg Save Config Into File    ${device}    /tmp/stptest_save/stc_config_${tmp}.xml

teardown_dhcp_server
    [Arguments]    ${device}
    [Documentation]    [Author:rshang]
    Tg Control Dhcp Server    ${device}    dhcps    reset

start_wan_dhcp_and_capture_packet
    [Arguments]    ${device}    ${tg}    ${port}=${g_tg_uport}    ${ip}=${dhcps_pool_ip}    ${mask}=${dhcps_subnet_mask}
    [Documentation]    [Author:cgao] Description: start 801f wan dhcp session and capture packet on traffic generater dhcp server port
    # capture packet on tg port
    Tg Packet Control    ${tg}    ${port}    start
    #start wan dhcp
    T801F_wan_dhcp_operate    ${device}    start
    # check wan ip and mask
    Wait Until Keyword Succeeds    10x    10s    T801F_check_interface_ip    ${device}    ${g_801f_wan_port}    ${ip}    ${mask}
    sleep    10s
    Tg Packet Control    ${tg}    ${port}    stop
    sleep    4s

dhcp_pkt_analyze
    [Arguments]    ${tg_device}    ${filename}    ${pkt_filter}    ${option}=None    ${value}=None
    [Documentation]    [Author:cgao] Description: store captured dhcp packet and verify option value, if packet count is 0, return directly
    ${save_file}    set variable    ${g_tg_store_file_path}/${filename}.pcap
    Tg Store Captured Packets    ${tg_device}    ${g_tg_uport}    ${save_file}
    sleep    10s
    Wsk Load File    ${save_file}    ${pkt_filter}
    # if packet count==0, or no option to verify, returen packet count
    ${cnt}    Wsk Get Totoal Packet Count
    Run Keyword If    ${cnt}==0    Return From Keyword    packet count is 0
    Run Keyword If    '${option}'=='None'    Return From Keyword    packet count is ${cnt}
    # verify dhcp option value
    ${res}    Wsk Verify Bootp Option    ${option}    ${value}
    should be true    ${res}
    [Return]    option verify result is ${res}

case_setup_dhcp
    [Arguments]  ${801f_device}
    [Documentation]    [Author:rshang]
    T801F_wan_dhcp_operate    ${801f_device}    stop
    T801F_wan_dhcp_operate    ${801f_device}    start
    T801F_dhcp_restart    ${801f_device}

case_teardown_dhcp
    [Arguments]  ${801f_device}
     [Documentation]    [Author:rshang]
    T801F_wan_dhcp_operate    ${801f_device}    stop

Get 801F IP Address
    [Documentation]  [Author:rshang] get 801f ip address
    ...  inet addr:192.85.1.4  Bcast:192.85.1.255  Mask:255.255.255.0
    [Arguments]    ${device}    ${interface}=pon0.85
    ${ret} =    Session Command    ${device}    ifconfig ${interface}

    ${ip} =    Get Regexp Matches    ${ret}    inet addr\\s*:\\s*(${g_ip_format})    1
    ${len} =    Get Length    ${ip}
    ${ip} =    Run Keyword If  ${len}    Get From List    ${ip}    0
    ...                        ELSE      Return From Keyword    ${SPACE}
    [Return]    ${ip}

Get 801F DNS Server List
    [Documentation]  [Author:rshang] get 801f DNS server list
    ...  ~ # cat /etc/resolv.conf
    ...  nameserver 127.0.0.1
    ...  search calix.local
    ...  nameserver 192.168.33.10
    ...  nameserver 172.23.41.11
    [Arguments]    ${device}
    ${ret} =    Session Command    ${device}    cat /etc/resolv.conf

    ${dns} =    Get Regexp Matches    ${ret}    nameserver\\s+(${g_ip_format})    1
    [Return]    ${dns}

Check 801F Get Valid IP Address
    [Arguments]  ${device}
    [Documentation]    [Author:rshang]
    ${ip} =    Get 801F IP Address    ${device}    ${g_801f_wan_port}
    Should Match Regexp    ${ip}    ${g_ip_format}

Check 801F Get Valid DNS Server List
    [Arguments]  ${device}
    [Documentation]    [Author:rshang]
    ${dns} =    Get 801F DNS Server List    ${device}
    List Should Contain Value    ${dns}    ${primary_dns}
    List Should Contain Value    ${dns}    ${secondary_dns}

801F Nslookup Website
    [Arguments]  ${device}    ${website}
    [Documentation]    [Author:rshang]
    ${ret} =    Cli    ${device}    nslookup ${website}    ${cli_prompt}    30
    [Return]  ${ret}

Check 801F DNS Queries Forwarded Count Should Be Zero
    [Arguments]  ${device}
    [Documentation]    [Author:rshang]
    ${content} =    801F Get DNS Queries Counter  ${device}
    ${count} =    801F Get DNS Queries Forwarded Count    ${device}
    Should Be True    ${count} == 0

801F Reset DNS Queries Counter
    [Arguments]  ${device}
    [Documentation]    [Author:rshang]
    Cli    ${device}    ${dnsmasq} restart    ${cli_prompt}    30
    Sleep    10s
    Cli    ${device}    ${g_input_enter}

801F Get DNS Queries Counter
    [Arguments]  ${device}
    [Documentation]    [Author:rshang]
    ${ret} =    Set Variable    ${EMPTY}
    :For    ${_}    IN RANGE    3
    \    ${ret} =    Cli    ${device}    ${dnsmasq} counter   counter ok    30
    \    ${passed} =    Run Keyword And Return Status    Should Not Contain    ${ret}    not found
    \    Return From Keyword If    ${passed}    ${ret}
    [Return]  ${ret}

801F Get DNS Queries Count By Regexp
    [Arguments]  ${content}    ${pattern}
    ${count} =    Get Regexp Matches    ${content}    ${pattern}    1
    ${len} =    Get Length    ${count}
    ${count} =    Run Keyword If  ${len}    Get From List    ${count}    0
    ...                           ELSE      Return From Keyword    0
    ${count} =    Evaluate    int(${count})
    [Return]  ${count}

801F Get DNS Queries Forwarded Count
    [Arguments]  ${content}
    [Documentation]    [Author:rshang]
    ${count} =    801F Get DNS Queries Count By Regexp    ${content}    queries forwarded\\s+(\\d+)
    [Return]  ${count}

801F Get DNS Queries Answered Locally Count
    [Arguments]  ${content}
    [Documentation]    [Author:rshang]
    ${count} =    801F Get DNS Queries Count By Regexp    ${content}    queries answered locally\\s+(\\d+)
    [Return]  ${count}

801F Get DNS Queries Retried Count
    [Arguments]  ${content}
    [Documentation]    [Author:rshang]
    ${count} =    801F Get DNS Queries Count By Regexp    ${content}    queries answered locally\\s+\\d+,\\s+retried\\s+(\\d+)
    [Return]  ${count}

Get 801F SW Version
    [Arguments]    ${device}
    [Documentation]    [Author:rshang]
    ${ret} =    Session Command    ${device}    cat version
    ${ver} =    Get Regexp Matches    ${ret}    version=(\\d\\.\\d\\.\\d\\.\\d+)    1
    ${len} =    Get Length    ${ver}
    ${ver} =    Run Keyword If    ${len}    Get From List    ${ver}    0
    ...    ELSE    Return From Keyword    ${SPACE}
    [Return]    ${ver}

change_dwl_file_name
    [Arguments]    ${device}    ${image_name}
    [Documentation]    [Author:rshang]
    ${model}    Get 801F Model    ${801f_device}
    ${str} =    Evaluate    str("sudo sed -r '/.*bootfile-name.*/s/.*/option bootfile-name \\"${image_name}\\";/' /etc/dhcp/dhcpd.conf > /etc/dhcp/tmpfile")
    cli    ${device}    ${str}
    ${str} =    Evaluate    str("sudo mv /etc/dhcp/tmpfile /etc/dhcp/dhcpd.conf")
    cli    ${device}    ${str}

Get 801F Model
    [Arguments]    ${device}
    [Documentation]    [Author:rshang]
    ${ret} =    Session Command    ${device}    cat version|grep model    ${cli_prompt}
    ${model} =    Get Regexp Matches    ${ret}    model=(.*)\\r    1
    ${len} =    Get Length    ${model}
    ${model} =    Run Keyword If    ${len}    Get From List    ${model}    0
    ...    ELSE    Return From Keyword    ${SPACE}
    [Return]    ${model}

change_dhcp_file_name
    [Arguments]    ${device}    ${modified_dhcp_file_name}
    [Documentation]    [Author:lbao] Description: Change DHCP file. ${modified_dhcp_file_name} is the new dhcp file that contains modified dhcp option value.
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | modified_dhcp_file_name | dhcp file name that contains modified dhcp option value.|

    ${str1} =    Evaluate    str("sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/tmpfile")
    Cli    ${device}    ${str1}
    ${str2} =    Evaluate    str("sudo mv ${modified_dhcp_file_name} /etc/dhcp/dhcpd.conf")
    Cli    ${device}    ${str2}

dhcp_file_name_back
    [Arguments]    ${device}    ${modified_dhcp_file_name}
    [Documentation]    [Author:lbao] Description: Put DHCP file back, which contains default dhcp option value. ${modified_dhcp_file_name} is the new dhcp file that contains modified dhcp option value.
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | device | device name setting in your yaml |  |
	...    | modified_dhcp_file_name | dhcp file name that contains modified dhcp option value.|

    ${str1} =    Evaluate    str("sudo mv /etc/dhcp/dhcpd.conf ${modified_dhcp_file_name}")
    Cli    ${device}    ${str1}
    ${str2} =    Evaluate    str("sudo mv /etc/dhcp/tmpfile /etc/dhcp/dhcpd.conf")
    Cli    ${device}    ${str2}

Get 801F device MAC
    [Arguments]    ${device}
    [Documentation]  [Author:lbao] Description: get 801f MAC address.
    ...               ethaddr=EC:4F:82:7E:72:11

    ${str} =    Evaluate    str('fw_printenv ethaddr')
    ${res} =    Cli    ${device}    ${str}    ~
    ${HWaddr} =    Get Regexp Matches    ${res}    (${g_HWaddr_format})    1
    log to console    ${HWaddr}
    ${len} =    Get Length    ${HWaddr}
    ${HWaddr} =    Run Keyword If  ${len}    Get From List    ${HWaddr}    0
    ...                        ELSE    Set Variable    false_default_str
    log to console    ${HWaddr}
    [Return]    ${HWaddr}