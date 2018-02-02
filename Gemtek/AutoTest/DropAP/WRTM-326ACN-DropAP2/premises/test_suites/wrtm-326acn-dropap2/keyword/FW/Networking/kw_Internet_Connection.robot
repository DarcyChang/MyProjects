*** Settings ***
Resource    base.robot

*** Variables ***
${Select_Protocal} =    xpath=//*[@id="cbid.network.wan.proto"]
${Button_Save} =    xpath=//*[@id="maincontent"]/div/form/div[3]/input[1]
${Input_Static_IP}    xpath=//*[@id="cbid.network.wan.ipaddr"]
${Input_Subnet_Mask}    xpath=//*[@id="cbid.network.wan.netmask"]
${Input_Static_Gateway}    xpath=//*[@id="cbid.network.wan.gateway"]
${Input_Static_DNS1}    xpath=//*[@id="cbid.network.wan.dns.1"]
${Input_PPPoE_Username}    xpath=//*[@id="cbid.network.wan.username"]
${Input_PPPoE_Password}    xpath=//*[@id="cbid.network.wan.password"]
${InvalidIPHTMLMSG} =      css=input[class="cbi-input-text cbi-input-invalid"]
${AddDNSButton}    xpath=//*[@id="cbi-network-wan-dns"]/div/div/img[1]
${TheSecondDNSInputText}    xpath=//*[@id="cbid.network.wan.dns.2"]

*** Keywords ***
Config DHCP Client
    [Arguments]
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking  Internet Connection
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_value    web    ${Select_Protocal}    dhcp
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Config Static Client
    [Arguments]    ${dns1}=${g_dut_static_dns1}
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking  Internet Connection
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_value    web    ${Select_Protocal}    static
    Input Text    web    ${Input_Static_IP}    ${g_dut_static_ipaddr}
    Input Text    web    ${Input_Subnet_Mask}    ${g_dut_static_netmask}
    Input Text    web    ${Input_Static_Gateway}    ${g_dut_static_gateway}
    Input Text    web    ${Input_Static_DNS1}    ${dns1}
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Config PPPoE Client
    [Arguments]    ${username}    ${password}
    [Documentation]
    [Tags]
    Wait Until Keyword Succeeds    3x    2s    click links    web    Networking  Internet Connection
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_value    web    ${Select_Protocal}    pppoe
    Input Text    web    ${Input_PPPoE_Username}    ${username}
    Input Text    web    ${Input_PPPoE_Password}    ${password}
    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely
    ${r1}   Get Length    ${username}
    ${r2}   Get Length    ${password}
    run keyword if  ${r1} == 0 or ${r2} == 0    page should contain text    web    The "Username" should not be empty!
    run keyword if  ${r1} > 64 or ${r2} > 64   page should contain element    web    ${InvalidIPHTMLMSG}

Adding DNS Candidate At GUI
    [Arguments]    ${NewDNS}
    [Documentation]  Adding DNS Candidate
    [Tags]
    cpe click    web    ${AddDNSButton}
    ${r} =  run keyword and return status    Wait Until Element Is Visible    web    ${TheSecondDNSInputText}    timeout=5s
    run keyword if    '${r}' == 'False'    Wait Until Keyword Succeeds    5x    1s    Retry Add DNS Candidates Button
    input text    web    ${TheSecondDNSInputText}    ${NewDNS}
    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Retry Add DNS Candidates Button
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cpe click    web    ${AddDNSButton}
    Wait Until Element Is Visible    web    ${TheSecondDNSInputText}    timeout=5s
