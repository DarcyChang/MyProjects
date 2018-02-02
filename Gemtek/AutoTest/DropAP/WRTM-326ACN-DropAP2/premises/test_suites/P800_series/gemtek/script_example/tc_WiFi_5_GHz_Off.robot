*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Gavin_Chang    norun

*** Variables ***
${844fb_device}    n1
${844fb_gui_session}    web

*** Keywords ***

*** Test Cases ***
tc_WiFi_5_GHz_Off
    [Documentation]    tc_WiFi_5_GHz_Off
    ...    Verify if the WiFi 5 GHz LED stay in OFF state when WiFi 5 GHz is disabled.
    [Tags]    @TCID=PREMS-TC-7892   @globalid= 1597614LED844F   @DUT=844FB   @DUT=844F
    [Timeout]
    #Login Web GUI
    login ont    ${844fb_gui_session}    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 5 GHz Control Page
    click links    ${844fb_gui_session}    Wireless
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    click links    ${844fb_gui_session}    5G Network
    #Disable WiFi 5 GHz
    Wait Until Element Is Visible    ${844fb_gui_session}    name=wireless_onoff
    select radio button    ${844fb_gui_session}    wireless_onoff    0
    Wait Until Element Is Visible    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    ${844fb_gui_session}    wireless_onoff    0
    #Check led 3 behavior is 0
    cli    n1    sh
    ${result} =   cli    n1     wl -i wl1 ledbh 3
    log    ${result}
    Should Contain    ${result}    led 3 behavior 8

*** comment ***
