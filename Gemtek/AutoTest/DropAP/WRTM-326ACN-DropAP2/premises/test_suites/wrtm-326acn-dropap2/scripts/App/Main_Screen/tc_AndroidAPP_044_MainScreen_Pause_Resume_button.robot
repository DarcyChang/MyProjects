*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_device}    Lanhost
${device_web}    youtube.com
${browser_web}    yahoo.com


*** Test Cases ***
tc_AndroidAPP_044_MainScreen_Pause_Resume_button
    [Documentation]  tc_AndroidAPP_044_MainScreen_Pause_Resume_button
    ...    1. Launch the app then into main screen.
    ...    2. Select a family user profile.
    ...    3. Press pause button.
    ...    4. Check the Family user mobile network.
    ...    5. Press resume button.
    ...    6. Check the Family user mobile network again.
    [Tags]   @TCID=WRTM-326ACN-217    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Select a family user profile
    Press pause button
    Check the Family user mobile network
    Press resume button
    Check the Family user mobile network again

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Select a family user profile
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${device_web}    20    -5
    select family member    ${member_device}

Press pause button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Pause_Resume    Pause

Check the Family user mobile network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux Ping Fail    app_lanhost    ${device_web}

Press resume button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Pause_Resume    Resume

Check the Family user mobile network again
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${device_web}    20    -5

*** comment ***
2017-12-06    Gavin_Chang
Init the script
