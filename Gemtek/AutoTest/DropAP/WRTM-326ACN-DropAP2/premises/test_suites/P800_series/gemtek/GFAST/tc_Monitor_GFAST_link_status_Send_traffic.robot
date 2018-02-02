*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=GFAST    @AUTHOR=Gemtek_Hans_Sun    stable

Suite Setup    Run keywords    LanHost Route Add Default Gateway
Suite Teardown    Run keywords    LanHost Route Delete Default Gateway
*** Variables ***
${vlan}    913
${priority}    1

*** Test Cases ***
tc_Monitor_GFAST_link_status_Send_traffic
    [Documentation]   tc_Monitor_GFAST_link_status_Send_traffic
    ...    1.Check web gui total-original Tx Packets
    ...    2.WanHost use tcpdump command line waitting for reciving 50 packets
    ...    3.LanHost use hping command line to send 50 packets
    ...    4.After Lan side host sends traffic to Wan side host, Check web gui total Tx Packets again
    [Tags]   @TCID=STP_DD-TC-11688    @globalid=1662612    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]

    #Check web gui GFAST status
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

    #Check web gui total-original Tx Packets from GFAST status
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    click links    web    G.fast
    ${Tx_Packets1} =   Wait Until Keyword Succeeds    5x    2s     Get Tx Packets Value    web    xpath=//table[@id='p0']    11    2
    log    ${Tx_Packets1}
    ${Tx_Packets2} =   Wait Until Keyword Succeeds    5x    2s     Get Tx Packets Value    web    xpath=//table[@id='p1']    11    2
    log    ${Tx_Packets2}

    #WanHost use tcpdump command line waitting for reciving 50 packets
    cli    WanHost    echo 'vagrant' | sudo -S tcpdump -n -i eth2 tcp dst port 8888 -c 50 -q > pfile &
    #Verify tcpdump is completed, so we sleep here.
    sleep    2s
    #LanHost use hping command line to send 50 packets
    cli    LanHost    echo 'vagrant' | sudo -S hping3 1.1.1.189 -S -p 8888 -c 50 -i u100 -I eth1

    #Wanhost check 50 packets have recived
    Wait Until Keyword Succeeds    5x    3s    Check Recived Packet Status

    #After Lan side host sends traffic to Wan side host, Check web gui GFAST status again
    Wait Until Keyword Succeeds    5x    3s    click links    web    G.fast
    ${After_Tx_Packets1} =   Wait Until Keyword Succeeds    5x    2s     Get Tx Packets Value    web    xpath=//table[@id='p0']    11    2
    log    ${After_Tx_Packets1}
    ${After_Tx_Packets2} =   Wait Until Keyword Succeeds    5x    2s     Get Tx Packets Value    web    xpath=//table[@id='p1']    11    2
    log    ${After_Tx_Packets2}
    Should Be True    ${After_Tx_Packets1}-${Tx_Packets1}+${After_Tx_Packets2}-${Tx_Packets2}>49

*** Keywords ***
LanHost Route Add Default Gateway
    [Arguments]
    [Documentation]    LanHost route add default gateway 192.168.1.1
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    cli    LanHost    echo 'vagrant' | sudo -S sudo route add default gw 192.168.1.1

Check Recived Packet Status
    [Arguments]
    [Documentation]    Go to cli mode
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =   cli    WanHost    cat pfile
    log    ${result}
    Should Not Be Empty    ${result}

Get Tx Packets Value
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is non empty, then return cell value.
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
    [Return]    ${cell1}

LanHost Route Delete Default Gateway
    [Arguments]
    [Documentation]    LanHost route add default gateway 192.168.1.1
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    LanHost    echo 'vagrant' | sudo -S sudo route delete default gw 192.168.1.1
