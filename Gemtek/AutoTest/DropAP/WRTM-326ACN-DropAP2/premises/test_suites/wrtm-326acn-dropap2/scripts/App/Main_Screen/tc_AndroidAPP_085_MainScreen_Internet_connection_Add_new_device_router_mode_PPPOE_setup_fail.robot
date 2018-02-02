*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Restore Internet Setting

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_085_MainScreen_Internet_connection_Add_new_device_router_mode_PPPOE_setup_fail
    [Documentation]  tc_AndroidAPP_085_MainScreen_Internet_connection_Add_new_device_router_mode_PPPOE_setup_fail
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Internet connection
    ...    3. Select the router mode > PPPOE
    ...    4. Input the wrong account and pw of PPPOE then press save button
    ...    5. Check the status
    [Tags]   @TCID=WRTM-326ACN-356    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Internet connection
    Select the router mode > PPPOE
    Input the wrong account and pw of PPPOE then press save button
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Internet connection
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Internet Connection

Select the router mode > PPPOE
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Select PPPoE

Input the wrong account and pw of PPPOE then press save button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Wrong PPPoE

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Is Linux Ping Fail    app_lanhost    8.8.8.8

Restore Internet Setting
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Internet Connection
    Config DHCP
    Close APP

*** comment ***
2017-12-26 Gavin_Chang
Init the script
