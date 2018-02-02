*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Disable NTP Server
*** Variables ***


*** Test Cases ***
tc_Config_Provide_NTP_Server
    [Documentation]  tc_Config_Provide_NTP_Server
    ...    1. Go to web page Device Management>System and Beneath Time Synchronization
    ...    2. Click on Provide NTP Server checkbox and save
    ...    3. Refresh Page and verify Provide NTP Server checkbox state has changed
    [Tags]   @TCID=WRTM-326ACN-341    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath Time Synchronization
    Click on Provide NTP Server checkbox and save
    Refresh Page and verify Provide NTP Server checkbox state has changed

*** Keywords ***
Go to web page Device Management>System and Beneath Time Synchronization
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Click on Provide NTP Server checkbox and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Enable NTP Server

Refresh Page and verify Provide NTP Server checkbox state has changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    System
    Checkbox Should Be Selected     web     ${Checkbox_NTPServer}

*** comment ***
2017-11-02     Hans_Sun
Init the script
