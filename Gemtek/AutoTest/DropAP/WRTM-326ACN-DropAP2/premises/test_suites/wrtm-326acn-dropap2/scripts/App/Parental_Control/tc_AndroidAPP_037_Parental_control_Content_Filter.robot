*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Close APP

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

*** Variables ***
${browse_web}    payeasy.com
${notifications_message}    is trying to visit the blocked website
*** Test Cases ***
tc_AndroidAPP_037_Parental_control_Content_Filter
    [Documentation]  tc_AndroidAPP_037_Parental_control_Content_Filter
    ...    1. Launch the app and go to the Parental control page
    ...    2. Click Content filter
    ...    3. Block some category
    ...    4. Save the settings
    ...    5. Use the family mobile to browse network
    ...    6. Check the status
    [Tags]   @TCID=WRTM-326ACN-244    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP and go to parental control page
    Click Content filter
    Block some category
    Save the settings
    Use the family mobile to browse network
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

Click Content filter
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Conten_Filters_btn}

Block some category
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Content_Filters_SHOPPING}

Save the settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Content_Filters_Save}
    Wait Until Page Contains Element    ${Conten_Filters_btn}    timeout=30

Use the family mobile to browse network
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux wget Successful    app_lanhost    ${browse_web}    5    -5

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch notifications info menu
    Wait Until Page Contains    ${notifications_message}    timeout=30
    touch notifications info menu
    Click Element    ${Conten_Filters_btn}
    Click Element    ${Content_Filters_SHOPPING}
    Click Element    ${Content_Filters_Save}
    Wait Until Page Contains Element    ${Conten_Filters_btn}    timeout=30

*** comment ***
2017-12-27    Gavin_Chang
Init the script