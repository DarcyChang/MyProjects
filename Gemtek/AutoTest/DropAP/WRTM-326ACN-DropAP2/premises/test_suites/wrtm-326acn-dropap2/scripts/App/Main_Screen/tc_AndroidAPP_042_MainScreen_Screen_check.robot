*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_042_MainScreen_Screen_check
    [Documentation]  tc_AndroidAPP_042_MainScreen_Screen_check
    ...    1. Launch the app then into main screen
    ...    2. Check all of option on main screen.
    [Tags]   @TCID=WRTM-326ACN-215    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Check all of option on main screen

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Check all of option on main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify account info menu
    verify main screen device name
    verify notifications info menu
    verify gps
    verify family member
    verify today
    verify report

*** comment ***
2017-11-15    Gavin_Chang
Init the script
