*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Recover Member List

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Leo_Li

*** Variables ***
${created_member_name}    KID
${DeviceName}    ASUS Zenfone 6
${no_history_info}    (No browsed website history)
${clear_data_info}    Are you sure to clear the Website and Apps data?

*** Test Cases ***
tc_AndroidAPP_040_Parental_control_Clear_Website_and_Apps_Data
    [Documentation]  tc_AndroidAPP_040_Parental_control_Clear_Website_and_Apps_Data
    ...    1. Launch the app and go to the Parental control page.
    ...    2. Clear Website and Apps Data.
    ...    3. Press Yes then check the status.

    [Tags]   @TCID=WRTM-326ACN-254    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the Parental control page
    Clear Website and Apps Data
    Press Yes then check the status

*** Keywords ***
Launch the app and go to the Parental control page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Clear Website and Apps Data
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Create a family member
    Swipe To Right
    Wait Until Page Contains Element    ${Clear_Website_and_Apps_Data_btn}    timeout=60

Create a family member
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
    Click Text    ${created_member_name}
    wait main screen
    ${Group_name}    Get Text    ${group_device_name}
    log    ${Group_name}
    Should Contain    ${Group_name}    ${created_member_name}
    Page Should Not Contain Element    ${refresh_report}
    Page Should Not Contain Text    ${no_history_info}

Press Yes then check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Clear_Website_and_Apps_Data_btn}
    Wait Until Page Contains    ${clear_data_info}    timeout=60
    Click Element    ${Clear_Website_and_Apps_Data_cancel}
    Page Should Contain Element    ${Clear_Website_and_Apps_Data_btn}
    Click Element    ${Clear_Website_and_Apps_Data_btn}
    Wait Until Page Contains    ${clear_data_info}    timeout=60
    Click Element    ${Clear_Website_and_Apps_Data_ok}
    Page Should Contain Element    ${refresh_report}
    Page Should Contain Text    ${no_history_info}

Recover Member List
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Right
    touch Delete
    touch Delete ok
    wait main screen
    Close APP

*** comment ***
2017-12-26    Leo_Li
Init the script
