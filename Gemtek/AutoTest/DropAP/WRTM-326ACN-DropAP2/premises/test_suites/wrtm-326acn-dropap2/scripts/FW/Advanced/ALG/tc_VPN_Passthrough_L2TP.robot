*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=ALG    @AUTHOR=Jujung_Chang

Suite Setup    Run keywords    Common Setup
Suite teardown    Run keywords    Common Teardown

*** Variables ***
${ppp_username}    test
${ppp_password}    test
${L2TP_TYPE_FULL}    full
${L2TP_START_WHEN_BOOT}    False
${L2TP_FORCE_ENCRYPTION}    False

*** Test Cases ***
tc_VPN_Passthrough_L2TP
    [Documentation]    tc_VPN_Passthrough_L2TP
    [Tags]    @TCID=WRTM-326ACN-388    @DUT=WRTM-326ACN      @AUTHOR=Jujung_Chang
    [Timeout]

    Configure L2TP including server ip, username, password, Select "Full" mode and save the settings.
    Checking PPTP_L2TP Is Connected Or Not
    From GUI, check traffic from lan to wanhost

*** Keywords ***
Configure L2TP including server ip, username, password, Select "Full" mode and save the settings.
    [Arguments]
    [Documentation]    Test Step

    Config PPTP_L2TP    web    l2tp    ${g_dut_static_gateway}    ${ppp_username}    ${ppp_password}    ${L2TP_TYPE_FULL}    ${L2TP_START_WHEN_BOOT}    ${L2TP_FORCE_ENCRYPTION}

Checking PPTP_L2TP Is Connected Or Not
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    5x    5s    Check PPTP_L2TP Connected    web

From GUI, check traffic from lan to wanhost
    [Arguments]
    [Documentation]    Test Step

    #Config dropAP is DHCP mode.
    Login Web GUI
    Config DHCP Client

    #Checking dropAP can capture l2tp packets.
    Wait Until Keyword Succeeds    5x    3s    cli    dut1    killall tcpdump
    Wait Until Keyword Succeeds    5x    3s    cli    dut1    tcpdump -n -i ${DEVICES.dut1.wan_interface} | grep l2tp > pfile &

    #Checking ping is successfully.
    Login Secomweb GUI
    ${ping_result}=    Ping Host IP by GUI     web    ${DEVICES.wanhost.traffic_ip}
    Should Contain    ${ping_result}    0% packet loss

    Wait Until Keyword Succeeds    3x    1s    RePing Host IP by GUI    web

RePing Host IP by GUI
    [Arguments]    ${browser}
    [Documentation]
    cpe click    ${browser}    xpath=//*[@id="ping_tool"]/div/div/div[3]/button[2]
    sleep    10s
    ${ret} =   cli    dut1    cat pfile
    ${ret} =   cli    dut1    cat pfile
    Should Contain    ${ret}    l2tp

Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route add -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}
    Login Secomweb GUI


Login Secomweb GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]

    delete all cookies    web
    go_to_page    web    ${l2tp_server_gui_url}
    input_text    web    xpath=//*[@id="loginuser"]    ${g_dut_gui_user}
    input_text    web    xpath=//*[@id="loginpass"]    ${g_dut_gui_pwd}
    cpe click    web    xpath=//*[@id="login"]/div[1]/div/div/div[2]/form/a
    sleep   3s

Common Teardown
    [Arguments]
    [Documentation]
    [Tags]
    cli    wanhost    echo ${DEVICES.wanhost.password} | sudo -S route del -net ${DEVICES.wanhost.route}/24 gw ${DEVICES.wanhost.default_gw}
    Wait Until Keyword Succeeds    5x    3s    cli    dut1    killall -9 tcpdump

*** comment ***
2018-01-02     Gemtek_Jujung_Chang
Init the script
