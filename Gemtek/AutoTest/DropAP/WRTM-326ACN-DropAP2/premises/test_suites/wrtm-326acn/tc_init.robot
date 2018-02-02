*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=System    @AUTHOR=Gemtek_Thomas_Chen   


*** Variables ***
${FW_PATH}    /home/vagrant/tmp_fw

*** Test Cases ***
tc_init
    [Documentation]    Check Firmware Version After Firmware Upgrade
    [Tags]   @FEATURE=System    @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Check Status Page of Firmware version and output to FW_VERSION_FROM_GUI file.

*** Keywords ***
Check Status Page of Firmware version and output to FW_VERSION_FROM_GUI file.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    ${FW_VERSION_FROM_GUI}=    Get Firmware Version    web
    log to console    ${FW_VERSION_FROM_GUI}

 
*** comment ***
2017-08-28     Gemtek_Thomas_Chen
Init the script
