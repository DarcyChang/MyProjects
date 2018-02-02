*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun

Suite Teardown    Run keywords    Reset Linux WPA Supplicant
*** Variables ***
${g_844_wifi_client_user}    vagrant
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_int}    wlan0
${dut_gw}    192.168.1.1
${sleep_seconds}    120
*** Test Cases ***
tc_RG_2.4GWIFI_WPS_Verify_WPS_function_2.4G
    [Documentation]    tc_RG_2.4GWIFI_WPS_Verify_WPS_function_2.4G
    ...   1. login to ubuntu to init wpa_supplicant
    ...   2. In DUT, click WPS connect  id=connect_btn
    ...   3. In ubunutu, execute wps_pbc command to connect to DUT
    [Tags]    @TCID=STP_DD-TC-10888    @globalid=1526057    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
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

    #Go to Status/Wireless page to see if changed ssid is present
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
	Wait Until Keyword Succeeds    5x    3s    go_to_page    web    ${g_844fb_gui_url}/html/status/status_wirelessstatus.html
    ${result} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_844fb_2.4g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_844fb_2.4g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_844fb_2.4g_ssid_name}


    #Login Linux wifi client to connect to DUT 2.4 ssid
    cli    wifi_client    whoami
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo 'vagrant' | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -C /var/run/wpa_supplicant/ -c ~/wpa.conf -B
    ${result_mac} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Mac From SSID Using WPA Supplicant    wifi_client    ${g_844fb_2.4g_ssid_name}
    log    ${result}
    cli    wifi_client    echo 'vagrant' | sudo -S wpa_cli wps_pbc ${result_mac}

    #Go to WPS page to click connect button
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    WPS
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id='connect_btn']

    #Linux wifi client ping DUT
    ${result} =    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interfafe Up    wifi_client    ${g_844fb_2.4g_ssid_name}
    wait until keyword succeeds     3x   10 sec     ping    ${dut_gw}

*** Keywords ***
Get Wifi Mac From SSID Using WPA Supplicant
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    wifi_client    echo 'vagrant' | sudo -S sudo wpa_cli scan
    sleep    3s
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
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Reset Linux WPA Supplicant
    [Arguments]
    [Documentation]    To cleanup Linux wpa_supplicant daemon
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    cli    wifi_client     whoami
    cli    wifi_client     echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client     echo 'vagrant' | sudo -S killall wpa_supplicant
    # Waitting WPS Button 120 secconds reciprocal
    sleep    ${sleep_seconds}
*** comment ***