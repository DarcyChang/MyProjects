*** Settings ***
Resource    base.robot

*** Variables ***
${expand_btn}    com.dropap.dropap:id/btnExpand
${setting_btn}    com.dropap.dropap:id/btnSettings
${devicelist_btn}    com.dropap.dropap:id/btnDeviceList
${zap_btn}    com.dropap.dropap:id/btnZAPSetting
${zap_switch}    com.dropap.dropap:id/btnGuest
${zap_save}    com.dropap.dropap:id/btnSave
${zap_ssid}    com.dropap.dropap:id/etSsidName
${confirm}    com.dropap.dropap:id/btnPositive
${cancel}    com.dropap.dropap:id/btnNegative
${device_list_remove_offline}    com.dropap.dropap:id/btnRemoveOfflineDevice
${zap_title}    com.dropap.dropap:id/tvGuest
${device_list_title}    com.dropap.dropap:id/tvTitle
${authorization_code}    com.dropap.dropap:id/authorityBtn
${master_code}    com.dropap.dropap:id/etEnterMasterCode
${authorization_save}    com.dropap.dropap:id/btnSave
${wireless_setting}    com.dropap.dropap:id/wirelessSettingBtn
${wireless_ssid}    com.dropap.dropap:id/etWifiName
${wireless_hide_ssid}    com.dropap.dropap:id/btnHideSsid
${wireless_password}    com.dropap.dropap:id/etWifiPassword
${wireless_ok}    com.dropap.dropap:id/btnOk

${internet_connection}    com.dropap.dropap:id/internetConnectionBtn
${internet_dhcp}    com.dropap.dropap:id/radioUserDhcp
${internet_static_ip}    com.dropap.dropap:id/radioUseStaticIp
${static_ip}    com.dropap.dropap:id/ipEditText
${static_mask}    com.dropap.dropap:id/mskEditText
${static_gateway}    com.dropap.dropap:id/gwEditText
${static_primary_dns}    com.dropap.dropap:id/dns1EditText
${static_secondary_dns}    com.dropap.dropap:id/dns2EditText
${internet_pppoe}    com.dropap.dropap:id/radioUsePppoe
${pppoe_username}    com.dropap.dropap:id/pppoeUserNameEditText
${pppoe_password}    com.dropap.dropap:id/pppoeUserPwdEditText
${internet_apply}    com.dropap.dropap:id/signInBtn
${internet_next}    com.dropap.dropap:id/btnNext
${internet_ok}    com.dropap.dropap:id/okBtn
${setup_success_msg}    com.dropap.dropap:id/tvSetupSuccess
${Setup_Failed_ok}    com.dropap.dropap:id/btnPositive
${setup_failed_msg}    com.dropap.dropap:id/tvSetupFailed

${timezone}    com.dropap.dropap:id/timezoneBtn
${current_zone}    com.dropap.dropap:id/currentZoneSubText
${anti_phishing}    com.dropap.dropap:id/antiPhishingBtn
${anti_phishing_switch}    com.dropap.dropap:id/ivAntiPhishingSwitch
${anti_phishing_Off}    com.dropap.dropap:id/ivAntiOff
${anti_phishing_On}    com.dropap.dropap:id/ivAntiOn

${performance_control}    com.dropap.dropap:id/performanceBtn
${performance_control_switch}    com.dropap.dropap:id/ivPerformanceSwitch

${speed_test}    com.dropap.dropap:id/speedTestBtn
${speed_test_now}    com.dropap.dropap:id/btnTestNow
${speed_test_retest}    com.dropap.dropap:id/btnRestart
${speed_test_show_value}    com.dropap.dropap:id/tvShowValue
${speed_test_download_value}    com.dropap.dropap:id/tvDownloadValue
${speed_test_upload_value}    com.dropap.dropap:id/tvUploadValue
${speed_test_ping_value}    com.dropap.dropap:id/tvPingValue

${system_info}    com.dropap.dropap:id/systemInfoBtn
${ip_address}    com.dropap.dropap:id/tvIPaddress
${mac_address}    com.dropap.dropap:id/tvMACaddress
${connection_time}    com.dropap.dropap:id/tvGuestNetwork
${system_uptime}    com.dropap.dropap:id/tvSystemUpTime
${serial_number}    com.dropap.dropap:id/tvSerialNum
${hw_version}    com.dropap.dropap:id/tvHWVersion
${fw_version_info}    com.dropap.dropap:id/tvFWVersion

