*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Recover NTP Server Settings
*** Variables ***


*** Test Cases ***
tc_Config_NTP_Server_Candidates_delete
    [Documentation]  tc_Config_NTP_Server_Candidates_delete
    ...    1. Go to web page Device Management>System and Beneath Time Synchronization
    ...    2. Click on delete button of the candidate server item we just added and save
    ...    3. Refresh Page and verify the candidate server has been deleted from list
    [Tags]   @TCID=WRTM-326ACN-346    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath Time Synchronization
    Click on delete button of the candidate server item we just added and save
    Refresh Page and verify the candidate server has been deleted from list

*** Keywords ***
Go to web page Device Management>System and Beneath Time Synchronization
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Click on delete button of the candidate server item we just added and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Add NTP Server Candidates
    ${result}    Get Element Value    web    ${Input_candidates1}
    Set Test Variable    ${old_ntp_server}    ${result}
    Delete NTP Server Candidates

Refresh Page and verify the candidate server has been deleted from list
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element Value    web    ${Input_candidates1}
    Should Not Be Equal    ${result}    ${old_ntp_server}

Recover NTP Server Settings
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_candidates1}    ${Default_ntp_server}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

*** comment ***
2017-11-02     Hans_Sun
Init the script
