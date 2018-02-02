*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_PPPoE    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup

*** Variables ***
${Traffic_port}    8888
${Traffic_count}    20
${pppoe_username}    test
${pppoe_password}    test


*** Test Cases ***
tc_PPPoE_Connection_Default_Value
    [Documentation]    The default value of username, password, and dns
    [Tags]   @tcid=WRTM-326ACN-27    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    #Reset factory defaults on the DUT.
    Check the WAN PPPoE mode default value if correct.
    
*** Keywords ***

Reset factory defaults on the DUT.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    Restore Default and Check Login    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}
   
    
Check the WAN PPPoE mode default value if correct.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Go To Page     web    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    web    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    15x    2s    cpe click    web    xpath=//*[@id="li_page1"]/a/p
    sleep    10s
    Wait Until Keyword Succeeds    15x    2s    cpe click    web    xpath=//*[@id="tab_0"]/a

    # Config value to pppoe wan

    Wait Until Element Is Visible    web    id=save_tab1
    
    ${get_val}=    Get Element Value    web    xpath=//*[@id="pppoe_username"]
    log    ${get_val}
    Should Be Empty    ${get_val}
    
    ${get_val}=    Get Element Value    web    xpath=//*[@id="pppoe_Password"]
    log    ${get_val}
    Should Be Empty    ${get_val}
    
    Checkbox Should Not Be Selected    web    xpath=//*[@id="wlan_ppoe_custom_dns"]

    
    
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

   


*** comment ***
2017-09-09     Gemtek_Thomas_Chen
Init the script
