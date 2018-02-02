*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Force Tags    @FEATURE=Main_Screen    @AUTHOR=Gavin_Chang

Test Teardown      Restore Frequency

*** Variables ***
${g_app_username}    wifitest
${g_app_password}    wifitest
${frequency}    2.4GHz
${original_frequency}    2.4GHz & 5GHz
*** Test Cases ***
tc_AndroidAPP_076_MainScreen_Wireless_settings_Edit_Settings_Set_the_Frequency_Only_2.4G
    [Documentation]  tc_AndroidAPP_076_MainScreen_Wireless_settings_Edit_Settings_Set_the_Frequency_Only_2.4G
    ...    1. Launch the DropAP app into main screen
    ...    2. Launch main screen > Device settings icon > Wireless Settings
    ...    3. Change the Frequency(Only 2.4G)
    ...    4. Check the status.
    [Tags]   @TCID=WRTM-326ACN-263    @DUT=WRTM-326ACN     @AUTHOR=Gavin_Chang
    [Timeout]

    Launch the DropAP app into main screen
    Launch main screen > Device settings icon > Wireless Settings
    Change the Frequency(Only 2.4G)
    Check the status

*** Keywords ***
Launch the DropAP app into main screen
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Launch APP
    Sign In
    wait main screen

Launch main screen > Device settings icon > Wireless Settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch Device Settings
    touch Wireless Setting

Change the Frequency(Only 2.4G)
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Change Frequency Bands    ${frequency}
    touch wireless ok
    wait wireless ok

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_home_ssid}
    Wait Until Keyword Succeeds    3x    5x    Verify Wireless Scan With Hidden or not    wifi_client    ${g_app_home_ssid}-5G    yes

Restore Frequency
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Change Frequency Bands    ${original_frequency}
    touch wireless ok
    wait wireless ok
    Close APP

*** comment ***
2017-12-18 Gavin_Chang
Init the script
