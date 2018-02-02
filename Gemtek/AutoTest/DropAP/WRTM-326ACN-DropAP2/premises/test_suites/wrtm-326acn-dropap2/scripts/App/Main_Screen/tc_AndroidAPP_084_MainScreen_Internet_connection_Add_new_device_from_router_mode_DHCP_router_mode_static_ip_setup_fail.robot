*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Restore Internet Setting

*** Variables ***
${wrong_static_ipaddr}    1.123.456.700
${wrong_static_netmask}    256.256.256.256
${wrong_static_gateway}    8.8.8.8
${wrong_static_dns1}    1.1.1.1
${wrong_static_dns2}    2.2.2.2

*** Test Cases ***
tc_AndroidAPP_084_MainScreen_Internet_connection_Add_new_device_from_router_mode_DHCP_router_mode_static_ip_setup_fail
    [Documentation]  tc_AndroidAPP_084_MainScreen_Internet_connection_Add_new_device_from_router_mode_DHCP_router_mode_static_ip_setup_fail
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Internet connection
    ...    3. Select the router mode > static IP
    ...    4. Set the incorrect format for IP address, Subnet Mask, Default gateway, Primary DNS, Secondary DNS
    ...    5. Check the status
    [Tags]   @TCID=WRTM-326ACN-352    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Internet connection
    Select the router mode > static IP
    Set the incorrect format for IP address, Subnet Mask, Default gateway, Primary DNS, Secondary DNS
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

Select the router mode > static IP
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Select Static IP

Set the incorrect format for IP address, Subnet Mask, Default gateway, Primary DNS, Secondary DNS
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Config Wrong Static IP

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
