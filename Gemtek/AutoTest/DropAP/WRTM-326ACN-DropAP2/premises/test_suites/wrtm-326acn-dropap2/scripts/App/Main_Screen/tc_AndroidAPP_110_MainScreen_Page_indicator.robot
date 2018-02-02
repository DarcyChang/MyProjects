*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***
${upgrade_message}    There is no new version for your device.


*** Test Cases ***
tc_AndroidAPP_110_MainScreen_Page_indicator
    [Documentation]  tc_AndroidAPP_110_MainScreen_Page_indicator
    ...    1. Launch the DropAP app into main screen
    ...    2. Swipe to left and check the status
    ...    3. Swipe to right and check the status
    [Tags]   @TCID=WRTM-326ACN-417    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Swipe to left and check the status
    Swipe to right and check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Swipe to left and check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Left
    verfiy Data Report page

Swipe to right and check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Right
    Swipe To Right
    Page Should Contain Text    Blocked Websites

*** comment ***
2017-11-21    Gavin_Chang
Init the script
