*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun

*** Variables ***
${vlan}    913
${priority}    1
${Custom_Security_Key}    1234567890
${g_844_wifi_client_user}    vagrant
${g_844_wifi_client_pwd}    vagrant
#${g_844_wifi_client_int}    ra0
${g_844_wifi_client_ip1}    192.168.1.122
${g_844_wifi_client_ip2}    192.168.9.122
${g_844_wifi_client_ip3}    192.168.11.122
${dut_wifi_ip_start3}    192.168.11.2
${dut_wifi_ip_end3}    192.168.11.254
${g_844_wifi_client_ip4}    192.168.13.122
${dut_wifi_ip_start4}    192.168.13.2
${dut_wifi_ip_end4}    192.168.13.254
${dut_gw1}    192.168.1.1
${dut_gw2}    192.168.9.1
${dut_gw3}    192.168.11.1
${dut_gw4}    192.168.13.1
${dut_ip_mask}    255.255.255.0
${WanHost_ip}    1.1.1.189
${WanHost_int}    eth2
${Traffic_port}    8888
${Traffic_count}    20
${Wireless_page}    http://${dut_gw1}/html/wireless/2dot4ghz/wireless_radiosetup.html
${Status_wireless_page}    http://${dut_gw1}/html/status/status_wirelessstatus.html

*** Test Cases ***
tc_GUI_STATUS_WIRELESS_Checking_Pck_SentReceived
    [Documentation]   tc_GUI_STATUS_WIRELESS_Checking_Pck_SentReceived
    ...    #Topology #Wifi_client.....CPE-----E5.....WanHost
    ...    1 Go to Wan service page configure ipv4 IPoE settings
    ...    2.Go to 2.4G Wi-Fi configure SSID name & Security Key & Network Domain
    ...    3.Use wifi_client to get IP from ONT via wireless with your setting.
    ...    4.WanHost use tcpdump command line assigning port and waitting for reciving 10 packets
    ...    5.wifi_client use hping command line assigning port and sending 10 packets
    ...    6.Duplicate step2~ 5step by configuring SSID name & Security Key & Network Domain
    [Tags]    @TCID=STP_DD-TC-10892    @globalid=1526062    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
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

    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    #Enable WiFi 2.4 GHz
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    wireless_onoff    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    radio_button_should_be_set_to    web    wireless_onoff    1

    #Change WiFi 2.4G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    input_text    web    xpath=//input[@id='id_ssid_name']    ${g_844fb_2.4g_ssid_name}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Use Custom Wi-Fi Password
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click element   web    xpath=//input[@id='lshxq02']
    input_text    web    xpath=//input[@id='pskKeyInput']    ${Custom_Security_Key}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Linux Wifi Client to Connect to DUT by using Fisrt SSID & 192.168.1.1 network domain
    Login Linux Wifi Client to Connect to DUT in Different 2.4G SSID    ${g_844fb_2.4g_ssid_name}    ${g_844_wifi_client_ip1}    ${dut_gw1}
    #Use Wifi Client send traffic to WanHost
    Wait Until Keyword Succeeds    5x    3s    Send Traffic from Linux Wifi Client to WanHost    ${g_844fb_2.4g_ssid_name}


    #Change WiFi 2.4G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    1
    ${Second_SSID} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_label    web    id=id_ssid
    log    ${Second_SSID}
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Change WiFi Security key type
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    1
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=security_type    psk+psk2
    input_text    web    xpath=//input[@id='pskKeyInput']    ${Custom_Security_Key}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Linux Wifi Client to Connect to DUT by using Second SSID & 192.168.9.1 network domain
    Login Linux Wifi Client to Connect to DUT in Different 2.4G SSID    ${Second_SSID}    ${g_844_wifi_client_ip2}    ${dut_gw2}
    #Use Wifi Client send traffic to WanHost
    Wait Until Keyword Succeeds    5x    3s    Send Traffic from Linux Wifi Client to WanHost    ${Second_SSID}


    #Change WiFi 2.4G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    2
    ${Third_SSID} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_label    web    id=id_ssid
    log    ${Third_SSID}
    #Change WiFi network domain
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    select_checkbox    web    xpath=//input[@id='interIsolateObj']
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='gatewayObj']    ${dut_gw3}
    input_text    web    xpath=//input[@id='ipAddressStartObj']    ${dut_wifi_ip_start3}
    input_text    web    xpath=//input[@id='ipAddressEndObj']    ${dut_wifi_ip_end3}
    input_text    web    xpath=//input[@id='ipAddressMaskObj']    ${dut_ip_mask}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Change WiFi Security key type
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    2
    input_text    web    xpath=//input[@id='pskKeyInput']    ${Custom_Security_Key}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Linux Wifi Client to Connect to DUT by using Third SSID & 192.168.11.1 network domain
    Login Linux Wifi Client to Connect to DUT in Different 2.4G SSID    ${Third_SSID}    ${g_844_wifi_client_ip3}    ${dut_gw3}
    #Use Wifi Client send traffic to WanHost
    Wait Until Keyword Succeeds    5x    3s    Send Traffic from Linux Wifi Client to WanHost    ${Third_SSID}


    #Change WiFi 2.4G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    3
    ${Fourth_SSID} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_label    web    id=id_ssid
    log    ${Fourth_SSID}
    #Change WiFi network domain
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    select radio button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    select_checkbox    web    xpath=//input[@id='interIsolateObj']
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='gatewayObj']    ${dut_gw4}
    input_text    web    xpath=//input[@id='ipAddressStartObj']    ${dut_wifi_ip_start4}
    input_text    web    xpath=//input[@id='ipAddressEndObj']    ${dut_wifi_ip_end4}
    input_text    web    xpath=//input[@id='ipAddressMaskObj']    ${dut_ip_mask}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Change WiFi Security key type
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    2
    input_text    web    xpath=//input[@id='pskKeyInput']    ${Custom_Security_Key}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Linux Wifi Client to Connect to DUT by using Fourth SSID & 192.168.13.1 network domain
    Login Linux Wifi Client to Connect to DUT in Different 2.4G SSID    ${Fourth_SSID}    ${g_844_wifi_client_ip4}    ${dut_gw4}
    #Use Wifi Client send traffic to WanHost
    Wait Until Keyword Succeeds    5x    3s    Send Traffic from Linux Wifi Client to WanHost    ${Fourth_SSID}


