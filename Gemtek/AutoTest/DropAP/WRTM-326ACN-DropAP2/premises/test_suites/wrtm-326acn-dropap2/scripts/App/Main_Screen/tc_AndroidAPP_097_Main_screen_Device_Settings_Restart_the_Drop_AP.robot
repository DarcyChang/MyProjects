*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown      Close APP

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest

*** Test Cases ***
tc_AndroidAPP_097_Main_screen_Device_Settings_Restart_the_Drop_AP
    [Documentation]  tc_AndroidAPP_097_Main_screen_Device_Settings_Restart_the_Drop_AP
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Restart the Drop AP.
    ...    3. Select ""Confirm"".
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-420    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Restart the Drop AP
    Select Confirm
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Restart the Drop AP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    Swipe To Up
    touch Restart DropAP

Select Confirm
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${confirm}
    Click Element    ${confirm}


Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    show router Offline icon
    verify the device status


*** comment ***
2017-12-11 Gavin_Chang
1. Add waiting time to wait offline icon
2. Move element id and sub keyword to keyword folder base on frame.

2017-12-05    Leo_Li
Init the script