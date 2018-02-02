*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_PPPoE    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***
${pppoe_username}    test
${mismatch_pppoe_password}    mismatch_test


*** Test Cases ***
tc_PPPoE_Connection_Mismatch_Username_and_Password
    [Documentation]    Input right Username and Password of 63 characters. The DUT can connect to PPPoE server.
    [Tags]   @tcid=WRTM-326ACN-42    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    #Reset factory defaults on the DUT.
    Connect a PC on LAN side. Connect a PPPoE Server on WAN side. Configure WAN Internet connection type to be PPPoE mode.
    Input User ID length of 60/61 characters and mismatch Password length of 50/51 characters, try to connect a PPPoE Server.
    Verify DUT should not establish PPPoE session.
    
*** Keywords ***

Reset factory defaults on the DUT.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Restore Default and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}

Connect a PC on LAN side. Connect a PPPoE Server on WAN side. Configure WAN Internet connection type to be PPPoE mode.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Wait Until Keyword Succeeds    5x    2s    Config PPPoE WAN    web    ${pppoe_username}    ${mismatch_pppoe_password}

Input User ID length of 60/61 characters and mismatch Password length of 50/51 characters, try to connect a PPPoE Server.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    log   It's done in the last step.

Verify DUT should not establish PPPoE session.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Internet Status Should be Down    web
    
    
    
    
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
2017-09-07     Gemtek_Thomas_Chen
Init the script
