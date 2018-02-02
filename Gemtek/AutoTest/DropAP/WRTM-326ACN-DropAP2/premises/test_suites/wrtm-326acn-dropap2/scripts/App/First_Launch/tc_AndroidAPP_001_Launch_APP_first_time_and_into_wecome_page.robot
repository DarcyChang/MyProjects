*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=First_Launch    @AUTHOR=Leo_Li

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_001_Launch_APP_first_time_and_into_wecome_page
    [Documentation]  tc_AndroidAPP_001_Launch_APP_first_time_and_into_wecome_page
    ...    1. Launch the app then show the Drop AP wecome page.
    ...    2. Check the status.
    [Tags]   @TCID=WRTM-326ACN-181    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app then show the Drop AP wecome page
    Check the status

*** Keywords ***
Launch the app then show the Drop AP wecome page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch App
    Sign In

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    wait main screen
    verify main screen device name

*** comment ***
2017-11-20 Gavin_Chang
Move Variables To Parameters.

2017-11-17    Leo_Li
Init the script