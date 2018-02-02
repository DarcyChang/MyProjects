*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_108_MainScreen_Notification_button
    [Documentation]  tc_AndroidAPP_108_MainScreen_Notification_button
    ...    1. Launch the app then into main screen.
    ...    2. Click notification button at right upper corner.
    ...    3. Check the stauts.
    [Tags]   @TCID=WRTM-326ACN-421    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app then into main screen
    Click notification button at right upper corner
    Check the stauts

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch App
    Sign In
    wait main screen

Click notification button at right upper corner
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Check main screen device name
    touch notifications info menu

Check main screen device name
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${device_name}    Get Text    ${main_screen_device_name}
    log    ${device_name}
    set test variable    ${device_name}    ${device_name}

Check the stauts
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    ${device_name}

*** comment ***
2017-12-18 Gavin_Chang
1. Remove Create family member
2017-12-12    Leo_Li
Init the script