*** Keywords ***
Login Linux wifi client to connect to DUT in different 2.4G SSID
    [Arguments]    ${SSID}    ${wifi_client_ip}    ${dut_gw}
    [Documentation]    Linux wifi client to connect to DUT
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    #Wait for push Apply button is completed, so sleep at here.
    sleep    5s
    cli    wifi_client    whoami
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    wpa_passphrase ${SSID} ${Custom_Security_Key} > wpa.conf
    cli    wifi_client    echo \'${g_844_wifi_client_pwd}\' | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    wifi_client    echo \'${g_844_wifi_client_pwd}\' | sudo -S ifconfig ${g_844_wifi_client_int} ${wifi_client_ip}

    ${result} =    Wait Until Keyword Succeeds    10x    10s    Is WIFI Interfafe Up    wifi_client    ${SSID}
    wait until keyword succeeds    5x    10s    cli    wifi_client    ping ${dut_gw} -c 3
    cli    wifi_client    echo 'vagrant' | sudo -S route add default gw ${dut_gw} ${g_844_wifi_client_int}
    cli    wifi_client    ip route

Is WIFI Interfafe Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Send Traffic from Linux Wifi Client to WanHost
    [Arguments]    ${SSID}
    [Documentation]    Send traffic from LAN to WAN
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    go_to_page    web    ${g_844fb_gui_url}/html/status/status_wirelessstatus.html
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_label    web    id=id_ssid    ${SSID}
    ${Before_Packets_Sent} =   Wait Until Keyword Succeeds    5x    2s     Get Wireless Packets Sent    web    xpath=//table[@id='gv_statusTabObjID']    16    2
    log    ${Before_Packets_Sent}

    #WanHost use tcpdump command line waitting for reciving 10 packets
    cli    WanHost    echo 'vagrant' | sudo -S sudo killall tcpdump
    cli    WanHost    echo 'vagrant' | sudo -S tcpdump -n -i ${WanHost_int} tcp dst port ${Traffic_port} -c ${Traffic_count} -q > pfile &
    #Wifi_client use hping command line to send 10 packets
    Wait Until Keyword Succeeds    5x    5s    Start Send Traffic and Check Packet Status
    #Wanhost check 10 packets have recived
    Wait Until Keyword Succeeds    5x    5s    Check Recived Packet Status

    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${Status_wireless_page}
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_label    web    id=id_ssid    ${SSID}
    ${After_Packets_Sent} =   Wait Until Keyword Succeeds    5x    2s     Get Wireless Packets Sent    web    xpath=//table[@id='gv_statusTabObjID']    16    2
    log    ${After_Packets_Sent}

    Should Be True    ${After_Packets_Sent}-${Before_Packets_Sent}>20
    Should Not Be True    ${After_Packets_Sent}-${Before_Packets_Sent}>40
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${Wireless_page}

Start Send Traffic and Check Packet Status
    [Arguments]
    [Documentation]    Check send packet is succeess
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =   cli    wifi_client    echo 'vagrant' | sudo -S hping3 ${WanHost_ip} -S -p ${Traffic_port} -c ${Traffic_count} -i u500 -I ${g_844_wifi_client_int}
    log    ${result}
    Should Not Contain   ${result}    100% packet loss

Check Recived Packet Status
    [Arguments]
    [Documentation]    Check recived packet is succeess
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    ${result} =   cli    WanHost    cat pfile
    log    ${result}
    Should Not Be Empty    ${result}

Get Wireless Packets Sent
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is non empty, then return cell value.
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
    [Return]    ${cell1}