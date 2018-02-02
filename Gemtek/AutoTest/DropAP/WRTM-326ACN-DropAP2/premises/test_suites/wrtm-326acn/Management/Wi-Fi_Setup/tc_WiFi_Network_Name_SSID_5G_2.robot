*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi_Setup    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup
*** Variables ***
${1byte_ssid}    A
${ascii_ssid}    `~!@#$%^&*()-_=+[]{}'";:/?.>,<\|
${32byte_ssid}    000000000011111111112222222222aA
${33byte_ssid}    000000000011111111112222222222aAa
${ssid}    ssid_5g

*** Test Cases ***
tc_WiFi_Network_Name_SSID_5G_2
    [Documentation]    Check "5G WiFi-Network Name(SSID)" default name is myvita
    [Tags]    @tcid=WRTM-326ACN-105    @DUT=wrtm-326acn    @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Click Management -> WiFi Setup.
    Verify "SSID" change all ASCII character. 
    Verify SSID minum character is 1 byte.
    Verify SSID maximum character is 32 byte.


*** Keywords ***
Click Management -> WiFi Setup.
    [Arguments]
    [Documentation]    Test Step

    # Go to device setting page
    Go To Page    web    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
Verify "SSID" change all ASCII character. 
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    input text    web    ${ssid}    ${ascii_ssid}
    cpe click    web    id=save
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${ssid}
    log    ${val}
    Should Match    ${val}    ${ascii_ssid}
    
Verify SSID minum character is 1 byte.
    [Arguments]
    [Documentation]    Test Step
    
    # Config SSID
    input text    web    ${ssid}    ${1byte_ssid}
    cpe click    web    id=save
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${ssid}
    log    ${val}
    Should Match    ${val}    ${1byte_ssid}
    
Verify SSID maximum character is 32 byte.
    [Arguments]
    [Documentation]    Test Step

    input text    web    ${ssid}    ${32byte_ssid}
    cpe click    web    id=save
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${ssid}
    log    ${val}
    Should Match    ${val}    ${32byte_ssid}
    
    input text    web    ${ssid}    ${33byte_ssid}
    cpe click    web    id=save
    ${val} =    Wait Until Keyword Succeeds    5x    3s    get element value    web    id=${ssid}
    log    ${val}
    Should Match    ${val}    ${32byte_ssid}


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
