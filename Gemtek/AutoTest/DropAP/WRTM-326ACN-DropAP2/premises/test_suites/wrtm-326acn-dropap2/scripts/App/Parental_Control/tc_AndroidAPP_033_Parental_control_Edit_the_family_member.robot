*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Recover Member List

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Leo_Li

*** Variables ***
${created_member_name}    KID
${Edit_member_name_id}    com.dropap.dropap:id/etValue
${Edit_member_name}    admin
${SAVE_Positive}    com.dropap.dropap:id/btnPositive
${SAVE}    com.dropap.dropap:id/btnSave
${Group_name_id}    com.dropap.dropap:id/tvGroup

*** Test Cases ***
tc_AndroidAPP_033_Parental_control_Edit_the_family_member
    [Documentation]  tc_AndroidAPP_033_Parental_control_Edit_the_family_member
    ...    1. Launch the app and go to the main screen.
    ...    2. Create some family member.
    ...    3. Launch one member, try to edit family name.

    [Tags]   @TCID=WRTM-326ACN-227    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the main screen
    Create some family member
    Launch one member, try to edit family name

*** Keywords ***
Launch the app and go to the main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Create some family member
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch family member
    touch create family member label
    input family member name    ${created_member_name}
    touch next
    Element Attribute Should Match    ${kid}    enabled    true
    touch next
    touch next
    Wait Until Page Contains Element    ${successful_info}    timeout=60
    Page Should Contain Text    &quot;${created_member_name}&quot; has been successfully added to your family.
    Click Element    ${successful_info}

Launch one member, try to edit family name
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Text    ${created_member_name}
    wait main screen
    Check the created member name status
    Swipe To Right
    Click Text    ${created_member_name}
    Click Text    ${created_member_name}
    Clear Text    ${Edit_member_name_id}
    Input Text    ${Edit_member_name_id}    ${Edit_member_name}
    Click Element    ${SAVE_Positive}
    wait until page contains element    ${SAVE}
    Click Element    ${SAVE}
    Check the Edit member name status

Check the created member name status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Group_name}    Get Text    ${Group_name_id}
    log    ${Group_name}
    Should Contain    ${Group_name}    ${created_member_name}

Check the Edit member name status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Left
    touch family member
    sleep    5s
    Page Should Contain Text    ${Edit_member_name}

Recover Member List
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Text    ${Edit_member_name}
    wait main screen
    Swipe To Right
    touch Delete
    touch Delete ok
    wait main screen
    Close APP

*** comment ***
2017-11-27    Leo_Li
Init the script