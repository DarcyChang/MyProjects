*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=System    @AUTHOR=Gemtek_Thomas_Chen   


*** Variables ***


*** Test Cases ***
tc_Firmware_Upgrade
    [Documentation]    Upgrade firmware from ~/tmp_fw folder
    [Tags]   @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Configure a LAN PC1 to be DHCP and attach on LAN side. After LAN PC getting IP information from DUT, access DUT Web Page.
    Put firmware at the LAN PC and update firmware via Upgrade Firmware Page. Reboot DUT automatically.
    Ensure the LAN PC1 can obtain IP and login to GUI.

tc_Firmware_Version
    [Documentation]    Check Firmware Version After Firmware Upgrade
    [Tags]   @FEATURE=System    @tcid=WRTM-326ACN-21    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Check Status Page of Firmware version is correctly.
    
    
    
*** Keywords ***
Configure a LAN PC1 to be DHCP and attach on LAN side. After LAN PC getting IP information from DUT, access DUT Web Page.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    
Put firmware at the LAN PC and update firmware via Upgrade Firmware Page. Reboot DUT automatically.
    [Arguments]
    [Documentation]    Test Step
    [Tags]
    
    ${FW_FILE_FULL_PATH}=    Check Firmware is Available and Get Full Path File Name    ${g_fw_folder}
    log    ${FW_FILE_FULL_PATH}
    Upgrade Firmware via GUI    web    ${FW_FILE_FULL_PATH}
    #Sleep    30s
    
Ensure the LAN PC1 can obtain IP and login to GUI.
    [Arguments]
    [Documentation]    Test Step
    [Tags]
    
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

Check Status Page of Firmware version is correctly.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    
    
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
    ${FW_VERSION_FROM_GUI}=    Get Firmware Version    web
    
    ${FW_VERSION_FROM_FW_FILE}=    Check Firmware is Available and Get Full Path File Name    ${g_fw_folder}
    log    ${FW_VERSION_FROM_FW_FILE}
    ${FW_VERSION_FROM_FW_FILE}=    Fetch From right    ${FW_VERSION_FROM_FW_FILE}    firmware-
    log    ${FW_VERSION_FROM_FW_FILE}
    ${FW_VERSION_FROM_FW_FILE}=    Fetch From left    ${FW_VERSION_FROM_FW_FILE}    .img
    log    ${FW_VERSION_FROM_FW_FILE}
    
    Should Match    ${FW_VERSION_FROM_GUI}    ${FW_VERSION_FROM_FW_FILE}
    
*** comment ***
2017-08-28     Gemtek_Thomas_Chen
Init the script
