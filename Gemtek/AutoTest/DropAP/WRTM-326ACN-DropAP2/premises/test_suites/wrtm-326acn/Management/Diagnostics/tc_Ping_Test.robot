*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=Diagnostics    @AUTHOR=Gemtek_Thomas_Chen   


*** Variables ***


*** Test Cases ***
tc_Ping_Test
    [Documentation]    Ping Test
    [Tags]   @tcid=WRTM-326ACN-84    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Make sure WAN connection is up.
    Input the IP address to Ping Test Input Box, and then click Ping Button and Verify if ICMP reply is received.
    
    
*** Keywords ***
Make sure WAN connection is up.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    Login Web GUI
    Config DHCP WAN    web
    Wait Until Keyword Succeeds    15x    5s    Internet Status Should be Up    web
    
    
Input the IP address to Ping Test Input Box, and then click Ping Button and Verify if ICMP reply is received.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    

    Wait Until Keyword Succeeds    5x    2s    Ping and Check Ping Result
    
Ping and Check Ping Result
    [Arguments]
    [Documentation]    Test Step
    [Tags] 
    
    ${ping_result}=    Ping Host IP by GUI     web    ${DEVICES.cisco.gateway}
    Should Contain    ${ping_result}    0% packet loss
        
   
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}



*** comment ***
2017-09-06     Gemtek_Thomas_Chen
Init the script
