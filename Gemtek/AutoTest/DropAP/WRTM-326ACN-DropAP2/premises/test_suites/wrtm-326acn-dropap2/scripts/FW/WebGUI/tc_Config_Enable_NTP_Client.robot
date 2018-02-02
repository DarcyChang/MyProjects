*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***


*** Test Cases ***
tc_Config_Enable_NTP_Client
    [Documentation]  tc_Config_Enable_NTP_Client
    ...    1. Go to web page Device Management>System and Beneath Time Synchronization
    ...    2. Click on enable NTP Client checkbox and save
    ...    3. Refresh Page and verify enable NTP Client checkbox state has changed
    [Tags]   @TCID=WRTM-326ACN-340    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath Time Synchronization
    Click on enable NTP Client checkbox and save
    Refresh Page and verify enable NTP Client checkbox state has changed

*** Keywords ***
Go to web page Device Management>System and Beneath Time Synchronization
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Click on enable NTP Client checkbox and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Enable NTP Client

Refresh Page and verify enable NTP Client checkbox state has changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    System
    Checkbox Should Be Selected     web     ${Checkbox_NTPClinet}

*** comment ***
2017-11-02     Hans_Sun
Init the script
