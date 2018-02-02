*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_069_MainScreen_Device_settings
    [Documentation]  tc_AndroidAPP_069_MainScreen_Device_settings
    ...    1. Launch the DropAP app into main screen
    ...    2. Press device settings button
    ...    3. Check the device option
    [Tags]   @TCID=WRTM-326ACN-251    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Press device settings button
    Check the device option

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Press device settings button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings

Check the device option
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    verify Authorization Code
    verify Wireless Setting
    verify Internet Connection
    verify Timezone
    verify Anti-Phishing
    verify Performance Control
    verify Speed Test
    verify System Info
    verify Restart DropAP
    verify Upgrade
    verify Remove DropAP
    verify Reset to Default

*** comment ***
2017-11-15    Gavin_Chang
Init the script
