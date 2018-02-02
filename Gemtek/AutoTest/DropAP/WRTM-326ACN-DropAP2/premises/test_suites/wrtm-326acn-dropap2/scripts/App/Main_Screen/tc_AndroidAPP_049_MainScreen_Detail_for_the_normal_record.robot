*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${browse_web}    youtube.com


*** Test Cases ***
tc_AndroidAPP_049_MainScreen_Detail_for_the_normal_record
    [Documentation]  tc_AndroidAPP_049_MainScreen_Detail_for_the_normal_record
    ...    1. Launch the app then into main screen
    ...    2. Select a family user profile
    ...    3. Click one of the data that is user visited forbidden website
    ...    4. Check the status

    [Tags]   @TCID=WRTM-326ACN-222    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Select a family user profile
    Click one of the data that is user visited forbidden website
    Check the status

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
    Is Linux wget Successful    app_lanhost    ${browse_web}    20    -5
    select family member

Click one of the data that is user visited forbidden website
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Text    ${browse_web}
    Click Element    ${block_app_btn}
    wait main screen
    Is Linux wget Failed    app_lanhost    ${browse_web}    20    -5
    select family member
    Click Element    ${block_icon}

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Text    Visit this Website
    Page Should Contain Text    Unblock
    Click Element    ${block_app_btn}
    wait main screen

*** comment ***
2018-01-08 Gavin_Chang
Init the script
