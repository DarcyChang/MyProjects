*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang

*** Variables ***
${g_844_wifi_client_pwd}    vagrant
${g_844_wifi_client_ip}    192.168.1.188
${dut_gw}    192.168.1.1
${security_type1}    WPA - WPA2-Personal
${security_type2}    WPA2-Personal
${security_type3}    Security Off
${8_characters_security_key}    1234abcd
${30_characters_security_key}    1234567890abcdefghijklmonporst
${63_characters_security_key}    1234567890abcdefghijklmonporst1234567890abcdefghijklmonporst123
${unmatched_wifi_pwd}    unmatchedwifipwd

*** Test Cases ***
tc_RG_2.4GWIFI_Security_Verify_remaining_SSID_functions
    [Documentation]    tc_RG_2.4GWIFI_Security_Verify_remaining_SSID_functions
    ...   1. After the configuration is applied, GUI page should show according to your setting.
    ...   2. Use one laptop to get IP from ONT via wireless with your setting.
    ...   3. Laptop connect screen will show the security type.
    ...   4. Change to other SSID
    [Tags]    @TCID=STP_DD-TC-10882    @globalid=1526049    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    #Enable WiFi 2.4 GHz
    Wait Until Element Is Visible    web    name=wireless_onoff
    select radio button    web    wireless_onoff    1
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wireless_onoff    1

    #Select WiFi 2.4G SSID to 2.4GHz_Guest040D1E
    Select WiFi 2.4G SSID    1
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    ${test_ssid} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']
    ${test_gw} =    get_element_value    web    xpath=//input[@id="gatewayObj"]
    ${test_client_ip} =    get_element_value    web    xpath=//input[@id="ipAddressStartObj"]

    #Select security type to WPA-WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    1    ${security_type1}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}_pwd}

    #Select encryption type to TKIP
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Encryption Type    TKIP
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}

    #Select encryption type to Both
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Encryption Type    Both
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}

    #Select security type to WPA2-Personal
    Select Security Type    1    ${security_type2}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    1
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${test_gw}    ${test_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${test_gw}    ${test_client_ip}

    #Select security type to Security Off
    Select Security Type    1    ${security_type3}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Verify Wi-Fi connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid Without Security Key    wifi_client    ${test_ssid}    ${test_gw}    ${test_client_ip}


    #Select WiFi 2.4G SSID to 2.4GHz_Operator_1
    Select WiFi 2.4G SSID    2
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    ${test_ssid} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']

    #Select security type to WPA-WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    2    ${security_type1}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}_pwd}

    #Select encryption type to TKIP
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Encryption Type    TKIP
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select encryption type to Both
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Encryption Type    Both
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select security type to WPA2-Personal
    Select Security Type    2    ${security_type2}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    2
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select security type to Security Off
    Select Security Type    2    ${security_type3}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Verify Wi-Fi connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid Without Security Key    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}


    #Select WiFi 2.4G SSID for 2.4GHz_Operator_2
    Select WiFi 2.4G SSID    3
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    ${test_ssid} =    get_selected_list_label    web    xpath=//select[@id='id_ssid']

    #Select security type to WPA-WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Select Security Type    3    ${security_type1}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}_pwd}

    #Select encryption type to TKIP
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Encryption Type    TKIP
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    CCMP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select encryption type to Both
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Encryption Type    Both
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select security type to WPA2-Personal
    Select Security Type    3    ${security_type2}

    #Select encryption type to AES
    Select Encryption Type    AES
    #Select 8 characters custom security key
    Select Custom Security Key    ${8_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${8_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 30 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${30_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${30_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}
    #Select 63 characters custom security key
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    3
    Select Custom Security Key    ${63_characters_security_key}
    #Verify wireless connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key    wifi_client    ${test_ssid}    ${63_characters_security_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type    wifi_client    ${test_ssid}    TKIP    ${dut_gw}    ${g_844_wifi_client_ip}
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key    wifi_client    ${test_ssid}    ${unmatched_wifi_pwd}    ${dut_gw}    ${g_844_wifi_client_ip}

    #Select security type to Security Off
    Select Security Type    3    ${security_type3}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Verify Wi-Fi connection is successful
    Login Linux Wifi Client To Connect To DUT 2.4g Ssid Without Security Key    wifi_client    ${test_ssid}    ${dut_gw}    ${g_844_wifi_client_ip}

*** Keywords ***
Select WiFi 2.4G SSID
    [Arguments]    ${ssid_index}
    [Documentation]    Select WiFi 2.4G SSID(1:2.4GHz_Guest040D1E, 2:2.4GHz_Operator_1, 3:2.4GHz_Operator_2)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    click links    web    SSID Setup
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    select radio button    web    ssid_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    name=ssid_state
    radio_button_should_be_set_to    web    ssid_state    1



Select Security Type
    [Arguments]    ${ssid_index}    ${security_type}
    [Documentation]    Select security type(1:WPA-WPA2-Personal, 2:WPA2-Personal, 3:Security Off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    xpath=//select[@id='id_ssid']    ${ssid_index}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    select_from_list_by_label    web    xpath=//select[@id='security_type']    ${security_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='security_type']
    should be equal   ${items}    ${security_type}

Select Custom Security Key
    [Arguments]    ${custom_security_key}
    [Documentation]    Select custom security key(8, 30 and 63 characters)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    input_text    web    xpath=//input[@id='pskKeyInput']    ${custom_security_key}
    #Read Wi-Fi Password
    ${g_custom_wifi_pwd} =    get_element_value    web    pskKeyInput
    log    ${g_custom_wifi_pwd}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

Select Encryption Type
    [Arguments]    ${encryption_type}
    [Documentation]    Select encryption type(AES/TKIP/Both)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    select_from_list_by_label    web    xpath=//select[@id='id_wpa_cipher']    ${encryption_type}
    ${items} =    get_selected_list_label    web    xpath=//select[@id='id_wpa_cipher']
    should be equal   ${items}    ${encryption_type}


Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Matched Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${secruity_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 2.4g ssid with matched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Up    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x   10s    Is Ping Successful    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Type
    [Arguments]    ${device}    ${g_ssid_name}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 2.4g ssid with unmatched security type(choose security off)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    mv wpa.conf temp
    cli    ${device}    head -n 5 temp > wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    rm temp
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s     Is Ping Fail    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Encryption Type
    [Arguments]    ${device}    ${g_ssid_name}    ${unmatched_encryption_type}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 2.4g ssid with unmatched encryption type(choose TKIP/CCMP=AES)
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    mv wpa.conf temp
    cli    ${device}    head -n 5 temp > wpa.conf
    cli    ${device}    echo 'group=${unmatched_encryption_type}\n}' >> wpa.conf
    cli    ${device}    rm temp
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    5x    10s     Is Ping Fail    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 2.4g Ssid With Unmatched Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${unmatched_secruity_key}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 2.4g ssid with unmatched security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    wpa_passphrase ${g_ssid_name} ${unmatched_secruity_key} > wpa.conf
    cli    ${device}    sed -i '4ascan_ssid=1' wpa.conf
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S wpa_supplicant -D wext -i ${g_844_wifi_client_int} -c ~/wpa.conf -B
    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S ifconfig ${g_844_wifi_client_int} ${g_844_wifi_client_ip}
    Wait Until Keyword Succeeds    10x    5s    Is WIFI Interface Down    wifi_client    ${g_ssid_name}
    Wait Until Keyword Succeeds    10x   10s    Is Ping Fail    wifi_client    ${dut_gw}

Login Linux Wifi Client To Connect To DUT 2.4g Ssid Without Security Key
    [Arguments]    ${device}    ${g_ssid_name}    ${dut_gw}    ${g_844_wifi_client_ip}
    [Documentation]    Connect to DUT 2.4g ssid without security key
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    cli    ${device}    echo ${g_844_wifi_client_pwd} | sudo -S killall wpa_supplicant
    cli    ${device}    echo 'network={' > wpa.conf
    cli    ${device}    echo 'ssid="${g_ssid_name}"' >> wpa.conf
    cli    ${device}    echo 'key_mgmt=NONE\n}' >> wpa.conf
    cli    ${device}    sed -i '3ascan_ssid=1' wpa.conf
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
