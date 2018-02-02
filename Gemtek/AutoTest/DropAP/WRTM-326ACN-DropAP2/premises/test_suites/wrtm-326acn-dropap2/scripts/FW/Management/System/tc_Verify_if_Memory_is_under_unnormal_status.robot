*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Jujung_Chang

*** Variables ***
${Free_Memory}
*** Test Cases ***
tc_Verify_if_Memory_is_under_unnormal_status
    [Documentation]  tc_Verify_if_Memory_is_under_unnormal_status
    ...    1. Go to webpage Status>Overview
    ...    2. Read the status of memory volume
    ...    3. If the remaining memory volume is greater than 40000kb, test PASS.

    [Tags]   @TCID=WRTM-326ACN-274    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to webpage Status>Overview
    Read the status of memory volume
    If the remaining memory volume is greater than 40000kb, test PASS

*** Keywords ***
Go to webpage Status>Overview
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview

Read the status of memory volume
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${r} =  Get Free Memory On GUI
    Set Global Variable    ${Free_Memory}    ${r}

If the remaining memory volume is greater than 40000kb, test PASS
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang

    run keyword if    ${Free_Memory} < 40000     Fail    "The free memory is unnormal."

Get Free Memory On GUI
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${result} =   Get Element text    web    ${Memory_Free}
    log    ${result}
    @{R} =   Split String    ${result}    kB
    ${r} =  Set Variable    @{R}[0]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

*** comment ***
2017-12-14     Jujung_Chang
Init the script