${restart_dropap}    com.dropap.dropap:id/resstartDropAPBtn
${update}    com.dropap.dropap:id/upgradeDropAPBtn
${update_pop_message}    com.dropap.dropap:id/tvMessage
${remove_dropap}    com.dropap.dropap:id/deleteRouterBtn
${remove_info}    com.dropap.dropap:id/content
${default_cancel}    com.dropap.dropap:id/buttonDefaultNegative
${default_ok}    com.dropap.dropap:id/buttonDefaultPositive

${reset_to_default}    com.dropap.dropap:id/resetBtn

${wireless_security}    com.dropap.dropap:id/btnWirelessSecurity
${frequency_bands}    com.dropap.dropap:id/btnFrequencyBands
${ipv6_btn}    com.dropap.dropap:id/btnEnableIPv6
${ipv6_ok_btn}    com.dropap.dropap:id/nextBtn

*** Keywords ***
touch Expand Shortcut Button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${expand_btn}
    sleep    1s

wait title show
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${device_list_title}    timeout=30

touch Device Settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Expand Shortcut Button
    Click Element    ${setting_btn}
    wait title show

touch Device list
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Expand Shortcut button
    Click Element    ${devicelist_btn}
    wait title show

touch ZAP setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Expand Shortcut button
    Click Element    ${zap_btn}
    wait title show

verify Device Settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${setting_btn}

verify Device list
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${devicelist_btn}

verify ZAP setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${zap_btn}

verify ZAP page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${zap_switch}

touch ZAP Switch
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${zap_switch}

touch ZAP Save
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${zap_save}

touch confirm
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${confirm}

Press ZAP button via command
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    cli    app-vm    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    cli    dut1    /etc/btnd/wps_click.sh
    sleep    20s
    wait main screen

Remove Offline Device From List
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${device_list_remove_offline}

verify Authorization Code
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${authorization_code}

verify Wireless Setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${wireless_setting}

verify Internet Connection
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${internet_connection}

verify Timezone
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${timezone}

verify Timezone page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${current_zone}

verify Anti-Phishing
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${anti_phishing}

verify Performance Control
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${performance_control}

verify Speed Test
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${speed_test}

verify System Info
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${system_info}

verify items in System Info
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang

    Page Should Contain Element    ${ip_address}
    Page Should Contain Element    ${mac_address}
    Page Should Contain Element    ${connection_time}
    Page Should Contain Element    ${system_uptime}
    Page Should Contain Element    ${serial_number}
    Page Should Contain Element    ${hw_version}
    Page Should Contain Element    ${fw_version_info}

verify Restart DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Page Should Contain Element    ${restart_dropap}

verify Upgrade
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Page Should Contain Element    ${update}

verify upgrade pop message
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${result}    Get Text    ${update_pop_message}
    Should Contain    ${result}    ${upgrade_message}

verify Remove DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Page Should Contain Element    ${remove_dropap}

verify Reset to Default
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Page Should Contain Element    ${reset_to_default}

touch Authorization Code
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${authorization_code}

touch Wireless Setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${wireless_setting}
    wait title show

touch Internet Connection
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${internet_connection}

touch Timezone
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${timezone}

touch Anti-Phishing
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${anti_phishing}

touch Performance Control
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${performance_control}

touch Speed Test
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${speed_test}

touch Speed Test Now
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${speed_test_now}

touch Speed Test Retest
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${speed_test_retest}

touch System Info
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${system_info}

touch Restart DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Click Element    ${restart_dropap}

touch Upgrade
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Click Element    ${update}

touch Remove DropAP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Click Element    ${remove_dropap}

touch Remove OK button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${default_ok}

touch Reset to Default
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Up
    Click Element    ${reset_to_default}

input wireless password
    [Documentation]
    [Arguments]    ${wifi_pwd}
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${wireless_password}    ${wifi_pwd}


wait speed test web
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${speed_test_now}
    ${speed_test_value}    Get Text    ${speed_test_show_value}
    log    ${speed_test_value}
    Set Global Variable     ${original_speed_test_value}     ${speed_test_value}

wait speed test retest web
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait until keyword succeeds    2x    3s    Wait Until Page Contains Element    ${speed_test_retest}    timeout=50

Change Wireless SSID name
    [Documentation]
    [Arguments]    ${input_ssid}
    [Tags]   @AUTHOR=Gavin_Chang
    Clear Text    ${wireless_ssid}
    Input Text    ${wireless_ssid}    ${input_ssid}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard

Change ZAP SSID name
    [Documentation]
    [Arguments]    ${input_ssid}
    [Tags]   @AUTHOR=Gavin_Chang
    Clear Text    ${zap_ssid}
    Input Text    ${zap_ssid}    ${input_ssid}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard

