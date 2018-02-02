*** Settings ***
Resource      base.robot


*** Variables ***
${Input_SSID} =     css=input[id="cbid.wireless.ra0.ssid"]
${Checkbox_Hidden_SSID} =      id=cbid.wireless.ra0.hidden
${Select_Security}=    css=select[id="cbid.wireless.ra0.encryption"]
${Button_SAVE} =    xpath=/html/body/div/div[3]/div[2]/div/form/div[3]/input[1]
${Select_Guest_Turn_On_Off}=    css=select[id="cbid.wireless.ra1.disabled"]
${Input_Guest_SSID}=    css=input[id="cbid.wireless.ra1.ssid"]
${Previous_SSID} =
${Previous_Checkbox_Hidden_SSID_State}=
${Previous_Select_Security}=
${Previous_Input_Password}=
#${Previous_Guest_Network_Radio_On_Off}=
${Previous_Guest_Network_SSID}=
${Input_PasswordForWPA-PSK}=     xpath=//*[@id="cbid.wireless.ra0._wpakey"]
${InvalidHtmlMSGForWirelessPassword}    css=input[class="cbi-input-password cbi-input-invalid"]
${Input_SSID}    xpath=//*[@id="cbid.wireless.ra0.ssid"]
${Select_Security}    xpath=//*[@id="cbid.wireless.ra0.encryption"]
${Checkbox_Hidden}    xpath=//*[@id="cbid.wireless.ra0.hidden"]
${Select_Radio}    xpath=//*[@id="cbid.wireless.ra1.disabled"]
${Input_GuestSSID}    xpath=//*[@id="cbid.wireless.ra1.ssid"]
${Input_Password}    xpath=/html/body/div/div[3]/div[2]/div/form/div[2]/fieldset[1]/div/div[3]/div/input

*** Keywords ***

Set SSID Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]  ${ssid}
    input text    web    ${Input_SSID}    ${ssid}
    Save Wireless Config

Set Hidden SSID Checkbox to Checked
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Select Checkbox    web    ${Checkbox_Hidden_SSID}
    Save Wireless Config

Verify Hidden SSID Checkbox is Checked
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Checkbox Should Be Selected     web     ${Checkbox_Hidden_SSID}

Backup Current Checkbox Hidden SSID State
    [Documentation]
    [Tags]  @AUTHOR=Johnny_Peng
    ${checkbox_state} =     run keyword and return status   Checkbox Should Be Selected     web     ${Checkbox_Hidden_SSID}
    Set Test Variable       ${Previous_Checkbox_Hidden_SSID_State}    ${checkbox_state}

Restore To Previous Checkbox Hidden SSID State
    [Documentation]  Restore the checkbox state
    [Tags]  @AUTHOR=Johnny_Peng
    kw_Common.Set Checkbox State     ${Checkbox_Hidden_SSID}      ${Previous_Checkbox_Hidden_SSID_State}
    Save Wireless Config

Reset To Default Checkbox Hidden SSID State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Unselect checkbox       web     ${Checkbox_Hidden_SSID}
    Save Wireless Config

Backup Previous SSID Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    ${element_value} =     Get Element Value     web      ${Input_SSID}
    Set Test Variable       ${Previous_SSID}    ${element_value}

Restore To Previous SSID Value
    Set SSID Value       ${Previous_SSID}

Verify SSID Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]  ${ssid}
    Wait Until Element Is Visible    web    ${Input_SSID}
    ${input_text}=     Get Element value    web     ${Input_SSID}
    should be equal   ${ssid}    ${input_text}


Backup Current Security And Password State
    [Documentation]  Backup Security List Value, if Security List Value is not Open, Backup Password Value
    [Tags]   @AUTHOR=Johnny_Peng
    Backup Current Security State
    Backup Current Password State

Get Security Value
    [Documentation]
    [Tags]  @AUTHOR=Johnny_Peng
    ${security_value}=   Wait Until Keyword Succeeds    5x    3s    get selected list label    web    ${Select_Security}
    [Return]    ${security_value}

Backup Current Security State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    ${security_value}=   Get Security Value
    Set Test Variable   ${Previous_Select_Security}     ${security_value}

Backup Current Password State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    ${input_password_is_visible}=   Assert Password Input Is Visible
    Run Keyword Unless      ${input_password_is_visible}==True
    ...                      Return From Keyword

    ${password}=     Get Element Value     web      ${Input_Password}
    Set Test Variable   ${Previous_Input_Password}     ${password}

Set Security And Password
    [Documentation]  Write Security and Password Value
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${security}     ${password}
    Set Security Value    ${security}
    Set Password    ${password}
    Save Wireless Config

Set Security Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]       ${security}
    Select From List By Label    web    ${Select_Security}    ${security}

Set Password For WPA-PSK Security Type
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Arguments]     ${password}
    ${input_password_is_visible}=    Assert Password Input Is Visible
    Run Keyword Unless      ${input_password_is_visible}==True
        ...                      Return From Keyword
    input text    web    ${Input_PasswordForWPA-PSK}    ${password}

Set Password
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${password}
    ${input_password_is_visible}=    Assert Password Input Is Visible
    Run Keyword Unless      ${input_password_is_visible}==True
        ...                      Return From Keyword
    input text    web    ${Input_Password}    ${password}

Verify Security And Password Were Set
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${security}    ${password}
    Assert Security Value     ${security}
    Assert Password Value     ${password}

Assert Security Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${security}
    ${current_securiry_value}=    Get Security Value
    should be equal   ${security}    ${current_securiry_value}

