*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***


*** Test Cases ***
tc_Config_Language_English
    [Documentation]  tc_Config_Language_English
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Language and Style" Tab
    ...    2. Select English on language list and SAVE
    ...    3. Re-login and Verify Gui Page should contain Text "Configure DropAP"
    [Tags]   @TCID=WRTM-326ACN-337    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Language and Style" Tab
    Select English on language list and SAVE
    Re-login and Verify Gui Page should contain Text "Configure DropAP"

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Language and Style" Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Language_tab}

Select English on language list and SAVE
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Select Language By Value    en

Re-login and Verify Gui Page should contain Text "Configure DropAP"
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    go to page    web    ${g_dut_gui_url}
    page should contain text    web    Configure DropAP

*** comment ***
2017-11-01     Hans_Sun
Init the script
