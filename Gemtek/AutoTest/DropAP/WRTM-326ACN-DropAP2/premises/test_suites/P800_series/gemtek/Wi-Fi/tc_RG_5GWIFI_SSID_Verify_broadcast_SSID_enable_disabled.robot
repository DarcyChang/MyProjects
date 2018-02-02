*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

*** Variables ***
${g_ssid_name}    CXNK-gavin-5G
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${security_type}    WPA - WPA2-Personal
${custom_security_key}    1234abcd


*** Test Cases ***
tc_RG_5GWIFI_SSID_Verify_broadcast_SSID_enable_disabled
    [Documentation]    tc_RG_5GWIFI_SSID_Verify_broadcast_SSID_enable_disabled.
    ...   1. After the configuration is applied, GUI page should show according to your setting.
    ...   2. Use one laptop to get IP from ONT via wireless with your setting.
    ...   3. Change to other SSID
    [Tags]    @TCID=STP_DD-TC-10915    @globalid=1526099    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
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

    #Select the first WiFi 5G SSID and rename
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}

    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    ssid_mode    1
    ${test_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']

    #Scan SSID
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    10s    Scan SSID Successful    wifi_client    ${test_ssid}

    #Disable Broadcast SSID
    Select Radio Button    web    ssid_mode    0
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    ssid_mode    0
    Wait Until Keyword Succeeds    10x    20s    Scan SSID Fail    wifi_client    ${test_ssid}

    #Select security type to WPA-WPA2
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    0    ${security_type}

    #Set custom security key
    Select Custom Security Key    0    ${custom_security_key}
    #Verify wireless connection
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${custom_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Restore to original setting : boradcast is enabled
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Select Radio Button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    ssid_mode    1

    #Select the second WiFi 5G SSID
    Select WiFi 5G SSID  1
    ${test_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']
    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    Select From List By Value    web    xpath=//select[@id='id_ssid']    1
    Radio Button Should Be Set To    web    ssid_mode    1
    ${test_gw} =    Get Element Value    web    xpath=//input[@id="gatewayObj"]
    ${test_client_ip} =    Get Element Value    web    xpath=//input[@id="ipAddressStartObj"]

    #Scan SSID
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    10x    10s    Scan SSID Successful    wifi_client    ${test_ssid}

    #Disable Broadcast SSID
    Select Radio Button    web    ssid_mode    0
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    Select From List By Value    web    xpath=//select[@id='id_ssid']    1
    Radio Button Should Be Set To    web    ssid_mode    0
    Wait Until Keyword Succeeds    10x    20s    Scan SSID Fail    wifi_client    ${test_ssid}

    #Select security type to WPA-WPA2
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    1    ${security_type}

    #Set custom security key
    Select Custom Security Key    1    ${custom_security_key}
    #Verify wireless connection
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${custom_security_key}    ${test_gw}    ${test_client_ip}


    #Select the third WiFi 5G SSID
    Select WiFi 5G SSID And Verify The Broadcast Function    wifi_client    2

    #Select the fourth WiFi 5G SSID
    Select WiFi 5G SSID And Verify The Broadcast Function    wifi_client    3

*** Keywords ***
Select WiFi 5G SSID
    [Arguments]    ${ssid_index}
    [Documentation]    Select WiFi 5G SSID(1:5GHz_Guest040D1E, 2:5GHz_Operator_1, 3:5GHz_Operator_2)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    Select Radio Button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    Radio Button Should Be Set To    web    ssid_state    1

Select Security Type
    [Arguments]    ${ssid_index}    ${security_type}
    [Documentation]    Select security type(WPA-WPA2-Personal, WPA2-Personal, Security Off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    Select From List By Value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Select From List By Label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    Get Selected List Label    web    xpath=//select[@id='security_type']
    Should Be Equal   ${items}    ${security_type}

Select Custom Security Key
    [Arguments]    ${ssid_index}    ${custom_security_key}
    [Documentation]    Select custom security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Run Keyword If    ${ssid_index} == 0    Wait Until Keyword Succeeds    5x    3s    Click Element    web    xpath=//input[@id='lshxq02']
    Input Text    web    xpath=//input[@id='pskKeyInput']    ${custom_security_key}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Value    web    xpath=//input[@id="pskKeyInput"]
    Should Be Equal    ${result}    ${custom_security_key}

Scan SSID Successful
    [Arguments]    ${device}    ${g_ssid_name}
    [Documentation]    Scan the broadcast SSID(enabled)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan_results | grep 5G > temp
    ${result} =    cli    ${device}    cat temp
    log    ${result}
    Should Contain    ${result}    ${g_ssid_name}
    cli    ${device}    rm temp

Scan SSID Fail
    [Arguments]    ${device}    ${g_ssid_name}
    [Documentation]    Scan the broadcast SSID(disabled)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_cli scan_results | grep gavin > temp
    ${result} =    cli    ${device}    cat temp
    log    ${result}
    Should Not Contain    ${result}    ${g_ssid_name}
    cli    ${device}    rm temp


Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${secruity_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 5g ssid with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x   10s    Is Ping Successful    wifi_client    ${dut_gw}

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

Select WiFi 5G SSID And Verify The Broadcast Function
    [Arguments]    ${device}    ${ssid_index}
    [Documentation]    Select WiFi 5G SSID And Verify The Broadcast Function(enabled and disabled)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Select WiFi 5G SSID  ${ssid_index}
    ${test_ssid} =    Get Selected List Label    web    xpath=//select[@id='id_ssid']
    #Enable Broadcast SSID
    Select Radio Button    web    ssid_mode    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    Select From List By Value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Radio Button Should Be Set To    web    ssid_mode    1

    #Scan SSID
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    wifi_client    echo 'ctrl_interface=/var/run/wpa_supplicant/' > wpa.conf
    cli    wifi_client    echo 'update_config=1' >> wpa.conf
    cli    wifi_client    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    Wait Until Keyword Succeeds    20x    10s    Scan SSID Successful    wifi_client    ${test_ssid}

    #Disable Broadcast SSID
    Select Radio Button    web    ssid_mode    0
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    Select From List By Value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Radio Button Should Be Set To    web    ssid_mode    0
    Wait Until Keyword Succeeds    10x    20s    Scan SSID Fail    wifi_client    ${test_ssid}

    #Select security type to WPA-WPA2
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    ${ssid_index}    ${security_type}

    #Set custom security key
    Select Custom Security Key    ${ssid_index}    ${custom_security_key}
    #Verify wireless connection
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${custom_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}

*** comment ***
