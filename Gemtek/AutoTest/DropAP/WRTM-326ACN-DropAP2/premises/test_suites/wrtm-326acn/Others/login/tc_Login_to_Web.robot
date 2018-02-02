*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=SYSTEM    @AUTHOR=Gemtek_Thomas_Chen

Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${pppoe_username}    test
${pppoe_password}    test
@{Port_Fordward_List}    1  2  3  4  5
${2.4G_ssid}    myvita_2.4G_test
${security_type}    wpa2-psk-mixed
${security_key}    1234abcd

*** Test Cases ***
tc_Login_to_Web_DHCP_Mode
    [Documentation]    Change wan to repeater mode and change router mode back
    [Tags]   @tcid=WRTM-326ACN-121    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login Web GUI
    Check Major Links to See If They Are Available

    
tc_Login_to_Web_Repeater_Mode
    [Documentation]    Change wan to repeater mode and change router mode back
    [Tags]   @tcid=WRTM-326ACN-122    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login Web GUI
    Using Web to login. Click "Management" -> "WAN Setup". Choose "Operation Mode" -> Repeater mdoe.
    Connect to WiFi AP.
    Check Major Links to See If They Are Available
    Switch to Router mode again.
    
    
*** Keywords ***
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
   
Using Web to login. Click "Management" -> "WAN Setup". Choose "Operation Mode" -> Repeater mdoe.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Config Repeater WAN    web    ${g_dut_repeater_ssid}    ${g_dut_repeater_ssid_pw}
    
Connect to WiFi AP.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Wait Until Keyword Succeeds    10x    5s    Internet Status Should be Up    web
    
Check Major Links to See If They Are Available
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    10x    2s    Config PPPoE WAN    web    ${pppoe_username}    ${pppoe_password}
    sleep    5s
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_List}    off
    sleep    5s
    Control Multiple Port Forward Rule Switch    web    ${Port_Fordward_List}    on
    sleep    5s
    Config 2.4G Wireless    web    on    ${2.4G_ssid}    0    ${security_type}    ${security_key}
    Go To Page     web    ${g_dut_gui_url}/main_pannel_sysinfo.html
    
Switch to Router mode again.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    log    In Common Cleanup section will do dhcp mode and check connection
    

Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Restore WAN Setting
    
Restore WAN Setting    
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Wait Until Keyword Succeeds    5x    2s    Config DHCP WAN and Check Internet     web
    

*** comment ***
2017-09-06     Gemtek_Thomas_Chen
Init the script
