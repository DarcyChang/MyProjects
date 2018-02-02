*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***
${Eniwetok_timezone}    Eniwetok (-12:00)
${Taipei_timezone}    Taipei (+08:00)

*** Test Cases ***
tc_AndroidAPP_078_MainScreen_Check_the_Timezone
    [Documentation]  tc_AndroidAPP_078_MainScreen_Check_the_Timezone
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Timezone.
    ...    3. Press timezone, it will go to timezone screen.
    ...    4. Check the status after you change the timezone.
    [Tags]   @TCID=WRTM-326ACN-306    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Timezone
    Press timezone, it will go to timezone screen
    Check the status after you change the timezone

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Timezone
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings

Press timezone, it will go to timezone screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Timezone

Check the status after you change the timezone
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Check current timezone
    Click Text    ${Eniwetok_timezone}
    Wait Until Page Contains Element    ${current_zone}    timeout=60
    ${change_timezone}    Get Text    ${current_zone}
    log    ${change_timezone}
    Should Not Contain    ${change_timezone}    ${current_timezone}

Check current timezone
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${current_timezone}    Get Text    ${current_zone}
    log    ${current_timezone}
    set test variable    ${current_timezone}    ${current_timezone}

*** comment ***
2017-12-19    Leo_Li
Init the script