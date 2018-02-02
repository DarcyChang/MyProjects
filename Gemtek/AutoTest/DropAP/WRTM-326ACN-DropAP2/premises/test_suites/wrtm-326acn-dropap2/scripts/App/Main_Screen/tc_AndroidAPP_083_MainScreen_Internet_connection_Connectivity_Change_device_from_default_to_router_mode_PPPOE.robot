*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Restore Internet Setting

*** Variables ***
${interface}    pppoe-wan
${dut_wan_ip_prefix}    172.18.19

*** Test Cases ***
tc_AndroidAPP_083_MainScreen_Internet_connection_Connectivity_Change_device_from_default_to_router_mode_PPPOE
    [Documentation]  tc_AndroidAPP_083_MainScreen_Internet_connection_Connectivity_Change_device_from_default_to_router_mode_PPPOE
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Internet connection
    ...    3. Select the Router mode.
    ...    4. Input the account and password about PPPOE and press next button
    ...    5. Check the status
    [Tags]   @TCID=WRTM-326ACN-344    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Internet connection
    Select the Router mode
    Input the account and password about PPPOE and press next button
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

Select the Router mode
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Select PPPoE

Input the account and password about PPPOE and press next button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config PPPoE

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Verify Internet Type via DUT    ${interface}    ${dut_wan_ip_prefix}

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
