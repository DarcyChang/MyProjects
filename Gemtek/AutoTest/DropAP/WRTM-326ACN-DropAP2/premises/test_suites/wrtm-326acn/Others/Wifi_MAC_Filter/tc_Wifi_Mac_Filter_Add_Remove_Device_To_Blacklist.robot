*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=MAC_FILTER    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup
*** Variables ***
${2.4G_ssid}    myvita_2.4G_test1
${security_type}    wpa2-psk-mixed
${security_key}    1234abcd

*** Test Cases ***
tc_Wifi_Mac_Filter_Add_Remove_Device_To_Blacklist
    [Documentation]    NB Connect to HA device with WPA/WPA2 AES authentication
    [Tags]    @tcid=WRTM-326ACN-148    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Configure Wifi Setting.
    Add Device MAC to The Blacklist.
    This Device can not connect to HA Device.
    Remove This Device From Blacklist.
    This Device can connect to HA Device.


*** Keywords ***
Configure Wifi Setting.
    [Arguments]
    [Documentation]    Test Step
    
    #Restore Default and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    Config 2.4G Wireless    web    on    ${2.4G_ssid}    0    ${security_type}    ${security_key}
    
Add Device MAC to The Blacklist.
    [Arguments]
    [Documentation]    Test Step
    
    Config MAC Filter Switch Off and Clear All    web
    Config MAC Filter Switch On and Add MAC    web    ${DEVICES.wifi_client.int_2_4g_mac}    on    block
    
This Device can not connect to HA Device.
    [Arguments]
    [Documentation]    Test Step

    ${wifi_val}=    Run Keyword And Return Status    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${2.4G_ssid}  ${security_key}  ${DEVICES.wifi_client.int_2_4g}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}
    
    Should Not Be True    ${wifi_val}

Remove This Device From Blacklist.
    [Arguments]
    [Documentation]    Test Step
    
    Config MAC Filter Switch Off and Clear All    web
    
This Device can connect to HA Device.
    [Arguments]
    [Documentation]    Test Step
    
    ${wifi_val}=    Run Keyword And Return Status    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${2.4G_ssid}  ${security_key}  ${DEVICES.wifi_client.int_2_4g}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}
    
    Should Be True    ${wifi_val}
    
Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]

    Login Web GUI

Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]

    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}


Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]
    
    Config MAC Filter Switch Off and Clear All    web
    Config 2.4G Wireless    web    on
    cli    wifi_client    echo ${DEVICES.wifi_client.password} | sudo -S killall wpa_supplicant


*** comment ***
2017-09-09    Gemtek_Thomas_Chen
1. Add new script
