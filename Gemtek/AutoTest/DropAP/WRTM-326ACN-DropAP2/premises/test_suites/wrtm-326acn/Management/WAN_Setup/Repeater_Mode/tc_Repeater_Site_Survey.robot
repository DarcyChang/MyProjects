*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_Repeater    @AUTHOR=Gemtek_Thomas_Chen

*** Variables ***

*** Test Cases ***
tc_Repeater_Site_Survey
    [Documentation]    Change wan to repeater mode and change router mode back
    [Tags]   @tcid=WRTM-326ACN-66    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]
    
    Login Web GUI
    Using Web to login. Click "Management" -> "WAN Setup". Choose "Operation Mode" -> Repeater mdoe.
    Click "Site Survey". It will all WiFi AP information.
    
    
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
    
    Check Site Survey Function   web    
    

Check Site Survey Function
    [Arguments]    ${browser}       
    [Documentation]    Check Site Survey
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_wifi.html
    sleep    3s
    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    2s
    
    # Click on Repearter mode tab
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="tab_2"]/a
    
    
    # Wait until reflash icon stop
    Wait Until Keyword Succeeds    10x    2s    page should contain element    ${browser}    xpath=//*[@src="img/refresh_green_24.png"]
    
    #Select ssid and input password
    ${list_val}=    Get List Items    ${browser}    xpath=//*[@id="wifi_relay_auto_ssid"]
    
    log    ${list_val}
    log to console    ${list_val}
    
    Should Not Be Empty    ${list_val}
    
Click "Site Survey". It will all WiFi AP information.
    [Arguments]
    [Documentation]    Test Step
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    log    Already check in the last step

*** comment ***
2017-09-08     Gemtek_Thomas_Chen
Init the script
