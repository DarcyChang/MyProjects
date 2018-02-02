*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_109_MainScreen_GPS_button
    [Documentation]  tc_AndroidAPP_109_MainScreen_GPS_button
    ...    1. Launch the DropAP app into main screen
    ...    2. Click GPS button at left side
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-419    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Click GPS button at left side
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Click GPS button at left side
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch gps

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify gps device name


*** comment ***
2017-12-01 Gavin_chang
1. Using all devices to check gps map

2017-11-21    Gavin_Chang
Init the script
