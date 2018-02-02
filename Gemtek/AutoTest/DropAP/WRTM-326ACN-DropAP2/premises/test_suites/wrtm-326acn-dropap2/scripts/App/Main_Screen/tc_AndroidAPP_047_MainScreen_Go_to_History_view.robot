*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Restore Member Device

*** Variables ***
${created_member_name}    KID
${DeviceName}    ASUS Zenfone 6

${restore_member}    Lanhost
${restore_device}    app-lanhost
*** Test Cases ***
tc_AndroidAPP_047_MainScreen_Go_to_History_view
    [Documentation]  tc_AndroidAPP_047_MainScreen_Go_to_History_view
    ...    1. Launch the app then into main screen.
    ...    2. Select a family user profile.
    ...    3. Check the data and press ""today"" button.
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-220    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app then into main screen
    Select a family user profile
    Check the data and press today button
    Check the status

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Select a family user profile
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Create some family member

Create some family member
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch family member
    touch create family member label
    input family member name    ${created_member_name}
    touch next
    Element Attribute Should Match    ${kid}    enabled    true
    touch next
    Click Text    ${DeviceName}
    touch next
    Wait Until Page Contains Element    ${successful_info}    timeout=60
    Page Should Contain Text    &quot;${created_member_name}&quot; has been successfully added to your family.
    Click Element    ${successful_info}
    Page Should Contain Text    ${created_member_name}
    Click Text    ${created_member_name}
    wait main screen

Check the data and press today button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    Online Time
    touch today

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Text    History

Restore Member Device
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch left
    Swipe To Right
    Click Text    Delete
    touch Remove OK button
    wait main screen
    Close APP

*** comment ***
2017-12-19    Leo_Li
Init the script