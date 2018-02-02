*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Jujung_Chang    norun

*** Variables ***
${wpa_supplicant_file}    /etc/wpa_supplicant/wpa_supplicant.conf
${g_ssid_name}     CXNK-thomas-2.4g
${g_5g_ssid_name}     CXNK-thomas-5g
${g_844_wifi_client_user}    vagrant
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_int}    wlan0
${g_844_wifi_client_ip}    192.168.1.155
${dut_gw}    192.168.1.1
*** Test Cases ***
tc_wps_pbc
    [Documentation]    tc_wps_pbc
    ...   1. login to ubuntu to init wpa_supplicant
    ...   2. In DUT, click WPS connect  id=connect_btn
    ...   3. In ubunutu, execute wps_pbc command to connect to dut
    [Tags]    @DUT=844FB  @DUT=844F

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    #Enable WiFi 2.4 GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    select radio button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wireless_onoff    1

    #Change WiFi 2.4G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    input_text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Go to Status/Wireless page to see if changed ssid is present
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =     get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_ssid_name}



    #Login Linux wifi client to connect to DUT 2.4 ssid
    cli    wifi_client    whoami
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo 'vagrant' | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -C /var/run/wpa_supplicant/ -c ~/wpa.conf -B
    cli    wifi_client    echo 'vagrant' | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    ${result_mac} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Mac From SSID Using WPA Supplicant    wifi_client    ${g_ssid_name}
    log    ${result}
    cli    wifi_client    echo 'vagrant' | sudo -S wpa_cli wps_pbc ${result_mac}

    #Go to WPS page to click connect button
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    WPS
    cpe click    web    xpath=//button[@id='connect_btn']


    #${result} =    cli    wifi_client    iwconfig
    ${result} =    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interfafe Up    wifi_client    ${g_ssid_name}
    wait until keyword succeeds     3x   10 sec     ping    ${dut_gw}

*** Keywords ***
Get Wifi Mac From SSID Using WPA Supplicant
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    cli    wifi_client    echo 'vagrant' | sudo -S sudo wpa_cli scan
    ${result} =    cli    ${device}    echo 'vagrant' | sudo -S sudo wpa_cli scan_results | grep ${SSID}
    log    ${result}
    Should not be empty    ${result}
    ${register_value_list} =    Get Regexp Matches    ${result}    ([\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2})      1
    Should not be empty    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${wifi_mac} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${wifi_mac}
    [Return]    ${wifi_mac}


Is WIFI Interfafe Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

*** comment ***



 1157  ps -aux | grep wpa_su
 1158  sudo kill -9 12380
 1159  sudo kill -9 12406
 1160  cat /etc/wpa_supplicant/wpa_supplicant.conf
 1161  vi sudo wpa_supplicant -Dwext -iwlan0 -C/var/run/wpa_supplicant/ -c/etc/wpa_supplicant/wpa_supplicant.conf &
 1162  vi /etc/wpa_supplicant/wpa_supplicant.conf
 1163  sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
 1164  sudo wpa_supplicant -Dwext -iwlan0 -C/var/run/wpa_supplicant/ -c/etc/wpa_supplicant/wpa_supplicant.conf &
 1165  sudo wpa_cli scan
 1166  sudo wpa_cli scan_results | grep thomas
 1167  sudo wpa_cli scan_results
 1168  sudo wpa_cli scan_results | grep thomas
 1169  sudo wpa_cli scan_results
 1170  sudo wpa_cli scan
 1171  sudo wpa_cli scan_results
 1172  sudo wpa_cli scan_results | grep thomas
 1173  sudo wpa_cli scan
 1174  sudo wpa_cli scan_results | grep thomas
 1175  history
thomas@thomas-VPCEB37FW:~$