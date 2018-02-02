*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_050_MainScreen_Extend_3_shortcut_buttons
    [Documentation]  tc_AndroidAPP_050_MainScreen_Extend_3_shortcut_buttons
    ...    1. Launch the app then into main screen
    ...    2. Click the button at bottom-right
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-223    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Click the button at bottom-right
    Check the status

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Click the button at bottom-right
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Expand Shortcut Button

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify Device Settings
    verify Device list
    verify ZAP setting

*** comment ***
2017-12-15 Gavin_Chang
1. Replace coordinates with element id

2017-11-15    Gavin_Chang
Init the script
