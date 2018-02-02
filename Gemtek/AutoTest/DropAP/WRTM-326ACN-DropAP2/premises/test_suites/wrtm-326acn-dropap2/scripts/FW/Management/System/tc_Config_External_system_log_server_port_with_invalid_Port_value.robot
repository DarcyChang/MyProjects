*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${port1}    65536
${port2}    jujung

*** Test Cases ***
tc_Config_External_system_log_server_port_with_invalid_Port_value
    [Documentation]  tc_Config_External_system_log_server_port_with_invalid_Port_value
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Set a new External system log server port value with invalid port number "65536", verify input string should turn red
    ...    3. Set a new External system log server port value with invalid port number "jujung", verify input string should turn red
    [Tags]   @TCID=WRTM-326ACN-311    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    Set a new External system log server port value with invalid port number "65536", verify input string should turn red
    Set a new External system log server port value with invalid port number "jujung", verify input string should turn red

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Set a new External system log server port value with invalid port number "65536", verify input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Log Server Port Format is Correct or Not    web    ${port1}

Set a new External system log server port value with invalid port number "jujung", verify input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Log Server Port Format is Correct or Not    web    ${port2}

Check Log Server Port Format is Correct or Not
    [Arguments]    ${b}    ${port}
    [Tags]   @AUTHOR=Hans_Sun
    input text    ${b}    ${Input_LogServer_port}    ${port}
    Page Should Contain Element    ${b}    ${InvalidIPHTMLMSG}

*** comment ***
2017-12-8     Hans_Sun
Init the script
