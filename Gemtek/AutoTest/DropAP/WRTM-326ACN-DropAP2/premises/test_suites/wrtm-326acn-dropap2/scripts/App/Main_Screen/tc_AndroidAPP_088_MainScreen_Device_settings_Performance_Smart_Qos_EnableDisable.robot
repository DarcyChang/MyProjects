*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Leo_Li

Test Teardown    Close APP

*** Variables ***


*** Test Cases ***
tc_AndroidAPP_088_MainScreen_Device_settings_Performance_Smart_Qos_EnableDisable
    [Documentation]  tc_AndroidAPP_088_MainScreen_Device_settings_Performance_Smart_Qos_EnableDisable
    ...    1. Launch the DropAP app into main screen.
    ...    2. Launch main screen > Device settings icon > Performance.
    ...    3. Enable the Performance.
    ...    4. Force close the APP then relaunch again.
    ...    5. Launch main screen > Device settings icon > Performance
    ...    6. Disable the Performance
    ...    7. Force close the APP then relaunch again
    ...    8. Check the status
    [Tags]   @TCID=WRTM-326ACN-374    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Performance
    Enable the Performance
    Force close the APP then relaunch again
    Second Launch main screen > Device settings icon > Performance    #same name defined multiple times
    Disable the Performance
    Second Force close the APP then relaunch again                    #same name defined multiple times
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Performance
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch Device Settings
    touch Performance Control

Enable the Performance
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Check the original Performance status
    Click Element    ${performance_control_switch}
    Wait Until Page Contains Element    ${performance_control_switch}    timeout=10
    Check the Enable Performance status

Check the original Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${original_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${original_performance_status}
    set test variable    ${original_performance_status}    ${original_performance_status}

Check the Enable Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Enable_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${Enable_performance_status}
    Should Not Contain    ${Enable_performance_status}    ${original_performance_status}
    set test variable    ${Enable_performance_status}    ${Enable_performance_status}

Force close the APP then relaunch again
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Close APP

Second Launch main screen > Device settings icon > Performance
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    touch Device Settings
    touch Performance Control

Disable the Performance
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${performance_control_switch}
    Wait Until Page Contains Element    ${performance_control_switch}    timeout=10

Second Force close the APP then relaunch again
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Close APP

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Sign In
    wait main screen
    touch Device Settings
    touch Performance Control
    Check the Disable Performance status

Check the Disable Performance status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${Disable_performance_status}    Get Element Attribute    ${performance_control_switch}    checked
    log    ${Disable_performance_status}
    Should Not Contain    ${Disable_performance_status}    ${Enable_performance_status}

*** comment ***
2017-12-22 Gavin_Chang
1. Rename script to replace special character with underline.

2017-12-19    Leo_Li
Init the script