*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Gemteks_Gavin_Chang    norun

*** Variables ***
${844fb_gui_session}    web

*** Keywords ***

*** Test Cases ***
tc_WiFi_2_4_GHz_Off
    [Documentation]    tc_WiFi_2_4_GHz_Off
    ...    Verify if the WiFi 2.4 GHz LED stay in OFF state when WiFi 2.4 GHz is disabled.
    [Tags]    @TCID=PREMS-TC-7889   @globalid=1597610LED844F   @DUT=844FB   @DUT=844F
    [Timeout]
    #Login Web GUI
    login ont    ${844fb_gui_session}    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    click links    ${844fb_gui_session}    Wireless
    #Disable WiFi 2.4 GHz
    Wait Until Element Is Visible    ${844fb_gui_session}    name=wireless_onoff
    select radio button    ${844fb_gui_session}    wireless_onoff    0
    Wait Until Element Is Visible    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    cpe click    ${844fb_gui_session}    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    ${844fb_gui_session}    wireless_onoff    0
    #Check led 3 behavior is 0
    cli    n1    sh
    ${result} =   cli    n1     wl -i wl0 ledbh 3
    log    ${result}
    cli    n1    exit
    Should Contain    ${result}    led 3 behavior 8

*** comment ***
