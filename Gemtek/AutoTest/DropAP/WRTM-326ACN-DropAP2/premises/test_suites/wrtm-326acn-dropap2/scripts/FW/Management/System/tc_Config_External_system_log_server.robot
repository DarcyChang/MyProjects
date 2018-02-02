*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${LogServer_ip}    10.5.182.254

*** Test Cases ***
tc_Config_External_system_log_server
    [Documentation]  tc_Config_External_system_log_server
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Input a valid external system log server ip and save
    ...    3. Refresh Page and Verify External system log server Has been changed
    [Tags]   @TCID=WRTM-326ACN-300    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    Input a valid external system log server ip and save
    Refresh Page and Verify External system log server Has been changed

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Input a valid external system log server ip and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun

    input text    web    ${Input_LogServer}    ${LogServer_ip}
    cpe click    web    ${System_save}
    #wait save compeletdly
    sleep    2

Refresh Page and Verify External system log server Has been changed
    [Arguments]
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    System
    cpe click    web    ${Logging_tab}
    ${result} =    Get Element Value    web    ${Input_LogServer}
    Should Be Equal    ${result}    ${LogServer_ip}

*** comment ***
2017-12-7     Hans_Sun
Init the script
