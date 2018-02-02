*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

Suite Teardown    Run keywords    Restore Original Security Type

*** Variables ***
${g_ssid_name}    CXNK-gavin-5G
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${status_wirelessstatus_url}    http://${dut_gw}/html/status/status_wirelessstatus.html
${wireless_url}    http://${dut_gw}/html/wireless/2dot4ghz/wireless_radiosetup.html
${security_type}    Security Off

*** Test Cases ***
tc_RG_5GWIFI_Security_Verify_Security_Off_security
    [Documentation]    tc_RG_5GWIFI_Security_Verify_Security_Off_security
    ...   1. After the configuration is applied, GUI page should show according to your setting.
    ...   2. Use one laptop to get IP from ONT via wireless with your setting.
    ...   3. Laptop connect screen will show the security type.
    [Tags]    @TCID=STP_DD-TC-10909    @globalid=1526092    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
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
    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    input_text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    # Check if Wi-Fi 5G SSID name is changed correctly
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    get_element_value    web    xpath=//input[@id="id_ssid_name"]
    should be equal    ${result}    ${g_ssid_name}

    #Go to Status/Wireless page to see if changed ssid is present, using go to page instead of click links due to the duplicate name of wireless
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${status_wirelessstatus_url}
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =     Get List Items    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_ssid_name}

    #Select security type to Security Off
    Wait Until Keyword Succeeds    5x    3s    go to page    web    ${wireless_url}
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    select_from_list_by_label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='security_type']
    should be equal   ${items}    ${security_type}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Verify Wi-Fi connection is successful
    Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key    wifi_client


*** Keywords ***
Restore Original Security Type
    [Arguments]
    [Documentation]    Restore Original Security Type to WPA - WPA2-Personal
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    select_from_list_by_label    web    xpath=//select[@id='security_type']    WPA - WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]

Login Linux Wifi Client To Connect To DUT 5g Ssid Without Security Key
    [Arguments]    ${device}
    [Documentation]    Connect to DUT 5g ssid without security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${g_ssid_name}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s    Is Ping Successful    wifi_client    ${dut_gw}

Is Ping Successful
    [Arguments]    ${device}    ${gw_ip}
    [Documentation]    To check ping ${dut_gw} is successful
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}   ping ${gw_ip} -c 3
    log    ${result}
    Should not contain    ${result}    100% packet loss

Is WIFI Interface Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}

*** comment ***
