*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=System    @AUTHOR=Gemtek_Thomas_Chen



*** Variables ***


*** Test Cases ***
tc_Verify_Reset_Default
    [Documentation]    Reset Device to Default
    [Tags]   @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Restore Device to Default
    Verify Default DHCP WAN and Check Internet
    
    
*** Keywords ***
Restore Device to Default
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    Restore Default and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    
Verify Default DHCP WAN and Check Internet
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    Config DHCP WAN and Check Internet     web
    



*** comment ***
2017-08-28     Gemtek_Thomas_Chen
Init the script
