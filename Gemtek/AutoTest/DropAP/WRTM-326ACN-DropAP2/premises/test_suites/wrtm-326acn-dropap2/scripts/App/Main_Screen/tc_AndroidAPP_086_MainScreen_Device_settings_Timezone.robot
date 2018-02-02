*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_086_MainScreen_Device_settings_Timezone
    [Documentation]  tc_AndroidAPP_086_MainScreen_Device_settings_Timezone
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Timezone
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-364    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Timezone
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Timezone
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Timezone

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify Timezone page


*** comment ***
2017-11-21    Gavin_Chang
Init the script
