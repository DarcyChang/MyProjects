*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${illegal_ip}    266.355.7766.43
${ContainChars_ip}    ave.eee.ss
${WrongFormat_ip_1}    12.4.5.6.3.5
${WrongFormat_ip_2}    13.4.
${WrongFormat_ip_3}    avbe.eed.###.4
${Multicast_ip}    224.0.0.1
${AllZero_ip}    0.0.0.0

*** Test Cases ***
tc_Config_External_system_log_server_with_invalid_IP_value
    [Documentation]  tc_Config_External_system_log_server_with_invalid_IP_value
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Input External system log server with invalid ip value and input string should turn red
    [Tags]   @TCID=WRTM-326ACN-302    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    Input External system log server with invalid ip value and input string should turn red

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Input External system log server with invalid ip value and input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Log Server IP Format is Correct or Not    web    ${illegal_ip}
    Check Log Server IP Format is Correct or Not    web    ${ContainChars_ip}
    Check Log Server IP Format is Correct or Not    web    ${WrongFormat_ip_1}
    Check Log Server IP Format is Correct or Not    web    ${WrongFormat_ip_2}
    Check Log Server IP Format is Correct or Not    web    ${WrongFormat_ip_3}
    Check Log Server IP Format is Correct or Not    web    ${Multicast_ip}
    Check Log Server IP Format is Correct or Not    web    ${AllZero_ip}

Check Log Server IP Format is Correct or Not
    [Arguments]    ${b}    ${input}
    [Tags]   @AUTHOR=Hans_Sun
    input text    ${b}    ${Input_LogServer}    ${input}
    Page Should Contain Element    ${b}    ${InvalidIPHTMLMSG}

*** comment ***
2017-12-8     Hans_Sun
Init the script
