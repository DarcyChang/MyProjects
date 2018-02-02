*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
Suite Teardown    Run keywords    Recover Hostname Value
*** Variables ***
${hostname}    JujungDrop

*** Test Cases ***
tc_Config_Host_Name_value
    [Documentation]  tc_Config_Host_Name_value
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    ...    2. Input Hostname value and Save Setting
    ...    3. Go to web page Status>Overview
    ...    4. Verify new hostname was set by hostname value should be updated beneath System table
    [Tags]   @TCID=WRTM-326ACN-284    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    Input Hostname value and Save Setting
    Go to web page Status>Overview
    Verify new hostname was set by hostname value should be updated beneath System table

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Input Hostname value and Save Setting
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun

    input text    web    ${Input_hostname}    ${hostname}
    cpe click    web    ${System_save}
    #wait save compeletdly
    sleep    2

Go to web page Status>Overview
    [Arguments]
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview

Verify new hostname was set by hostname value should be updated beneath System table
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${value} =    Get Status->Overview->System->Hostname
    Should Be Equal    ${value}    ${hostname}

Recover Hostname Value
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    input text    web    ${Input_hostname}    DropAP
    cpe click    web    ${System_save}
    #wait save compeletdly
    sleep    2

*** comment ***
2017-12-5     Hans_Sun
Init the script
