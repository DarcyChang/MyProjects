*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang    stable

*** Variables ***
${g_ssid_name}    CXNK-gavin-5G
${dut_gw}    192.168.1.1
${status_wirelessstatus_url}    http://${dut_gw}/html/status/status_wirelessstatus.html
${wireless_url}    http://${dut_gw}/html/wireless/2dot4ghz/wireless_radiosetup.html
${security_type}    WEP

*** Test Cases ***
tc_RG_5GWIFI_Security_Verify_no_WEP_option_in_security_type
    [Documentation]    tc_RG_5GWIFI_Security_Verify_no_WEP_option_in_security_type
    ...   Verify no WEP option in security type in 5G Wireless.
    [Tags]    @TCID=STP_DD-TC-10908    @globalid=1526091    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
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
    ${result} =     Get List Items    web    xpath=//select[@id='security_type']
    log    ${result}
    Should Not Contain    ${result}    ${security_type}

*** Keywords ***

*** comment ***
