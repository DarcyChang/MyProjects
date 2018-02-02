*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Hans_Sun

Suite Teardown    Run keywords    Restore Application Forwarding Original Settings
*** Variables ***
${vlan}    913
${priority}    1
${App_forwarding_name}    port_7777
${Forwarding_Port}    7777
${dummy_Forwarding_Port}    8888
${Port_forwarding_ip}    192.168.1.101
${LanHost_int}    eth1
${Traffic_count}    10

*** Test Cases ***
tc_Security_Applications_Forwarding_Rules
    [Documentation]   tc_Security_Applications_Forwarding_Rules
    ...    #Topology #LanHost.....CPE-----E5.....WanHost
    ...    1.Go to Advance-Security-Application Forwarding web page, and configure forwarding port
    ...    2.LanHost use tcpdump command line assigning port and waitting for reciving 10 packets
    ...    3.WanHost use hping command line assigning port and sending 10 packets
    ...    4.Duplicate step2 & step3 by using dummy forwaring port, and check sending packets is failed
    [Tags]    @TCID=STP_DD-TC-10508    @globalid=1506104    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Support Page and configure WAN Service
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    VLAN_config    tagged
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='vlan_config_vlan_id']    ${vlan}
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='vlan_config_priority']    ${priority}
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    version    ipv4
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    framing    IPoE
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Go to Status Page and get ipv4 wan ip by IPoE
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    ${dut_wan_ip} =   Wait Until Keyword Succeeds    5x    3s     Get Wan IP Value    web    xpath=//table[@id='gateway_tab']    9    2

    #Go to Advance-Security Page and configure Application Forwarding port
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'View')]
    Wait Until Keyword Succeeds    5x    10s  cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='application_name_field']    ${App_forwarding_name}
    input_text    web    xpath=//input[@id='port_start_field']    ${Forwarding_Port}
    input_text    web    xpath=//input[@id='port_end_field']    ${Forwarding_Port}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Go Back')]
    Wait Until Keyword Succeeds    5x    3s    click element   web    xpath=//input[@id='associate_rule_with_ip_radio']
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='ip_address_field']    ${Port_forwarding_ip}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #LanHost use tcpdump command line waitting for reciving 10 packets
    cli    LanHost    echo 'vagrant' | sudo -S tcpdump -n -i ${LanHost_int} tcp dst port ${Forwarding_Port} -c ${Traffic_count} -q > pfile &
    #Verify tcpdump is completed ,so sleep here.
    sleep    2s
    #WanHost use hping command line to send 10 packets
    Wait Until Keyword Succeeds    5x    3s    Start Send Traffic and Check Packet Status    ${dut_wan_ip}
    #LanHost check 10 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Check Recived Packet Status

    #LanHost use tcpdump command line waitting for reciving 10 packets
    cli    LanHost    echo 'vagrant' | sudo -S tcpdump -n -i ${LanHost_int} tcp dst port ${dummy_Forwarding_Port} -c ${Traffic_count} -q > pfile &
    #WanHost use hping command line to send 10 packets
    Wait Until Keyword Succeeds    5x    3s    Start Send Traffic and Check Dummy Forwarding Port Unuse    ${dut_wan_ip}


*** Keywords ***
Check Recived Packet Status
    [Arguments]
    [Documentation]    Check pfile if have recieved packets
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =   cli    LanHost    cat pfile
    log    ${result}
    Should Contain   ${result}    ${Forwarding_Port}

Start Send Traffic and Check Packet Status
    [Arguments]    ${Lanhost_wan_ip}
    [Documentation]    Check send packet is failed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =   cli    WanHost    echo 'vagrant' | sudo -S hping3 ${Lanhost_wan_ip} -S -p ${Forwarding_Port} -c ${Traffic_count} -i u500
    log    ${result}

Start Send Traffic and Check Dummy Forwarding Port Unuse
    [Arguments]    ${Lanhost_wan_ip}
    [Documentation]    Check send packet is failed
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =   cli    WanHost    echo 'vagrant' | sudo -S hping3 ${Lanhost_wan_ip} -S -p ${dummy_Forwarding_Port} -c ${Traffic_count} -i u500
    #log    ${result}
    #Should Contain   ${result}    100% packet loss

Get Wan IP Value
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is non empty, then return cell value.
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
    [Return]    ${cell1}

Restore Application Forwarding Original Settings
    [Arguments]
    [Documentation]    Restore application forwarding default settings
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