touch wireless ok
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${wireless_ok}

wait wireless ok
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${wireless_ok}

Trigger Device List
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    cli    app_lanhost    echo '${DEVICES.app_lanhost.password}' | sudo -S dhclient -r ${DEVICES.app_lanhost.interface}
    cli    app_lanhost    echo '${DEVICES.app_lanhost.password}' | sudo -S dhclient ${DEVICES.app_lanhost.interface}
    cli    app_lanhost    wget youtube.com
    touch Device list
    Swipe By Percent    50    30    50   70
    sleep    3s
    touch left

touch Hide SSID
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${wireless_hide_ssid}

Change Frequency Bands
    [Documentation]
    [Arguments]    ${frequency}
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${frequency_bands}
    Click Text    ${frequency}

Change Security
    [Documentation]
    [Arguments]    ${security}    ${wifi_password}=1234abcd
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${wireless_security}
    Click Text    ${security}
    return from keyword if    '${security}' == 'Open'
    Input Text    ${wireless_password}    ${wifi_password}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard

touch IPv6 Switch
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${ipv6_btn}
    Click Element    ${confirm}
    Wait Until Page Contains Element    ${ipv6_ok_btn}    timeout=30
    Click Element    ${ipv6_ok_btn}
    wait main screen

Select Static IP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${internet_static_ip}

Select PPPoE
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${internet_pppoe}

Config Static IP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${static_ip}    ${g_dut_static_ipaddr}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_mask}    ${g_dut_static_netmask}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_gateway}    ${g_dut_static_gateway}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Swipe To Up
    Input Text    ${static_primary_dns}    ${g_dut_static_dns1}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_secondary_dns}    ${g_dut_DNS_from_company}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Click Element    ${internet_apply}
    Wait Until Page Contains Element    ${internet_ok}    timeout=50
    Click Element    ${internet_ok}
    wait main screen

Config Wrong Static IP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${static_ip}    ${wrong_static_ipaddr}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_mask}    ${wrong_static_netmask}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_gateway}    ${wrong_static_gateway}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Swipe To Up
    Input Text    ${static_primary_dns}    ${wrong_static_dns1}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${static_secondary_dns}    ${wrong_static_dns2}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Click Element    ${internet_apply}
    Wait Until Page Contains Element    ${Setup_Failed_ok}    timeout=50
    Page Should Contain Element    ${setup_failed_msg}
    Click Element    ${Setup_Failed_ok}
    wait main screen

Config PPPoE
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${pppoe_username}    ${g_dut_pppoe_username}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${pppoe_password}    ${g_dut_pppoe_password}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Click Element    ${internet_apply}
    Wait Until Page Contains Element    ${internet_ok}    timeout=50
    Page Should Contain Element    ${setup_success_msg}
    Click Element    ${internet_ok}
    wait main screen

Config Wrong PPPoE
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${pppoe_username}    ${g_dut_invalid_pppoe_username}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Input Text    ${pppoe_password}    ${g_dut_invalid_pppoe_password}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Click Element    ${internet_apply}
    Wait Until Page Contains Element    ${Setup_Failed_ok}    timeout=50
    Page Should Contain Element    ${setup_failed_msg}
    Click Element    ${Setup_Failed_ok}
    wait main screen

Config DHCP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${internet_dhcp}
    Click Element    ${internet_apply}
    Wait Until Page Contains Element    ${internet_ok}    timeout=50
    Click Element    ${internet_ok}
    wait main screen

Verify Internet Type via DUT
    [Documentation]
    [Arguments]    ${interfce}    ${address}
    [Tags]   @AUTHOR=Gavin_Chang
    cli    app-vm    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ${result}    cli    dut1    ifconfig ${interfce}
    Should Contain    ${result}    ${address}

Check the original ZAP is disable
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Close APP
    Launch APP
    Sign In
    wait main screen
    touch ZAP setting
    ${status}    run keyword and return status    Element Attribute Should Match    ${zap_switch}    checked    false
    run keyword if    ${status}==False
    ...    Run keywords
    ...    touch ZAP Switch
    ...    touch ZAP Save
    ...    touch confirm
    ...    wait main screen
    Close APP

*** comment ***
2018-01-17 Gavin_Chang
1. Add ZAP seting teardown to make sure the precondition is correct.
2. Add appium keyword to prevent wait command over 60 seconds during connect to ZAP newtork.

2017-12-22 Gavin_Chang
1. Hide keyboard to ensure the element is clickable
2. Delete the wireless security and frequency coordinates keyword

2017-12-5     Leo_Li
Add New Keywords

2017-11-10     Leo_Li
Init basic AP common keyword
