*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_Repeater    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***

*** Test Cases ***
tc_Repeater_Ping_Gateway
    [Documentation]    Change wan to repeater mode and change router mode back
    [Tags]   @tcid=WRTM-326ACN-68    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Restore WAN Setting and Record Gateway IP
    Using Web to login. Click "Management" -> "WAN Setup". Choose "Operation Mode" -> Repeater mdoe.
    Connect to WiFi AP.
    Make Sure Gateway IP Address is Changed
    Ping Gateway IP.
    Switch to Router mode again.
    
*** Keywords ***
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

Switch to Router mode again.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    log    In Common Cleanup section will do dhcp mode and check connection
    
Restore WAN Setting and Record Gateway IP
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Restore WAN Setting 
    ${WAN_GW_IP}=    Get Default Gatway IP    dut1_ssh
    log    ${WAN_GW_IP}
    set global variable    ${DHCP_WAN_GW_IP}    ${WAN_GW_IP}
    
Make Sure Gateway IP Address is Changed
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    ${WAN_GW_IP}=    Wait Until Keyword Succeeds    10x    5s    Get Default Gatway IP    dut1_ssh
    log many    ${WAN_GW_IP}    ${DHCP_WAN_GW_IP}
    should not be equal    ${WAN_GW_IP}    ${DHCP_WAN_GW_IP}

Ping Gateway IP.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    ${WAN_GW_IP}=    Get Default Gatway IP    dut1_ssh
    Wait Until Keyword Succeeds    5x    2s    Ping and Check Ping Result    ${WAN_GW_IP}
    
Ping and Check Ping Result
    [Arguments]    ${dst_ip}
    [Documentation]    Test Step
    [Tags] 
    
    ${ping_result}=    Ping Host IP by GUI     web    ${dst_ip}
    Should Contain    ${ping_result}    0% packet loss


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
    
    Wait Until Keyword Succeeds    5x    2s    Config DHCP WAN and Check Internet     web
    

*** comment ***
2017-09-06     Gemtek_Thomas_Chen
Init the script
