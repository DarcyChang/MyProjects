*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${port1}    0
${port2}    65535

*** Test Cases ***
tc_Config_External_system_log_server_port
    [Documentation]  tc_Config_External_system_log_server_port
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Set a new External system log server port value 0, refresh Page and Verify port value Has been changed
    ...    3. Set a new External system log server port value 65535, refresh Page and Verify port value Has been changed
    [Tags]   @TCID=WRTM-326ACN-308    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    Set a new External system log server port value 0, refresh Page and Verify port value Has been changed
    Set a new External system log server port value 65535, refresh Page and Verify port value Has been changed

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Set a new External system log server port value 0, refresh Page and Verify port value Has been changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Log Server Port between 0 and 65535 is Pass or not    web    ${port1}

Set a new External system log server port value 65535, refresh Page and Verify port value Has been changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Log Server Port between 0 and 65535 is Pass or not    web    ${port2}

Check Log Server Port between 0 and 65535 is Pass or not
    [Arguments]    ${b}    ${port}
    input text    ${b}    ${Input_LogServer_port}    ${port}
    cpe click    ${b}    ${System_save}
    #wait save compeletdly
    sleep    2
    Wait Until Keyword Succeeds    3x    2s    click links    ${b}    System
    cpe click    ${b}    ${Logging_tab}
    ${result} =    Get Element Value    ${b}    ${Input_LogServer_port}
    Should Be Equal    ${result}    ${port}

*** comment ***
2017-12-8     Hans_Sun
Init the script
