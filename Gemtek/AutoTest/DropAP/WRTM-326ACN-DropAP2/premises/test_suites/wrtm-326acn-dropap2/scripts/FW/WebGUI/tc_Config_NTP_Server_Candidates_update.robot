*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Recover NTP Server Settings
*** Variables ***


*** Test Cases ***
tc_Config_NTP_Server_Candidates_update
    [Documentation]  tc_Config_NTP_Server_Candidates_update
    ...    1. Go to web page Device Management>System and Beneath Time Synchronization
    ...    2. Input a candidate server value on one candidate server item on candidate server list and save
    ...    3. Refresh Page and verify the candidate server value we just input has applied on the list
    [Tags]   @TCID=WRTM-326ACN-343    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath Time Synchronization
    Input a candidate server value on one candidate server item on candidate server list and save
    Refresh Page and verify the candidate server value we just input has applied on the list

*** Keywords ***
Go to web page Device Management>System and Beneath Time Synchronization
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Input a candidate server value on one candidate server item on candidate server list and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Update NTP Server Candidates

Refresh Page and verify the candidate server value we just input has applied on the list
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element Value    web    ${Input_candidates1}
    Should Be Equal    ${result}    ${New_ntp_server}

Recover NTP Server Settings
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_candidates1}    ${Default_ntp_server}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

*** comment ***
2017-11-03     Hans_Sun
Init the script
