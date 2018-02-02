*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Data_Report    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_device}    Lanhost
${device_app}    Yahoo.com
${launch_app}    youtube.com
${check_launch_app}    YouTube


*** Test Cases ***
tc_AndroidAPP_115_Data_report_Top_20_Most_Used_APP
    [Documentation]  tc_AndroidAPP_115_Data_report_Top_20_Most_Used_APP
    ...    1. Launch the app and login the user account
    ...    2. Swipe to left to show the Data report screen
    ...    3. Select the family member and check the Top 20 APP
    ...    4. Launch others APP, then check it again
    [Tags]   @TCID=WRTM-326ACN-357    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Swipe to left to show the Data report screen
    Select the family member and check the Top 20 APP
    Launch others APP, then check it again

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

Select the family member and check the Top 20 APP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${device_app}    20    -5
    select family member    ${member_device}
    touch most used app
    Page Should Contain Text    ${device_app}

Launch others APP, then check it again
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${launch_app}    20    -5
    select family member    ${member_device}
    Page Should Contain Text    ${check_launch_app}

*** comment ***
2017-12-12 Gavin_Chang
1. Browse website first to make sure date report is not empty.

2017-12-06    Gavin_Chang
Init the script
