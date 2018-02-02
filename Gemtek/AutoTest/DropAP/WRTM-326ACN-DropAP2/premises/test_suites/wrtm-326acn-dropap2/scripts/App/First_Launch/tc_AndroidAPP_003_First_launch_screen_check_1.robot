*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Restore DHCP Server

Force Tags    @FEATURE=First_Launch    @AUTHOR=Gavin_Chang

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_003_First_launch_screen_check_1
    [Documentation]  tc_AndroidAPP_003_First_launch_screen_check_1
    ...    1. Launch the app
    ...    2. Check the status
    [Tags]   @TCID=WRTM-326ACN-200    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the app
    Check the status

*** Keywords ***
Launch the app
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen
    Remove The Master Account Binding
    Disable DHCP Server
    Click Element    ${Configure_DropAP_btn}
    touch account menu
    touch sign out

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains    Configure DropAP    timeout=30
    Wait Until Page Contains    Change Internet&#10;Connection Type    timeout=30
    Enable DHCP Server
    wait until keyword succeeds    10x    5s    Is Linux Ping Successful    app-lanhost    8.8.8.8

Remove The Master Account Binding
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    Swipe To Up
    touch Remove DropAP
    Wait Until Page Contains Element    ${remove_info}    timeout=60
    touch Remove OK button
    Wait Until Page Contains Element    ${Bind_the_Existing_DropAP_Router_btn_master}    timeout=20

Restore DHCP Server
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Enable DHCP Server
    Close APP

*** comment ***
2018-01-03 Gavin_Chang
Init the script
