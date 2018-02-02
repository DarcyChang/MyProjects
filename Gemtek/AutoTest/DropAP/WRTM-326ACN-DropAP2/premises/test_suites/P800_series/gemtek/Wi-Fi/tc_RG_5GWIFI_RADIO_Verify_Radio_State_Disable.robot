*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

*** Variables ***
${g_ssid_name}    CXNK-gavin-5G
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${status_wirelessstatus_url}    http://${dut_gw}/html/status/status_wirelessstatus.html
${wireless_url}    http://${dut_gw}/html/wireless/2dot4ghz/wireless_radiosetup.html
${security_type}    WPA - WPA2-Personal
${custom_security_key}    1234abcd


*** Test Cases ***
tc_RG_5GWIFI_RADIO_Verify_Radio_State_Disable
    [Documentation]    tc_RG_5GWIFI_RADIO_Verify_Radio_State_Disable
    ...   1. After the setting is applied, GUI should show Radio state is disabled, and other controls are disabled.
    ...   2. The connected Wi-Fi clients should loss wireless connection, and can not connect to this Wi-Fi again.
    ...   3. After radio enabled, the other controls on GUI are enabled, the Wi-Fi clients can connect to the Wi-Fi again.
    [Tags]    @TCID=STP_DD-TC-10894    @globalid=1526076    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 5GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Enable WiFi  5GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    Select Radio Button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    1
    #Change WiFi 5G SSID
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Input Text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    # Check if Wi-Fi 5G SSID name is changed correctly
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    get_element_value    web    xpath=//input[@id="id_ssid_name"]
    Should Be Equal    ${result}    ${g_ssid_name}
    #Go to Status/Wireless page to see if changed ssid is present, using go to page instead of click links due to the duplicate name of wireless
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${status_wirelessstatus_url}
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =    Get List Items    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    Select From List By Label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    Should Be Equal   ${items}    ${g_ssid_name}

    #Select security type to WPA-WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${wireless_url}
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Select From List By Label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    Get Selected List Label    web    xpath=//select[@id='security_type']
    should be equal   ${items}    ${security_type}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${custom_security_key}
    #Verify the wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${custom_security_key}

    #Disable WiFi  5GHz
    Wait Until Keyword Succeeds    5x    3s    click links    web    Radio Setup
    Wait Until Element Is Visible    web    name=wireless_onoff
    Select Radio Button    web    wireless_onoff    0
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    0
    #Verify the wireless connection is fail
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s     Is Ping Fail    wifi_client    ${dut_gw}

    #Enable WiFi  5GHz
    Select Radio Button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Radio Button Should Be Set To    web    wireless_onoff    1
    #Verify the wireless connection is successful again
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x    10s    Is Ping Successful    wifi_client    ${dut_gw}

*** Keywords ***
Select Custom Security Key
    [Arguments]    ${custom_security_key}
    [Documentation]    Select custom security key(8, 30 and 63 characters)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    Click Element    web    xpath=//input[@id='lshxq02']
    input_text    web    xpath=//input[@id='pskKeyInput']    ${custom_security_key}

    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

Select Encryption Type
    [Arguments]    ${encryption_type}
    [Documentation]    Select encryption type(AES/TKIP/Both)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    select_from_list_by_label    web    xpath=//select[@id='id_wpa_cipher']    ${encryption_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_wpa_cipher']
    should be equal   ${items}    ${encryption _type}

Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key
    [Arguments]    ${device}    ${secruity_key}
    [Documentation]    Connect to DUT 5g ssid with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x    10s    Is Ping Successful    wifi_client    ${dut_gw}

Is Ping Successful
    [Arguments]    ${device}    ${gw_ip}
    [Documentation]    To check ping ${gw_ip} is successful
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c 3
    log    ${result}
    Should not contain    ${result}    100% packet loss

Is Ping Fail
    [Arguments]    ${device}    ${gw_ip}
    [Documentation]    To check ping ${gw_ip} is fail
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c 3
    log    ${result}
    Should Contain    ${result}    100% packet loss

Is WIFI Interface Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

Is WIFI Interface Down
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is down
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Not Contain    ${result}    ${SSID}

*** comment ***
