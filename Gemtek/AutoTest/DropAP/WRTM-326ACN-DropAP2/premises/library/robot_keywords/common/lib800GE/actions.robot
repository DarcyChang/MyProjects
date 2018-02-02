*** Settings ***
Resource          caferobot/cafebase.robot

*** Keywords ***
enable WAP mode for ONT
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${ont_trunk_conn}
    [Documentation]  log in to ONT and enable WAP for it
    log in to ONT    ${browser}    ${url}    ${username}    ${password}
    enable WAP    ${browser}    ${url}
    #now the device will reboot, wait it
    sleep    180
    wait_trunk_able_to_execute_command    ${ont_trunk_conn}
    ${ip_addr}    get_lan_gateway_from_serial_port    ${ont_trunk_conn}
    should contain    ${ip_addr}    192.168.1.
    # check whether WAP enable
    log in to ONT    ${browser}    http://${ip_addr}    ${username}    ${password}
    WAP should be enable    ${browser}    http://${ip_addr}
    [Return]    ${ip_addr}


enable WAP and IGMP mode for ONT
    [Arguments]    ${browser}    ${url}    ${username}    ${password}    ${ont_trunk_conn}
    [Documentation]  log in to ONT and enable WAP and IGMP for it
    ${ip_addr}    enable WAP mode for ONT    ${browser}    ${url}    ${username}    ${password}    ${ont_trunk_conn}
    log in to ONT	ff	http://${ip_addr}	support	 support
    enable WAP-IGMP	ff	http://${ip_addr}
    #now the device will reboot, wait it
    sleep	180
    wait_trunk_able_to_execute_command	 ${ont_trunk_conn}
    ${ip_addr}	get_lan_gateway_from_serial_port	${ont_trunk_conn}
    should contain   	 ${ip_addr}    	192.168.1.
    # check whether WAP-IGMP enable
    log in to ONT	ff	http://${ip_addr}	support	support
    WAP-IGMP should be enable	ff	 ${ip_addr}
    [Return]    ${ip_addr}