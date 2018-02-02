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
${security_type}    WPA2-Personal
${custom_security_key}    1234abcd
${unmatched_wifi_pwd}    unmatchedwifipwd


*** Test Cases ***
tc_RG_5GWIFI_Security_Verify_WPA2_Personal_security_type_with_Custom_Security
    [Documentation]    tc_RG_5GWIFI_Security_Verify_WPA2_Personal_security_type_with_Custom_Security
    ...   1. After the configuration is applied, GUI page should show according to your setting.
    ...   2. Use one laptop to get IP from ONT via wireless with your setting.
    ...   3. Laptop connect screen will show the security type.
    [Tags]    @TCID=STP_DD-TC-10907    @globalid=1526090    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 5GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Enable WiFi 5GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    select radio button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wireless_onoff    1

    #Change WiFi 5G SSID
    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    input_text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    cpe click    web    xpath=//button[contains(., 'Apply')]

    # Check if Wi-Fi 5G SSID name is changed correctly
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    get_element_value    web    xpath=//input[@id="id_ssid_name"]
    should be equal    ${result}    ${g_ssid_name}

    #Go to Status/Wireless page to see if changed ssid is present, using go to page instead of click links due to the duplicate name of wireless
    Wait Until Keyword Succeeds    5x    3s    go to page    web        ${status_wirelessstatus_url}
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =    Get List Items    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_ssid_name}

    #Select security type to WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${wireless_url}
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    select_from_list_by_label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='security_type']
    should be equal   ${items}    ${security_type}

    #Select Custom Security Key
    Select Custom Security Key    ${custom_security_key}

    #Read Wi-Fi Password
    ${matched_wifi_pwd} =    get_element_value    web    pskKeyInput

    #Select encryption type to AES
    Select Encryption Type    AES

    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key    wifi_client    ${matched_wifi_pwd}
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Security Type    wifi_client
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Encryption Type    wifi_client    TKIP
    Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Security Key    wifi_client    ${unmatched_wifi_pwd}

*** Keywords ***
Select Custom Security Key
    [Arguments]    ${custom_security_key}
    [Documentation]    Select custom security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    Click Element    web    xpath=//input[@id='lshxq02']
    input_text    web    xpath=//input[@id='pskKeyInput']    ${custom_security_key}


Select Encryption Type
    [Arguments]    ${encryption_type}
    [Documentation]    Select encryption type(AES/TKIP/Both)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    select_from_list_by_label    web    xpath=//select[@id='id_wpa_cipher']    ${encryption_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_wpa_cipher']
    should be equal   ${items}    ${encryption _type}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]


Login Linux Wifi Client To Connect To DUT 5g Ssid With Matched Security Key
    [Arguments]    ${device}    ${secruity_key}
    [Documentation]    Connect to DUT 5g ssid with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s    Is Ping Successful    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Security Type
    [Arguments]    ${device}
    [Documentation]    Connect to DUT 5g ssid with unmatched security type(choose security off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    mv wpa.conf temp
    cli    ${device}    head -n 4 temp > wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    rm temp
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s     Is Ping Fail    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Encryption Type
    [Arguments]    ${device}    ${unmatched_encryption_type}
    [Documentation]    Connect to DUT 5g ssid with unmatched encryption type(choose TKIP)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    mv wpa.conf temp
    cli    ${device}    head -n 4 temp > wpa.conf
    cli    ${device}    echo 'group=${unmatched_encryption_type}\n}' >> wpa.conf
    cli    ${device}    rm temp
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s     Is Ping Fail    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 5g Ssid With Unmatched Security Key
    [Arguments]    ${device}    ${secruity_key}
    [Documentation]    Connect to DUT 5g ssid with unmatched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s    Is Ping Fail    wifi_client    ${dut_gw}

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
