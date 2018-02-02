*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***

*** Test Cases ***
tc_Security_Administrator_Credentials_Not_Required
    [Documentation]    Verify Login is done with no username or password required.
    ...    1.When web page credentials choose Not Required, then the Login Web UI does not need to input username and password.
    [Tags]   @TCID=STP_DD-TC-10555   @globalid=1506156    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore administrator credentials original setting
    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Check Not Required status by web Page
    Wait Until Keyword Succeeds    10x    3s    select radio button    web    admin_state    0    #Unstable to select radio button one time, so we select twice.
    Wait Until Keyword Succeeds    10x    3s    select radio button    web    admin_state    0
    Wait Until Keyword Succeeds    5x    3s    radio_button_should_be_set_to    web    admin_state    0
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    go_to_page    web    ${g_844fb_gui_url}

*** Keywords ***
Restore administrator credentials original setting
    [Arguments]
    [Documentation]    Restore administrator credentials original setting
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    go_to_page    web    ${g_844fb_gui_url}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Restore Required status by web Page
    Wait Until Keyword Succeeds    10x    3s    select radio button    web    admin_state    1    #Unstable to select radio button one time, so we select twice.
    Wait Until Keyword Succeeds    10x    3s    select radio button    web    admin_state    1
    Wait Until Keyword Succeeds    5x    3s    radio_button_should_be_set_to    web    admin_state    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

*** comment ***