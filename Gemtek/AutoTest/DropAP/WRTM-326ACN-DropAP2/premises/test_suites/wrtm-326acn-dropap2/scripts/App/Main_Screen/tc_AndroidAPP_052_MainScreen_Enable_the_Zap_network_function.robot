*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown    Check the original ZAP is disable

*** Variables ***

*** Test Cases ***
tc_AndroidAPP_052_MainScreen_Enable_the_Zap_network_function
    [Documentation]  tc_AndroidAPP_052_MainScreen_Enable_the_Zap_network_function
    ...    1. Launch the app then into main screen
    ...    2. Click the button at bottom-right > Zap button
    ...    3. Enable the Zap network function
    ...    4. Check the status
    [Tags]   @TCID=WRTM-326ACN-226    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the app then into main screen
    Click the button at bottom-right > Zap button
    Enable the Zap network function
    Check the status

*** Keywords ***
Launch the app then into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Click the button at bottom-right > Zap button
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch ZAP setting

Enable the Zap network function
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${status}    run keyword and return status    Element Attribute Should Match    ${zap_switch}    checked    false
    return from keyword if    ${status}==False
    touch ZAP Switch
    Change ZAP SSID name    ${g_app_guest_ssid}
    touch ZAP Save
    touch confirm
    wait main screen

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_guest_ssid}


*** comment ***
2017-12-27 Gavin_Chang
1. Restore ZAP only when change be saved.

2017-12-12 Gavin_Chang
Init the script
