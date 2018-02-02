*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${buffer_size}    40

*** Test Cases ***
tc_Config_System_log_buffer_size
    [Documentation]  tc_Config_System_log_buffer_size
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. input a valid System log buffer size 40 and save
    ...    3. Refresh Page and Verify System log buffer size Has been changed
    [Tags]   @TCID=WRTM-326ACN-294    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    input a valid System log buffer size 40 and save
    Refresh Page and Verify System log buffer size Has been changed

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

input a valid System log buffer size 40 and save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun

    input text    web    ${Input_BufferSize}    ${buffer_size}
    cpe click    web    ${System_save}
    #wait save compeletdly
    sleep    2

Refresh Page and Verify System log buffer size Has been changed
    [Arguments]
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    System
    cpe click    web    ${Logging_tab}
    ${result} =    Get Element Value    web    ${Input_BufferSize}
    Should Be Equal    ${result}    ${buffer_size}

*** comment ***
2017-12-6     Hans_Sun
Init the script
