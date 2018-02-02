*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***


*** Test Cases ***
tc_Config_Language_Auto
    [Documentation]  tc_Config_Language_Auto
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Language and Style" Tab
    ...    2. Select Auto on language list and SAVE
    ...    3. Re-login and Verify Gui Page should contain Text "Configure DropAP"'s translation version mapping to current location
    [Tags]   @TCID=WRTM-326ACN-338    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Language and Style" Tab
    Select English on language list and SAVE
    Re-login and Verify Gui Page should contain Text "Configure DropAP"'s translation version mapping to current location

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
    Select Language By Value    auto

Re-login and Verify Gui Page should contain Text "Configure DropAP"'s translation version mapping to current location
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    go to page    web    ${g_dut_gui_url}
    page should contain text    web    Configure DropAP

*** comment ***
2017-11-01     Hans_Sun
Init the script
