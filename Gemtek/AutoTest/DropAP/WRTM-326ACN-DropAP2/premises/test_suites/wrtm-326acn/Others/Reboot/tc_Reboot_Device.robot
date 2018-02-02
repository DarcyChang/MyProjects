*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=System    @AUTHOR=Gemtek_Thomas_Chen   


*** Variables ***


*** Test Cases ***
tc_Reboot_Device
    [Documentation]    Reboot Device
    [Tags]   @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Configure a LAN PC to be DHCP and attach on LAN side. After LAN PC getting IP information from DUT, access DUT Web Page.
    Press the Restart Router button on Web page.
    Verify the DUT reboot or not.
    
    
*** Keywords ***

Configure a LAN PC to be DHCP and attach on LAN side. After LAN PC getting IP information from DUT, access DUT Web Page.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    Login Web GUI
    
Press the Restart Router button on Web page.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    
    Reboot Device and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    
Verify the DUT reboot or not.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    ${bootup_time}=    Get Element Text    web    xpath=//*[@id="time_strong"]
    log    ${bootup_time}
    ${bootup_time_int}=    Convert To Integer    ${bootup_time}
    log    ${bootup_time_int}
    
    Comment    Boot Up time should be less than 5 minutes
    Should Be True    ${bootup_time_int} < 5
    
   
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}



*** comment ***
2017-08-28     Gemtek_Thomas_Chen
Init the script
