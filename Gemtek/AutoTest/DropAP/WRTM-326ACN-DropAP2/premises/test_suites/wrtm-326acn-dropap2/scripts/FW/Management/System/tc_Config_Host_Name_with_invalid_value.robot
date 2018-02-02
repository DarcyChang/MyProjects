*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***

*** Test Cases ***
tc_Config_Host_Name_with_invalid_value
    [Documentation]  tc_Config_Host_Name_with_invalid_value
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    ...    2. Input special character "Hello%##$World", verify prompt alert should show and the input string should turn red
    ...    3. Input empty in between two words, verify prompt alert should show and the input string should turn red
    [Tags]   @TCID=WRTM-326ACN-288    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    Input special character "Hello%##$World", verify prompt alert should show and the input string should turn red
    Input empty in between two words, verify prompt alert should show and the input string should turn red

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Input special character "Hello%##$World", verify prompt alert should show and the input string should turn red
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_hostname}    Hello%##$World
    Page Should Contain Element    web    ${InvalidIPHTMLMSG}

Input empty in between two words, verify prompt alert should show and the input string should turn red
    [Arguments]
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_hostname}    Hello World
    Page Should Contain Element    web    ${InvalidIPHTMLMSG}

*** comment ***
2017-12-5     Hans_Sun
Init the script
