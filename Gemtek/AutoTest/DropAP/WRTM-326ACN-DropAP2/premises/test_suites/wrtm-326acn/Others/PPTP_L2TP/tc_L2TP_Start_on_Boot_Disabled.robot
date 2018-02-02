*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=L2TP/PPTP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    50
${ppp_username}    test
${ppp_password}    test
${L2TP_TYPE_FULL}    full
${L2TP_START_WHEN_BOOT}    False
${L2TP_FORCE_ENCRYPTION}    False

*** Test Cases ***
tc_L2TP_Start_on_Boot_Disabled
    [Documentation]    Configure L2TP and check status
    [Tags]    @tcid=WRTM-326ACN-154    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Config DHCP WAN and Check Internet Status
    Configure L2TP including server ip, username, password, Select Start on Boot on and save the settings.
    Press "Click" to start the service, then status change "Connected"
    Reload DUT
    Check L2TP Status Should be "Disconnected"

*** Keywords ***
Config DHCP WAN and Check Internet Status
    [Arguments]
    [Documentation]    Test Step

    Wait Until Keyword Succeeds    5x    3s    Config DHCP WAN    web
    Wait Until Keyword Succeeds    10x    5s    Internet Status Should be Up    web
    
Configure L2TP including server ip, username, password, Select Start on Boot on and save the settings.
    [Arguments]
    [Documentation]    Test Step    
    
    Config PPTP_L2TP    web    l2tp    ${DEVICES.cisco.gateway}    ${ppp_username}    ${ppp_password}    ${L2TP_TYPE_FULL}    ${L2TP_START_WHEN_BOOT}    ${L2TP_FORCE_ENCRYPTION}
    
Press "Click" to start the service, then status change "Connected"
    [Arguments]
    [Documentation]    Test Step  
    
    Config PPTP_L2TP Connect    web
    Wait Until Keyword Succeeds    5x    5s    Check PPTP_L2TP Connected    web

Reload DUT
    [Arguments]
    [Documentation]    Test Step  

    Reboot Device and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}    
    
Check L2TP Status Should be "Disconnected"
    [Arguments]
    [Documentation]    Test Step  
    

    Wait Until Keyword Succeeds    5x    5s    Check PPTP_L2TP Disconnected    web

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
    
    Restore WAN Setting
   
    
Restore WAN Setting    
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    
    
    Config PPTP_L2TP    web    l2tp    ${DEVICES.cisco.gateway}    ${ppp_username}    ${ppp_password}    full    False    False
    Config PPTP_L2TP Disconnect    web
    Wait Until Keyword Succeeds    5x    3s    Check PPTP_L2TP Disconnected    web
    Config DHCP WAN and Check Internet     web

    

*** comment ***
2017-09-08     Gemtek_Thomas_Chen
Init the script
