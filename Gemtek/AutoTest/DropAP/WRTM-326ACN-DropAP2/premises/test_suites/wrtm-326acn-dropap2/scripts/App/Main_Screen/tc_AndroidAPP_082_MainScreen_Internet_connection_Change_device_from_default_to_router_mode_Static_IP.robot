*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Restore Internet Setting

*** Variables ***
${interface}    eth0.2

*** Test Cases ***
tc_AndroidAPP_082_MainScreen_Internet_connection_Change_device_from_default_to_router_mode_Static_IP
    [Documentation]  tc_AndroidAPP_082_MainScreen_Internet_connection_Change_device_from_default_to_router_mode_Static_IP
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Internet connection
    ...    3. Select the Router mode
    ...    4. Set the static IP and press next button
    ...    5. Check the status
    [Tags]   @TCID=WRTM-326ACN-335    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Internet connection
    Select the Router mode
    Set the static IP and press next button
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
    Select Static IP

Set the static IP and press next button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Static IP

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Verify Internet Type via DUT    ${interface}    ${g_dut_static_ipaddr}

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
