*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***
${Charcters}    abced
${OverNumbers}    9 9
${special_chars}    !@#$%

*** Test Cases ***
tc_Config_System_log_buffer_size_with_invalid_value
    [Documentation]  tc_Config_System_log_buffer_size_with_invalid_value
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Input non-numeric charcter: "abced" in System log buffer size, verify input string should turn red
    ...    3. Input too big number "9 9" in System log buffer size, verify input string should turn red
    ...    4. Input "!@#$%" in System log buffer size, verify input string should turn red
    [Tags]   @TCID=WRTM-326ACN-298    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    #Input non-numeric charcter: "abced" in System log buffer size, verify input string should turn red
    #Input too big number "9 9" in System log buffer size, verify input string should turn red
    Input "!@#$%" in System log buffer size, verify input string should turn red

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Input non-numeric charcter: "abced" in System log buffer size, verify input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_BufferSize}    ${Charcters}
    Page Should Contain Element    web    ${InvalidIPHTMLMSG}

Input too big number "9 9" in System log buffer size, verify input string should turn red
    [Arguments]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_BufferSize}    ${OverNumbers}
    Page Should Contain Element    web    ${InvalidIPHTMLMSG}

Input "!@#$%" in System log buffer size, verify input string should turn red
    [Arguments]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_BufferSize}    ${special_chars}
    Page Should Contain Element    web    ${InvalidIPHTMLMSG}

*** comment ***
2017-12-6     Hans_Sun
Init the script
