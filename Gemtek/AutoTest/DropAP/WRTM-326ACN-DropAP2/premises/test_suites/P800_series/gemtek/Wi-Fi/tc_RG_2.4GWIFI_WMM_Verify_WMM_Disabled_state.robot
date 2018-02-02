*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Gavin_Chang    stable

*** Variables ***

*** Test Cases ***
tc_RG_2.4GWIFI_WMM_Verify_WMM_Disabled_state
    [Documentation]    tc_RG_2.4GWIFI_WMM_Verify_WMM_Disabled_state
    ...   1. Check WMM state and WMM Power. Save state on the page.
    ...   2. Run  wlctl wme , the result should be 0. 0=off, 1=on, -1=auto

    [Tags]    @TCID=STP_DD-TC-10886    @globalid=1526054    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Gavin_Chang
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page, click WMM
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    WMM

    #Enable WMM state
    Wait Until Element Is Visible    web    name=wmm
    select radio button    web    wmm    0
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    radio_button_should_be_set_to    web    wmm    0

    #Check WMM state is disabled by command wlctl wme, the result should be 0
    Wait Until Keyword Succeeds    5x    3s    Check WMM State Is Disabled

*** Keywords ***
Check WMM State Is Disabled
    [Arguments]
    [Documentation]    Check WMM state is disabled by command wlctl wme, the result should be 0
    [Tags]    @AUTHOR=Gemtek_Gavin_Chang

    ${wmm_state_result} =    cli    n1    wlctl wme
    log    ${wmm_state_result}
    Should Contain     ${wmm_state_result}    0

*** comment ***
