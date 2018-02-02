*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${congratulations_web}    com.dropap.dropap:id/tvCongratulation

*** Test Cases ***
tc_AndroidAPP_009_Account_Settings_Add_device
    [Documentation]  tc_AndroidAPP_009_Account_Settings_Add_device
    ...    1. Launch the app and into the main page.
    ...    2. Press account settings at left-upper corner.
    ...    3. Press Add a DropAP.
    ...    5. Check the status.
    [Tags]   @TCID=WRTM-326ACN-204    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the main page
    Press account settings at left upper corner
    Press Add a DropAP
    Check the status

*** Keywords ***
Launch the app and into the main page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Press account settings at left upper corner
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch account menu

Press Add a DropAP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch add dropap
    touch DropAP is powered on
    touch plugged in the ethernet cable
    touch next step
    wait add dropap congratulations web
    Click Element    ${OK_btn}

wait add dropap congratulations web
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${congratulations_web}    timeout=10

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    verify account info menu

*** comment ***
2017-12-05    Leo_Li
Init the script