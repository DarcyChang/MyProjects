*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Leo_Li

*** Variables ***
${created_member_name}    KID
${Group_name_id}    com.dropap.dropap:id/tvGroup

*** Test Cases ***
tc_AndroidAPP_041_Parental_control_Delete_family_user
    [Documentation]  tc_AndroidAPP_041_Parental_control_Delete_family_user
    ...    1. Launch the app and go to the Parental control page.
    ...    2. Press delete button to delete current family user.
    ...    3. Press Yes then check the status.

    [Tags]   @TCID=WRTM-326ACN-255    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to the Parental control page
    Press delete button to delete current family user
    Press Yes then check the status

*** Keywords ***
Launch the app and go to the Parental control page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    Create Family Member    ${created_member_name}    ${created_member_name}
    touch family member
    Click Text    ${created_member_name}
    wait main screen
    Check the created member name status

Press delete button to delete current family user
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Swipe To Right
    touch Delete

Press Yes then check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Delete ok
    wait main screen
    check the status

Check the created member name status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Group_name}    Get Text    ${Group_name_id}
    log    ${Group_name}
    Should Contain    ${Group_name}    ${created_member_name}

check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Group_name}    Get Text    ${Group_name_id}
    log    ${Group_name}
    Should Not Contain    ${Group_name}    ${created_member_name}
    touch family member
    Page Should Not Contain Text    ${created_member_name}

*** comment ***
2017-12-26 Gavin_Chang
1. Using keyword to create family member and detect keyboard then hide it.

2017-12-01 Gavin_Chang
1. Select member should wait until loading page close

2017-11-27    Leo_Li
Init the script