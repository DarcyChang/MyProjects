*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_096_MainScreen_Device_Settings_System_info
    [Documentation]  tc_AndroidAPP_096_MainScreen_Device_Settings_System_info
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > System info
    ...    3. Check the status
    [Tags]   @TCID=WRTM-326ACN-415    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > System info
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > System info
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch System Info


Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify items in System Info

*** comment ***
2017-11-15    Gavin_Chang
Init the script
