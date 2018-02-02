*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_095_MainScreen_Speed_test_Swipe_to_right_History_screen
    [Documentation]  tc_AndroidAPP_095_MainScreen_Speed_test_Swipe_to_right_History_screen.robot
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Speed test.
    ...    3. Press the test button.
    ...    4. After the APP show the speed test result, press the retest button.
    ...    5. Retest 10 times.
    ...    6. Swipe the screen to right.
    ...    7. Check the History record.

    [Tags]   @TCID=WRTM-326ACN-416    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Speed test
    Press the test button
    After the APP show the speed test result, press the retest button
    Retest 10 times
    Swipe the screen to right
    Check the History record

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

Press the test button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Speed Test Now

After the APP show the speed test result, press the retest button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait speed test retest web
    ${first_download_value}    Get Text    ${speed_test_download_value}
    log    ${first_download_value}
    Should Not Be Equal    ${first_download_value}    ${original_speed_test_value}
    set test variable    ${first_download_value}    ${first_download_value}
    ${first_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${first_upload_value}
    Should Not Be Equal    ${first_upload_value}    ${original_speed_test_value}
    set test variable    ${first_upload_value}    ${first_upload_value}
    ${first_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${first_ping_value}
    Should Not Be Equal    ${first_ping_value}    ${original_speed_test_value}
    set test variable    ${first_ping_value}    ${first_ping_value}
    touch Speed Test Retest

Retest 10 times
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait speed test retest web
    ${second_download_value}    Get Text    ${speed_test_download_value}
    log    ${second_download_value}
    Should Not Be Equal    ${second_download_value}    ${original_speed_test_value}
    set test variable    ${second_download_value}    ${second_download_value}
    ${second_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${second_upload_value}
    Should Not Be Equal    ${second_upload_value}    ${original_speed_test_value}
    set test variable    ${second_upload_value}    ${second_upload_value}
    ${second_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${second_ping_value}
    Should Not Be Equal    ${second_ping_value}    ${original_speed_test_value}
    set test variable    ${second_ping_value}    ${second_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${third_download_value}    Get Text    ${speed_test_download_value}
    log    ${third_download_value}
    Should Not Be Equal    ${third_download_value}    ${original_speed_test_value}
    set test variable    ${third_download_value}    ${third_download_value}
    ${third_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${third_upload_value}
    Should Not Be Equal    ${third_upload_value}    ${original_speed_test_value}
    set test variable    ${third_upload_value}    ${third_upload_value}
    ${third_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${third_ping_value}
    Should Not Be Equal    ${third_ping_value}    ${original_speed_test_value}
    set test variable    ${third_ping_value}    ${third_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${fourth_download_value}    Get Text    ${speed_test_download_value}
    log    ${fourth_download_value}
    Should Not Be Equal    ${fourth_download_value}    ${original_speed_test_value}
    set test variable    ${fourth_download_value}    ${fourth_download_value}
    ${fourth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${fourth_upload_value}
    Should Not Be Equal    ${fourth_upload_value}    ${original_speed_test_value}
    set test variable    ${fourth_upload_value}    ${fourth_upload_value}
    ${fourth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${fourth_ping_value}
    Should Not Be Equal    ${fourth_ping_value}    ${original_speed_test_value}
    set test variable    ${fourth_ping_value}    ${fourth_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${fifth_download_value}    Get Text    ${speed_test_download_value}
    log    ${fifth_download_value}
    Should Not Be Equal    ${fifth_download_value}    ${original_speed_test_value}
    set test variable     ${fifth_download_value}    ${fifth_download_value}
    ${fifth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${fifth_upload_value}
    Should Not Be Equal    ${fifth_upload_value}    ${original_speed_test_value}
    set test variable     ${fifth_upload_value}    ${fifth_upload_value}
    ${fifth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${fifth_ping_value}
    Should Not Be Equal    ${fifth_ping_value}    ${original_speed_test_value}
    set test variable     ${fifth_ping_value}    ${fifth_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${sixth_download_value}    Get Text    ${speed_test_download_value}
    log    ${sixth_download_value}
    Should Not Be Equal    ${sixth_download_value}    ${original_speed_test_value}
    set test variable     ${sixth_download_value}    ${sixth_download_value}
    ${sixth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${sixth_upload_value}
    Should Not Be Equal    ${sixth_upload_value}    ${original_speed_test_value}
    set test variable     ${sixth_upload_value}    ${sixth_upload_value}
    ${sixth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${sixth_ping_value}
    Should Not Be Equal    ${sixth_ping_value}    ${original_speed_test_value}
    set test variable     ${sixth_ping_value}    ${sixth_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${seventh_download_value}    Get Text    ${speed_test_download_value}
    log    ${seventh_download_value}
    Should Not Be Equal    ${seventh_download_value}    ${original_speed_test_value}
    set test variable     ${seventh_download_value}    ${seventh_download_value}
    ${seventh_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${seventh_upload_value}
    Should Not Be Equal    ${seventh_upload_value}    ${original_speed_test_value}
    set test variable     ${seventh_upload_value}    ${seventh_upload_value}
    ${seventh_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${seventh_ping_value}
    Should Not Be Equal    ${seventh_ping_value}    ${original_speed_test_value}
    set test variable     ${seventh_ping_value}    ${seventh_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${eighth_download_value}    Get Text    ${speed_test_download_value}
    log    ${eighth_download_value}
    Should Not Be Equal    ${eighth_download_value}    ${original_speed_test_value}
    set test variable     ${eighth_download_value}    ${eighth_download_value}
    ${eighth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${eighth_upload_value}
    Should Not Be Equal    ${eighth_upload_value}    ${original_speed_test_value}
    set test variable     ${eighth_upload_value}    ${eighth_upload_value}
    ${eighth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${eighth_ping_value}
    Should Not Be Equal    ${eighth_ping_value}    ${original_speed_test_value}
    set test variable    ${eighth_ping_value}    ${eighth_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${ninth_download_value}    Get Text    ${speed_test_download_value}
    log    ${ninth_download_value}
    Should Not Be Equal    ${ninth_download_value}    ${original_speed_test_value}
    set test variable    ${ninth_download_value}    ${ninth_download_value}
    ${ninth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${ninth_upload_value}
    Should Not Be Equal    ${ninth_upload_value}    ${original_speed_test_value}
    set test variable    ${ninth_upload_value}    ${ninth_upload_value}
    ${ninth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${ninth_ping_value}
    Should Not Be Equal    ${ninth_ping_value}    ${original_speed_test_value}
    set test variable    ${ninth_ping_value}    ${ninth_ping_value}

    touch Speed Test Retest
    wait speed test retest web
    ${tenth_download_value}    Get Text    ${speed_test_download_value}
    log    ${tenth_download_value}
    Should Not Be Equal    ${tenth_download_value}    ${original_speed_test_value}
    set test variable     ${tenth_download_value}    ${tenth_download_value}
    ${tenth_upload_value}    Get Text    ${speed_test_upload_value}
    log    ${tenth_upload_value}
    Should Not Be Equal    ${tenth_upload_value}    ${original_speed_test_value}
    set test variable     ${tenth_upload_value}    ${tenth_upload_value}
    ${tenth_ping_value}    Get Text    ${speed_test_ping_value}
    log    ${tenth_ping_value}
    Should Not Be Equal    ${tenth_ping_value}    ${original_speed_test_value}
    set test variable     ${tenth_ping_value}    ${tenth_ping_value}

Swipe the screen to right
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Right
    Wait Until Page Contains Element    ${left}    timeout=60

Check the History record
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    log    ${first_download_value}
    log    ${first_upload_value}
    Page Should Contain Text    ${first_download_value}
    Page Should Contain Text    ${first_upload_value}
    Page Should Contain Text    ${first_ping_value}

    Page Should Contain Text    ${second_download_value}
    Page Should Contain Text    ${second_upload_value}
    Page Should Contain Text    ${second_ping_value}

    Page Should Contain Text    ${third_download_value}
    Page Should Contain Text    ${third_upload_value}
    Page Should Contain Text    ${third_ping_value}

    Page Should Contain Text    ${fourth_download_value}
    Page Should Contain Text    ${fourth_upload_value}
    Page Should Contain Text    ${fourth_ping_value}

    Page Should Contain Text    ${fifth_download_value}
    Page Should Contain Text    ${fifth_upload_value}
    Page Should Contain Text    ${fifth_ping_value}

    Page Should Contain Text    ${sixth_download_value}
    Page Should Contain Text    ${sixth_upload_value}
    Page Should Contain Text    ${sixth_ping_value}

    Page Should Contain Text    ${seventh_download_value}
    Page Should Contain Text    ${seventh_upload_value}
    Page Should Contain Text    ${seventh_ping_value}

    Page Should Contain Text    ${eighth_download_value}
    Page Should Contain Text    ${eighth_upload_value}
    Page Should Contain Text    ${eighth_ping_value}

    Page Should Contain Text    ${ninth_download_value}
    Page Should Contain Text    ${ninth_upload_value}
    Page Should Contain Text    ${ninth_ping_value}

    Swipe By Percent    50    60    50    10
    Page Should Contain Text    ${tenth_download_value}
    Page Should Contain Text    ${tenth_upload_value}
    Page Should Contain Text    ${tenth_ping_value}

*** comment ***
2017-12-29 Gavin_Chang
1. Set test variable if others keyword need use.

2017-12-26    Leo_Li
Init the script