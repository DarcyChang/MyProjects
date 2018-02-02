*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

*** Variables ***
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${security_type}    Security Off
${rename_first_ssid}    gavin-5g-rename1
${rename_second_ssid}    gavin-5g-raname2
${rename_third_ssid}    gavin-5g-raname3
${rename_fourth_ssid}    gavin-5g-raname4

*** Test Cases ***
tc_RG_5GWIFI_SSID_Verify_SSID_rename
    [Documentation]    tc_RG_5GWIFI_SSID_Verify_SSID_rename
    ...   1. Rename SSID network name.
    ...   2. After the configuration is applied, GUI page should show according to your setting.
    ...   3. Use one laptop to get IP from ONT via wireless with your setting.
    ...   4. Change to other SSID
    [Tags]    @TCID=STP_DD-TC-10914    @globalid=1526098    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 5 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Enable WiFi 5 GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    Select Radio Button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    1

    #Rename the first WiFi 5G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${original_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']
    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${rename_first_ssid}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${rename_first_ssid}
    Radio Button Should Be Set To    web    ssid_mode    1

    #Select security type to Security Off
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    0    ${security_type}

    #Scan SSID and verify wireless connection
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Scan SSID Successful    wifi_client    ${rename_first_ssid}
    Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key    wifi_client    ${rename_first_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Restore to original SSID and setting
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${original_ssid}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${original_ssid}


    #Rename the second WiFi 5G SSID
    Select WiFi 5G SSID  1
    ${original_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']
    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${rename_second_ssid}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${rename_second_ssid}
    Radio Button Should Be Set To    web    ssid_mode    1
    ${test_gw} =    Get Element Value    web    xpath=//input[@id="gatewayObj"]
    ${test_client_ip} =    Get Element Value    web    xpath=//input[@id="ipAddressStartObj"]

    #Select security type to Security Off
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    1    ${security_type}

    #Scan SSID and verify wireless connection
    cli    wifi_client    echo ${g_844_wifi_client_pwd}| sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd}| sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Scan SSID Successful    wifi_client    ${rename_second_ssid}
    Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key    wifi_client    ${rename_second_ssid}    ${test_gw}    ${test_client_ip}

    #Restore to original SSID and setting
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${original_ssid}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${original_ssid}


    #Rename the third WiFi 5G SSID
    Rename WiFi 5G SSID And Verify The Wireless Connection    wifi_client    2    ${rename_third_ssid}

    #Rename the fourth WiFi 5G SSID
    Rename WiFi 5G SSID And Verify The Wireless Connection    wifi_client    3    ${rename_fourth_ssid}

*** Keywords ***
Select WiFi 5G SSID
    [Arguments]    ${ssid_index}
    [Documentation]    Select WiFi 5G SSID(1:5GHz_Guest040D1E, 2:5GHz_Operator_1, 3:5GHz_Operator_2)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    select radio button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    Radio Button Should Be Set To    web    ssid_state    1


Select Security Type
    [Arguments]    ${ssid_index}    ${security_type}
    [Documentation]    Select security type(WPA-WPA2-Personal, WPA2-Personal, Security Off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Select From List By Label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    Get Selected List Label    web    xpath=//select[@id='security_type']
    Should Be Equal   ${items}    ${security_type}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

Scan SSID Successful
    [Arguments]    ${device}    ${g_ssid_name}
    [Documentation]    Scan the broadcast SSID
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan_results | grep gavin > temp
    ${result} =    cli    ${device}    cat temp
    log    ${result}
    Should Contain    ${result}    ${g_ssid_name}
    cli    ${device}    rm temp

Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 5g ssid without security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${g_ssid_name}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds     5x   10s     Is Ping Successful    wifi_client    ${dut_gw}

Is Ping Successful
    [Arguments]    ${device}    ${gw_ip}
    [Documentation]    To check ping ${gw_ip} is successful
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c 3
    log    ${result}
    Should Not Contain    ${result}    100% packet loss


Is WIFI Interface Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Rename WiFi 5G SSID And Verify The Wireless Connection
    [Arguments]    ${device}    ${ssid_index}    ${rename_ssid_index}
    [Documentation]    Rename WiFi 5G SSID, scan and connect with wireless
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Select WiFi 5G SSID  ${ssid_index}
    ${original_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']
    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${rename_ssid_index}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${rename_ssid_index}
    Radio Button Should Be Set To    web    ssid_mode    1

    #Select security type to Security Off
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    ${ssid_index}    ${security_type}

    #Scan SSID and verify wireless connection
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    ${device}    echo 'update_config=1' >> wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    3s    Scan SSID Successful    wifi_client    ${rename_ssid_index}
    Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key    wifi_client    ${rename_ssid_index}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Restore to original SSID and setting
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${original_ssid}
    Select Radio Button    web    ssid_mode    0
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${original_ssid}
    Radio Button Should Be Set To    web    ssid_mode    0

*** comment ***
