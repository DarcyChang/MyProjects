*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun

*** Variables ***
${invalid_candidates1}    invalid.server.
${invalid_candidates2}    @#$$%%^
${invalid_candidates3}    abc efg

*** Test Cases ***
tc_Config_NTP_Server_Candidates_invalid_input
    [Documentation]  tc_Config_NTP_Server_Candidates_invalid_input
    ...    1. Go to web page Device Management>System and Beneath Time Synchronization
    ...    2. Input a candidate server value with invalid input content on the last candidate server item on candidate server list and save
    ...    3. Verify the prompt alert has shown and input string should turn red
    [Tags]   @TCID=WRTM-326ACN-345    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath Time Synchronization
    Input a candidate server value with invalid input content on the last candidate server item on candidate server list and save
    Verify the prompt alert has shown and input string should turn red

*** Keywords ***
Go to web page Device Management>System and Beneath Time Synchronization
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Input a candidate server value with invalid input content on the last candidate server item on candidate server list and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_candidates1}    ${invalid_candidates1}
    input text    web    ${Input_candidates3}    ${invalid_candidates2}
    input text    web    ${Input_candidates4}    ${invalid_candidates3}
    cpe click    web    ${System_save}

Verify the prompt alert has shown and input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Page Should Contain Element    web    ${Alert_element}
    Page Should Contain Element    web    ${Red_candidates1}
    Page Should Contain Element    web    ${Red_candidates2}
    Page Should Contain Element    web    ${Red_candidates3}

*** comment ***
2017-11-08     Hans_Sun
Init the script
