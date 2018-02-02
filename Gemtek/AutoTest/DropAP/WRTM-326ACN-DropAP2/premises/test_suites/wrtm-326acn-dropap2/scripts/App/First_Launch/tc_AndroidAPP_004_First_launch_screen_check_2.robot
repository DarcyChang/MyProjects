*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown    Restore DHCP Server

Force Tags    @FEATURE=First_Launch    @AUTHOR=Gavin_Chang

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_004_First_launch_screen_check_2
    [Documentation]  tc_AndroidAPP_004_First_launch_screen_check_2
    ...    1. Launch the app
    ...    2. Check the status
    [Tags]   @TCID=WRTM-326ACN-201    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]
    Launch the app
    Check the status

*** Keywords ***
Launch the app
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Disable DHCP Server
    First Launch

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains    Configure DropAP    timeout=30
    Enable DHCP Server
    wait until keyword succeeds    10x    5s    Is Linux Ping Successful    app-lanhost    8.8.8.8

Restore DHCP Server
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Enable DHCP Server
    Close APP
*** comment ***
2018-01-03 Gavin_Chang
Init the script
