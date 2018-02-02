*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Gavin_Chang    norun

*** Variables ***
${g_ssid_name}     CXNK-jujung-2.4g
${g_844_wifi_client_user}    vagrant
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_int}    wlan0
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1


*** Keywords ***

*** Test Cases ***


tc_WiFi_2_4_GHz_Flashing_Green_Activity_Radio_ON_with_Clients
    [Documentation]    tc_WiFi_2_4_GHz_Flashing_Green_Activity_Radio_ON_with_Clients
    ...   Verify if the WiFi 2.4 GHz LED stay in Solid Green state when WiFi 2.4 GHz no clients connected.
    ...   When WiFi 2.4 GHz enable but no clients connected, the WiFi 2.4GHz LED stay in solid green.
    [Tags]    @TCID=PREMS-TC-7890   @globalid=1597611LED844F   @DUT=844FB   @DUT=844F
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    click links    web    Wireless
    #Enable WiFi 2.4 GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    select radio button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wireless_onoff    1

    #Change WiFi 2.4G SSID
    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    input_text    web    xpath=//input[@id='id_ssid_name']    ${g_ssid_name}
    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Read Wi-Fi Password
    click links    web    Security
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${g_default_wifi_pwd} =    get_element_value    web    defaultPskKeyInput
    log    ${g_default_wifi_pwd}

    # Check if Wi-Fi 2.4G SSID name is changed correctly
    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    get_element_value    web    xpath=//input[@id="id_ssid_name"]
    should be equal    ${result}    ${g_ssid_name}

    #Go to Status/Wireless page to see if changed ssid is present
    click links    web    Status
    click links    web    Wireless
    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =     get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_ssid_name}

    #Login Linux wifi client to connect to DUT 2.4 ssid
    cli    wifi_client    ls
    cli    wifi_client    echo 'vagrant' | sudo -S killall wpa_supplicant
    cli    wifi_client    vagrant
    cli    wifi_client    wpa_passphrase CXNK-gavin-2.4g ${g_default_wifi_pwd} > wpa.conf
    cli    wifi_client    echo 'vagrant' | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    wifi_client    echo 'vagrant' | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    #cli    wifi_client    echo \'${g_844_wifi_client_pwd}\' | sudo -S wpa_supplicant -Dwext -i${g_844_wifi_client_int} -c ~/wpa.conf -B
    #cli    wifi_client    echo \'${g_844_wifi_client_pwd}\' | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    ${result} =    cli    wifi_client    iwconfig
    ${result} =    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interfafe Up    wifi_client    ${g_ssid_name}
    wait until keyword succeeds     3x   10 sec     ping    ${dut_gw}



*** Keywords ***
Is WIFI Interfafe Up
    [Arguments]    ${device}    ${SSID}
    [Documentation]    To check if wifi interface is up
    [Tags]    @AUTHOR=Gemteks_Gavin_Chang

    ${result} =    cli    ${device}    iwconfig
    Should Contain    ${result}    ${SSID}


*** comment ***



    #Check led 3 behavior is 8
    cli    n1    sh
    ${result} =   cli    n1     wl -i wl0 ledbh 3
    log    ${result}
    Should Contain    ${result}    led 3 behavior 8
    cli    n1    exit


    #Go to WiFi 5G Control Page
    click links    web    Wireless
    click links    web    5G Network

    #Enable WiFi 5G
    Wait Until Element Is Visible    web    name=wireless_onoff
    select radio button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wireless_onoff    1

    #Change WiFi 5G SSID
    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    Get Element Text    web    xpath=//input[@id="id_ssid_name"]
    input text    web    xpath=//input[@id='id_ssid_name']    ${g_5g_ssid_name}
    cpe click    web    xpath=//button[contains(., 'Apply')]

    # Check if Wi-Fi 5G SSID name is changed correctly
    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    ${result} =    get_element_value    web    xpath=//input[@id="id_ssid_name"]
    should be equal    ${result}    ${g_5g_ssid_name}

    #Go to Status/Wireless page to see if changed ssid is present
    click links    web    Status
    click links    web    Wireless
    Wait Until Element Is Visible    web    xpath=//select[@id='id_ssid']
    ${result} =     get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${g_5g_ssid_name}
    select_from_list_by_label    web    xpath=//select[@id='id_ssid']    ${g_5g_ssid_name}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    should be equal   ${items}    ${g_5g_ssid_name}
