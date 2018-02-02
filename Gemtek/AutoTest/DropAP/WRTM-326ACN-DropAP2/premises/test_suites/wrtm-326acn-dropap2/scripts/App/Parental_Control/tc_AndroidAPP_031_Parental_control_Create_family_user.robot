*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Parental_Control    @AUTHOR=Gavin_Chang

Test Teardown    Recover Member List

*** Variables ***
${member_name}    KID

*** Test Cases ***
tc_AndroidAPP_031_Parental_control_Create_family_user
    [Documentation]  tc_AndroidAPP_031_Parental_control_Create_family_user
    ...    1. Launch the app and go to the main screen
    ...    2. Press the Family icon
    ...    3. Press "Create family user"
    ...    4. Add name of family
    ...    5. Assign the age setting
    ...    6. Assign owned devices
    ...    7. Check the status
    [Tags]   @TCID=WRTM-326ACN-214    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app and go to the main screen
    Press the Family icon
    Press "Create family user"
    Add name of family
    Assign the age setting
    Assign owned devices
    Check the status


*** Keywords ***
Launch the app and go to the main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Press the Family icon
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch family member

Press "Create family user"
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch create family member label

Add name of family
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    input family member name    ${member_name}
    touch next

Assign the age setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Element Attribute Should Match    ${kid}    enabled    true
    touch next

Assign owned devices
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch next

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${successful_info}    timeout=60
    Page Should Contain Text    &quot;${member_name}&quot; has been successfully added to your family.
    Click Element    ${successful_info}
    touch left

Recover Member List
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Delete Member    ${member_name}
    Close APP


*** comment ***
2017-11-27    Gavin_Chang
Init the script