Assert Password Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]   ${password}
    ${input_password_is_visible}=    Assert Password Input Is Visible
    Run Keyword Unless      ${input_password_is_visible}==True
    ...                      Return From Keyword
    ${current_password_value}=      Get Element Value     web      ${Input_Password}
    should be equal   ${password}    ${current_password_value}

Restore To Previous Security State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Set Security And Password   ${Previous_Select_Security}     ${Previous_Input_Password}

Set Guest Network Radio State
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${radio_on_off}
    Select From List By Label    web    ${Select_Guest_Turn_On_Off}    ${radio_on_off}
    Save Wireless Config

Verify Guest Network Radio Is on or off
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${radio_on_off}
    ${current_radio_is_on_off}=    Wait Until Keyword Succeeds    5x    3s    get selected list label    web    ${Select_Guest_Turn_On_Off}
    should be equal   ${radio_on_off}     ${current_radio_is_on_off}

Backup Current Guest Network SSID
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    ${element_value} =     Get Element Value     web      ${Input_Guest_SSID}
    Set Test Variable       ${Previous_Guest_Network_SSID}    ${element_value}

Verify Guest Network SSID Value
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${guest_network_ssid}
    ${current_guest_network_ssid_value}=      Get Element Value     web      ${Input_Guest_SSID}
    should be equal   ${guest_network_ssid}     ${current_guest_network_ssid_value}

Restore Guest Network SSID
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    Set Guest Network SSID    ${previous_guest_network_ssid}


Turn On Guest Network and Set Guest Network SSID
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${guest_network_ssid}
    Select From List By Label    web    ${Select_Guest_Turn_On_Off}    on
    input text    web    ${Input_Guest_SSID}    ${guest_network_ssid}
    Save Wireless Config

Assert Password Input Is Visible
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    ${security_value}=      Get Security Value
    ${is_visible}=  run keyword and return status   should not be equal     ${security_value}       Open
    [Return]    ${is_visible}

Set Guest Network SSID
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    [Arguments]     ${guest_network_ssid}
    input text    web    ${Input_Guest_SSID}    ${guest_network_ssid}
    Save Wireless Config
#

Save Wireless Config
    [Documentation]
    [Tags]   @AUTHOR=Johnny_Peng
    cpe click       web    ${Button_SAVE}
    kw_Common.Wait Until Config Has Applied Completely

Config Wireless Home Network
    [Arguments]    ${browser}    ${ssid}=${g_dut_home_ssid}    ${Security}=Open    ${Hidden}=no    ${password}=${g_dut_repeater_ssid_pw}
    [Documentation]    Config Wireless Home Network
    [Tags]    @AUTHOR=Hans_Sun

    # Input home SSID Name
    Input Text    ${browser}    ${Input_SSID}    ${ssid}

    # Select Security type
    Run Keyword If    '${Security}'=='Open'    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_label    ${browser}    ${Select_Security}    ${Security}
    ...    ELSE    run keywords    select_from_list_by_label    ${browser}    ${Select_Security}    ${Security}
    ...    AND    Input Text    ${browser}    ${Input_Password}    ${password}

    # Hidden SSID
    Run Keyword If    '${Hidden}'=='no'    Unselect checkbox    ${browser}    ${Checkbox_Hidden}
    ...    ELSE    Select Checkbox    ${browser}    ${Checkbox_Hidden}

    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Config Wireless Guest Network
    [Arguments]    ${browser}    ${radio}=off    ${ssid}=${g_dut_guest_ssid}
    [Documentation]    Config Wireless Home Network
    [Tags]    @AUTHOR=Hans_Sun

    # Go to Wireless setting page
    Wait Until Keyword Succeeds    3x    2s    click links    ${browser}    Networking  Wireless

    # Select Security type
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_label    ${browser}    ${Select_Radio}    ${radio}

    # Input home SSID Name
    Input Text    ${browser}    ${Input_GuestSSID}    ${ssid}

    Wait Until Keyword Succeeds    3x    2s    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Recover Wireless Page Settings
    [Arguments]
    [Documentation]    Recover Wireless Page Settings
    [Tags]    @AUTHOR=Hans_Sun
    go to page    web    http://192.168.66.1/cgi-bin/luci//admin/network/wifi
    Input Text    web    ${Input_SSID}    ${g_dut_home_ssid}
    select_from_list_by_label    web    ${Select_Security}    Open
    Unselect checkbox    web    ${Checkbox_Hidden}
    select_from_list_by_label    web    ${Select_Radio}    off
    Input Text    web    ${Input_GuestSSID}    ${g_dut_guest_ssid}
    cpe click    web    ${Button_Save}
    Wait Until Config Has Applied Completely

Verify Wifi Client On Wireless Status GUI
    [Arguments]    ${locator}    ${value}
    [Documentation]    Connect to DUT without security key
    [Tags]    @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview
    ${result}=    Get Element Text    web    ${locator}
    log    ${result}
    Should Contain    ${result}    ${value}

Retry to Check DHCP Leases
    [Tags]   @AUTHOR=Hans_Sun
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo killall dhclient
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S sudo dhclient ${DEVICES.wifi_client.int} &
    sleep    5
    Reload Page    web
    sleep    1
    ${result}=    Get Element Text    web    ${Lease_status_table}
    log    ${result}
    Should Contain    ${result}    ${DEVICES.wifi_client.hostname}

Get Wifi Client DHCP IP Value
    [Tags]   @AUTHOR=Hans_Sun
    ${result}=    cli    wifi_client    ifconfig wlan0
    ${IP} =    Get Regexp Matches    ${result}    192.168.\\d+.\\d+
    log    ${IP}
    Should Contain    ${IP}[0]    192.168
    [Return]    @{IP}[0]