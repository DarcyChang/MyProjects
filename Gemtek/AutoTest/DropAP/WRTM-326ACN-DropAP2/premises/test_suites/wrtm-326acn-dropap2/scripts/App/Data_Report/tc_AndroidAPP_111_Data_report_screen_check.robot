*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Data_Report    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_111_Data_report_screen_check
    [Documentation]  tc_AndroidAPP_111_Data_report_screen_check
    ...    1. Launch the app and login the user account
    ...    2. Launch main screen and select the family user
    ...    3. Swipe to left to show the Data report screen
    ...    4. Check the UI screen
    [Tags]   @TCID=WRTM-326ACN-256    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Launch main screen and select the family user
    Swipe to left to show the Data report screen
    Check the UI screen

*** Keywords ***
Launch the app and login the user account
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen and select the family user
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    select family member

Swipe to left to show the Data report screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Left

Check the UI screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify account info menu
    verify main screen device name
    verify notifications info menu
    verify family member
    verify most used web
    verify most used app
    verify most click web
    verify today top 20
    verify seven days top 20

*** comment ***
2017-11-27    Gavin_Chang
Init the script
