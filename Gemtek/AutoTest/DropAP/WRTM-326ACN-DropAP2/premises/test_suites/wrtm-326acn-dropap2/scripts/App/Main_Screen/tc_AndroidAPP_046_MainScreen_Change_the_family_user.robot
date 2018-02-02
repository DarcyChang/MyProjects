*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_device1}    Lanhost
${member_device2}    All Devices
${device1_web}    youtube.com
${device2_web}    oogle

*** Test Cases ***
tc_AndroidAPP_046_MainScreen_Change_the_family_user
    [Documentation]  tc_AndroidAPP_046_MainScreen_Change_the_family_user
    ...    1. Launch the app then into main screen
    ...    2. Select a family user profile
    ...    3. Check the data of family user used
    ...    4. Change to another family user
    ...    5. Check the data of another family user used
    [Tags]   @TCID=WRTM-326ACN-219    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Select a family user profile
    Check the data of family user used
    Change to another family user
    Check the data of another family user used

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
    Is Linux wget Successful    app_lanhost    ${device1_web}    20    -5
    select family member    ${member_device1}

Check the data of family user used
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Text    ${device1_web}

Change to another family user
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    select family member    ${member_device2}

Check the data of another family user used
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Text    ${device2_web}

*** comment ***
2017-12-20 Gavin_Chang
Init the script
