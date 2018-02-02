*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

*** Variables ***
${blocked_web_keyword}    xvideo
${browse_web}    xvideo.com

*** Test Cases ***
tc_AndroidAPP_038_Parental_control_Block_Website
    [Documentation]  tc_AndroidAPP_038_Parental_control_Block_Website
    ...    1. Launch the app and go to the Parental control page
    ...    2. Click Block website
    ...    3. Block some website
    ...    4. Save the settings
    ...    5. Use the family mobile to browse those website
    ...    6. Check the status
    [Tags]   @TCID=WRTM-326ACN-245    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the DropAP and go to parental control page
    Click Block website -> Block some website -> Save the settings
    Use the family mobile to browse those website
    Check the status

*** Keywords ***
Launch the DropAP and go to parental control page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch App
    Sign In
    wait main screen
    select family member
    Swipe To Right

Click Block website -> Block some website -> Save the settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Blocked Websites settings    ${blocked_web_keyword}

Use the family mobile to browse those website
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Failed    app_lanhost    ${browse_web}    5    -5

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Delete Blocked Websites settings
    Swipe To Left
    select family member
    Page Should Contain Text    ${browse_web}
*** comment ***
2018-01-04    Gavin_Chang
Init the script