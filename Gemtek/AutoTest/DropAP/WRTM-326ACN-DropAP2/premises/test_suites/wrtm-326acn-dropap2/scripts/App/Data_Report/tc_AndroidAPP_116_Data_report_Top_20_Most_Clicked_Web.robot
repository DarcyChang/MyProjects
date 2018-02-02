*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Data_Report    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_device}    Lanhost
${device_web}    youtube.com
${browser_web}    yahoo.com


*** Test Cases ***
tc_AndroidAPP_116_Data_report_Top_20_Most_Clicked_Web
    [Documentation]  tc_AndroidAPP_116_Data_report_Top_20_Most_Clicked_Web
    ...    1. Launch the app and login the user account
    ...    2. Swipe to left to show the Data report screen
    ...    3. Select a member and check the data report
    ...    4. browse others website, then check it again
    [Tags]   @TCID=WRTM-326ACN-361    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and login the user account
    Swipe to left to show the Data report screen
    Select a member and check the data report
    browse others website, then check it again

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
    Is Linux wget Successful    app_lanhost    ${device_web}    20    -5
    select family member    ${member_device}
    touch most click web
    Page Should Contain Text    ${device_web}

browse others website, then check it again
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${browser_web}    20    -5
    select family member    ${member_device}
    Page Should Contain Text    ${browser_web}

*** comment ***
2017-12-12 Gavin_Chang
1. Browse website first to make sure date report is not empty.

2017-12-06    Gavin_Chang
Init the script
