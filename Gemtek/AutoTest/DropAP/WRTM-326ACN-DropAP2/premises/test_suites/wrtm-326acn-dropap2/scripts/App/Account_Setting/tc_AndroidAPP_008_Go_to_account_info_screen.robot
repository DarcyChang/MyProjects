*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_008_Go_to_account_info_screen
    [Documentation]  tc_AndroidAPP_008_Go_to_account_info_screen
    ...    1. Press the account button at left upper corner.
    ...    2. Check the account info.
    [Tags]   @TCID=WRTM-326ACN-183    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Press the account button at left upper corner
    Check the account info

*** Keywords ***
Press the account button at left upper corner
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    touch account menu

Check the account info
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify the account info

*** comment ***
2017-11-20 Gavin_Chang
Move Variables To Parameters.

2017-11-17    Leo_Li
Init the script