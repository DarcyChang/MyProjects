*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

*** Variables ***
${blocked_app}    Yahoo.com
${browse_web}    www.yahoo.com
${notifications_message}    is trying to visit the blocked App: ${blocked_app}

*** Test Cases ***
tc_AndroidAPP_039_Parental_control_Block_APP
    [Documentation]  tc_AndroidAPP_039_Parental_control_Block_APP
    ...    1. Launch the app then into main screen
    ...    2. Block some APP
    ...    3. Use the family mobile to use those APP
    ...    4. Check the status
    [Tags]   @TCID=WRTM-326ACN-247    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the app then into main screen
    Block some APP
    Use the family mobile to use those APP
    Check the status

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch App
    Sign In
    wait main screen
    Is Linux wget Successful    app_lanhost    ${browse_web}    5    -5
    select family member

Block some APP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Blocked Apps settings    ${blocked_app}

Use the family mobile to use those APP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Failed    app_lanhost    ${browse_web}    5    -5

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch notifications info menu
    Wait Until Page Contains    ${notifications_message}    timeout=30
    touch notifications info menu
    Swipe To Right
    Delete Blocked Apps settings

*** comment ***
2018-01-04    Gavin_Chang
Init the script