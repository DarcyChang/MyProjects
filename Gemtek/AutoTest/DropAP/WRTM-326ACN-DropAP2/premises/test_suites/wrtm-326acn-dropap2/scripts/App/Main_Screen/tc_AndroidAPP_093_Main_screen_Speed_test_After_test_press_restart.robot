*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown      Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_093_Main_screen_Speed_test_After_test_press_restart
    [Documentation]  tc_AndroidAPP_093_Main_screen_Speed_test_After_test_press_restart
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Speed test.
    ...    3. Press test button.
    ...    4. Waiting for the Speed test complete.
    ...    5. Press restart again.
    ...    6. Check the status.
    [Tags]   @TCID=WRTM-326ACN-397    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Speed test
    Press test button
    Waiting for the Speed test complete
    Press restart again
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Speed test
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    Swipe To Up
    touch Speed Test
    wait speed test web

Press test button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Speed Test Now

Waiting for the Speed test complete
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait speed test retest web
    ${download_value}    Get Text    ${speed_test_download_value}
    log    ${download_value}
    Should Not Be Equal    ${download_value}    ${original_speed_test_value}
    ${upload_value}    Get Text    ${speed_test_upload_value}
    log    ${upload_value}
    Should Not Be Equal    ${upload_value}    ${original_speed_test_value}

Press restart again
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Speed Test Retest

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait speed test retest web
    ${second_download_value}    Get Text    ${speed_test_download_value}
    log    ${second_download_value}
    Should Not Be Equal    ${second_download_value}    ${original_speed_test_value}
    ${second_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${second_upload_value}
    Should Not Be Equal    ${second_upload_value}    ${original_speed_test_value}

*** comment ***
2017-12-08 Gavin_Chang
1. Using Should Not Be Equal instead of Should Not Contain due to x0.0x contain 0.0
2. Move element id and sub keyword to keyword folder base on frame.

2017-12-05    Leo_Li
Init the script