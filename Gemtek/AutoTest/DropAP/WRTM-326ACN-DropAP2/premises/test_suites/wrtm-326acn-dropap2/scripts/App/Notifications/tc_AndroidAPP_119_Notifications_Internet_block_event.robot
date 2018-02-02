*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Notifications    @AUTHOR=Gavin_Chang

*** Variables ***
${blocked_web_keyword}    xvideo
${browse_web}    xvideo.com
${notifications_message}    is trying to visit the blocked website. URL: ${browse_web}
*** Test Cases ***
tc_AndroidAPP_119_Notifications_Internet_block_event
    [Documentation]  tc_AndroidAPP_119_Notifications_Internet_block_event
    ...    1. Launch the DropAP and go to parental control page
    ...    2. Set the some forbidden website to block family member.(ex. Max -> www.xvideos.com)
    ...    3. Use the family user mobile to browse website.(www.xvideos.com)
    ...    4. Check main user(parental) notifications
    [Tags]   @TCID=WRTM-326ACN-370    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP and go to parental control page
    Set the some forbidden website to block family member.(ex. Max -> www.xvideos.com)
    Use the family user mobile to browse website.(www.xvideos.com)
    Check main user(parental) notifications

*** Keywords ***
Launch the DropAP and go to parental control page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch App
    Sign In
    wait main screen
    select family member
    Swipe To Right

Set the some forbidden website to block family member.(ex. Max -> www.xvideos.com)
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Blocked Websites settings    ${blocked_web_keyword}

Use the family user mobile to browse website.(www.xvideos.com)
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Failed    app_lanhost    ${browse_web}    5    -5

Check main user(parental) notifications
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch notifications info menu
    Wait Until Page Contains    ${notifications_message}    timeout=30
    touch notifications info menu
    Delete Blocked Websites settings
*** comment ***
2017-12-27    Gavin_Chang
Init the script