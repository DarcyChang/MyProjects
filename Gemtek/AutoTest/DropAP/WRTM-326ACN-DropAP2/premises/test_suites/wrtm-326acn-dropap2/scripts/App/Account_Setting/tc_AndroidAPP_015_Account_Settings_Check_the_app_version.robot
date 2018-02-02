*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_015_Account_Settings_Check_the_app_version
    [Documentation]  tc_AndroidAPP_015_Account_Settings_Check_the_app_version
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Check the app version.
    [Tags]   @TCID=WRTM-326ACN-207    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left-upper corner
    Check the app version

*** Keywords ***
Launch the app and into the main page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Press account settings at left-upper corner
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu

Check the app version
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${DropAP_version}    Get Text    ${version_info}
    log    ${DropAP_version}
    Should Contain    ${DropAP_version}    ${g_app_version}

*** comment ***
2017-11-21    Leo_Li
1. Remove Variables
2. Modified Keywords Check the app version content.

2017-11-17    Leo_Li
Init the script