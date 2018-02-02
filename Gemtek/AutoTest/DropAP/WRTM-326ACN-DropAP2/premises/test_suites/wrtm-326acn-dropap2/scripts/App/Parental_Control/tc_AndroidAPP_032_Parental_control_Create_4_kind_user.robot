*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

Test Teardown    Close APP

*** Variables ***
${member_pre-k}    PRE-K
${member_kid}    KID
${member_teen}    TEEN
${member_adult}    ADULT

*** Test Cases ***
tc_AndroidAPP_032_Parental_control_Create_4_kind_user
    [Documentation]  tc_AndroidAPP_032_Parental_control_Create_4_kind_user
    ...    1. Launch the app and go to the main screen
    ...    2. Create the 4 kinds user
    [Tags]   @TCID=WRTM-326ACN-224    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and go to the main screen
    Create the 4 kinds user


*** Keywords ***
Launch the app and go to the main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Create the 4 kinds user
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Create Family Member    ${member_pre-k}    ${member_pre-k}
    Delete Member    ${member_pre-k}
    Create Family Member    ${member_kid}    ${member_kid}
    Delete Member    ${member_kid}
    Create Family Member    ${member_teen}    ${member_teen}
    Delete Member    ${member_teen}
    Create Family Member    ${member_adult}    ${member_adult}
    Delete Member    ${member_adult}


*** comment ***
2017-12-05 Gavin_Chang
1. Recover member list after each creation.

2017-11-27    Gavin_Chang
Init the script
