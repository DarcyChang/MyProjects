*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemtek_Gavin_Chang    stable

Suite Setup    Run keywords    Enter Shell
Suite Teardown    Run keywords    Remove Linux WPA Supplicant

*** Variables ***
${g_ssid_name}    CXNK-jujung-2.4g
${844fb_dump_led_register}     dw fffe8114
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${status_wirelessstatus_url}    http://${dut_gw}/html/status/status_wirelessstatus.html
${wireless_url}    http://${dut_gw}/html/wireless/2dot4ghz/wireless_radiosetup.html

*** Test Cases ***
tc_WPS_Solid_Green_Synchronized_State
    [Documentation]    tc_WPS_Solid_Green_Synchronized_State
    ...   1. login to ubuntu to init wpa_supplicant
    ...   2. In DUT, click WPS connect  id=connect_btn
    ...   3. In ubunutu, execute wps_pbc command to connect to dut
    [Tags]    @TCID=PREMS-TC-7910    @globalid=1597636LED844F    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang

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

    #Go to Status/Wireless page to see if changed ssid is present, using go to page instead of click links due to the duplicate name of wireless
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${status_wirelessstatus_url}
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =     get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_ssid_name}

    #Login Linux wifi client to connect to DUT 2.4 ssid
    cli    wifi_client    whoami
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -C /var/run/wpa_supplicant/ -c ~/wpa.conf -B
    ${result_mac} =    Wait Until Keyword Succeeds    10x    3s    Get Wifi Mac From SSID Using WPA Supplicant    wifi_client    ${g_ssid_name}
    log    ${result}
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli wps_pbc ${result_mac}

    #Go to WPS page to click connect button
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${wireless_url}
    Wait Until Keyword Succeeds    5x    3s    click links    web    WPS
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Connect')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Connect')]
    #Check Wi-Fi connect successfully
    ${result} =    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    wait until keyword succeeds     3x   10 sec     ping    ${dut_gw}
    #Check WPS_Green_ON Register Value : bit 14 is 0
    Wait Until Keyword Succeeds    5x    20s    Check WPS Green ON    n1
    #Check WPS_Red_OFF Register Value : bit 8 is 1
    Wait Until Keyword Succeeds    5x    20s    Check WPS Red OFF    n1

*** Keywords ***
Enter Shell
    [Arguments]
    [Documentation]    To enter the shell
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang
    Wait Until Keyword Succeeds    5x    3s    cli    n1    sh    ~ #

Check WPS Green ON
    [Arguments]    ${device}
    [Documentation]    Check WPS Green ON
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    Wait Until Keyword Succeeds    5x    3s    Get WPS Green LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal     ${result}    0

Check WPS Red OFF
    [Arguments]    ${device}
    [Documentation]    Check WPS Red OFF
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    Wait Until Keyword Succeeds    5x    3s    Get WPS Red LED Status From Register Value    ${device}
    log    ${result}
    Should Be Equal     ${result}    1

Remove Linux WPA Supplicant
    [Arguments]
    [Documentation]    To cleanup Linux wpa_supplicant daemon and exit the shell
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    wifi_client    whoami
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    n1    exit

Get Wifi Mac From SSID Using WPA Supplicant
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S sudo wpa_cli scan
    ${result} =    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S sudo wpa_cli scan_results | grep ${SSID}
    log    ${result}
    Should not be empty    ${result}
    ${register_value_list} =    Get Regexp Matches    ${result}    ([\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2}:[\\w]{2})      1
    Should not be empty    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${wifi_mac} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${wifi_mac}
    [Return]    ${wifi_mac}


Is WIFI Interface Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Get WPS Green LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    When WPS green off, the register value is 17eadfef => Should retrive the 5th hex: d->1011, bit 14 is 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{4}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{1}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

Get WPS Red LED Status From Register Value
    [Arguments]    ${device}
    [Documentation]    When WPS red off, the register value is 17eadfef => Should retrive the 6th hex: f->1111, bit 8 is 1
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${dump_register_value}    cli    ${device}    ${844fb_dump_led_register}
    ${register_value_list} =    Get Regexp Matches    ${dump_register_value}    0xFFFE8114\\s:\\s\\w{5}([\\w]{1})     1
    log to console    ${register_value_list}
    ${length} =    Get Length    ${register_value_list}
    ${hex_register_value} =    Run Keyword If    ${length}    Get From List     ${register_value_list}    0
    ...    ELSE    Set Variable    false_default_str
    log   ${hex_register_value}
    ${binary_register_value} =    Convert To Binary    ${hex_register_value}    base=16    length=4
    ${ret_list} =    Get Regexp Matches    ${binary_register_value}    \\w{3}([\\w{1}])    1
    ${ret} =    Get From List     ${ret_list}    0
    log to console    ${ret}
    [Return]    ${ret}

*** comment ***
