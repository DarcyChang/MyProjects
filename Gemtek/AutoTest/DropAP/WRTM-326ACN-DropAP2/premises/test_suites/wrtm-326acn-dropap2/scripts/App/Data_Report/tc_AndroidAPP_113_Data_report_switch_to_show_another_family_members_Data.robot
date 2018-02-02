*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Data_Report    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_device1}    Lanhost
${member_device2}    All Devices
${device1_web}    youtube.com
${device2_web}    google.com

*** Test Cases ***
tc_AndroidAPP_113_Data_report_switch_to_show_another_family_members_Data
    [Documentation]  tc_AndroidAPP_113_Data_report_switch_to_show_another_family_members_Data
    ...    1. Launch the app and login the user account
    ...    2. Swipe to left to show the Data report screen
    ...    3. Select a member and check the data report
    ...    4. Select another member and check the data report
    [Tags]   @TCID=WRTM-326ACN-279    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Swipe to left to show the Data report screen
    Select a member and check the data report
    Select another member and check the data report

*** Keywords ***
Launch the app and login the user account
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen
    select family member

Swipe to left to show the Data report screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Swipe To Left

Select a member and check the data report
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${device1_web}    20    -5
    select family member    ${member_device1}
    Page Should Contain Text    ${device1_web}

Select another member and check the data report
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    select family member    ${member_device2}
    Page Should Contain Text    ${device2_web}

*** comment ***
2017-12-12 Gavin_Chang
1. Browse website first to make sure date report is not empty.

2017-12-06    Gavin_Chang
Init the script
