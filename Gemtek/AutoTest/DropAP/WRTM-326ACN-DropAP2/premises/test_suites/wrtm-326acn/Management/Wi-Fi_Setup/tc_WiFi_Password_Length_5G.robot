*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi_Setup    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${8byte_pwd}    12345678
${63byte_pwd}    012345678901234567890123456789012345678901234567890123456789AAA
${64byte_pwd}    012345678901234567890123456789012345678901234567890123456789AAAB
${63byte_ascii_to_64byte_hex}    012345678901234567890123456789012345678901234567890123456789abc   #hex with myvita_5G_test1: 21c3f426260eef48838656790131c2cb0448a9fb3e1491480acdb997e3617155
${64byte_hex_only_pwd_from_63byte_ascii}    21c3f426260eef48838656790131c2cb0448a9fb3e1491480acdb997e3617155
${64byte_hex_ascii_pwd}   012345678901234567890123456789012345678901234567890123456789abc!
${password_box}    Password_5g

${5G_ssid}    myvita_5G_test1
${security_type}    wpa2-psk-mixed
${security_key}    1234abcd

*** Test Cases ***
tc_WiFi_Password_Length_5G
    [Documentation]    1. "Wi-Fi Password" shuld be accept 8 ~63 characters. 2. NB and HA Device should setup the connection.
    [Tags]    @tcid=WRTM-326ACN-110    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Click Management -> WiFi Setup.
    Verify "Wi-Fi Password" shuld accept 8 characters. NB can connect to HA Devcie
    Verify "Wi-Fi Password" shuld accept 63 characters. NB can connect to HA Devcie
    Verify "Wi-Fi Password" shuld not accept 64 with ascii characters.
    Verify "Wi-Fi Password" shuld accept 64 hex characters.
    

*** Keywords ***
Click Management -> WiFi Setup.
    [Arguments]
    [Documentation]    Test Step

    # Go to device setting page
    Go To Page    web    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    
Verify "Wi-Fi Password" shuld accept 8 characters. NB can connect to HA Devcie
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    Config 5G Wireless    web    on    ${5G_ssid}    0    ${security_type}    ${8byte_pwd}
    
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${password_box}
    log    ${val}
    Should Match    ${val}    ${8byte_pwd}
    
    #NB can connect to HA Devcie
    
    Wait Until Keyword Succeeds    5x    3s    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${5G_ssid}  ${8byte_pwd}  ${DEVICES.wifi_client.int}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}
       
Verify "Wi-Fi Password" shuld accept 63 characters. NB can connect to HA Devcie
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    Config 5G Wireless    web    on    ${5G_ssid}    0    ${security_type}    ${63byte_pwd}
    
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${password_box}
    log    ${val}
    Should Match    ${val}    ${63byte_pwd}
    
    #NB can connect to HA Devcie
    
    Wait Until Keyword Succeeds    5x    3s    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${5G_ssid}  ${63byte_pwd}  ${DEVICES.wifi_client.int}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}

Verify "Wi-Fi Password" shuld not accept 64 with ascii characters.
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    Config 5G Wireless    web    on    ${5G_ssid}    0    ${security_type}    ${64byte_hex_ascii_pwd}
    
    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    id=msg_pwd_1@style
    log    ${status}
    # Warning message should be shown, so style should not be none
    Should Not Contain    ${status}    none

Verify "Wi-Fi Password" shuld accept 64 hex characters.
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    Config 5G Wireless    web    on    ${5G_ssid}    0    ${security_type}    ${64byte_hex_only_pwd_from_63byte_ascii}
    
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${password_box}
    log    ${val}
    Should Match    ${val}    ${64byte_hex_only_pwd_from_63byte_ascii}
    
    #NB can connect to HA Devcie
    
    Wait Until Keyword Succeeds    5x    3s    Login Linux Wifi Client To Connect To DUT With Matched Security Key
    ...    wifi_client  ${5G_ssid}  ${63byte_ascii_to_64byte_hex}  ${DEVICES.wifi_client.int}  ${DEVICES.wifi_client.assign_static_ip}  ${g_dut_gw}


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

    Config 5G Wireless    web    on




*** comment ***
2017-09-09    Gemtek_Thomas_Chen
1. Add new script
