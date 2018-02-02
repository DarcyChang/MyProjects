*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_051_MainScreen_Zap_buttons
    [Documentation]  tc_AndroidAPP_051_MainScreen_Zap_buttons
    ...    1. Launch the app then into main screen
    ...    2. Click the Zap button
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-225    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Click the Zap button
    Check the status


*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Click the Zap button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch ZAP setting

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify ZAP page

*** comment ***
2017-11-15    Gavin_Chang
Init the script
