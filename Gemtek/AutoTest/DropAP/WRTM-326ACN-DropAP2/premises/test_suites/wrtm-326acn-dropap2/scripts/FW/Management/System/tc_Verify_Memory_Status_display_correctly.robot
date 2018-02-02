*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Jujung_Chang

*** Variables ***
*** Test Cases ***
tc_Verify_Memory_Status_display_correctly
    [Documentation]  tc_Verify_Memory_Status_display_correctly
    ...    1. Go to webpage Status>Overview
    ...    2. Verify the status of memory correspond the status of real-time DUT

    [Tags]   @TCID=WRTM-326ACN-266    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to webpage Status>Overview
    Verify the status of memory correspond the status of real-time DUT

*** Keywords ***
Go to webpage Status>Overview
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview

Verify the status of memory correspond the status of real-time DUT
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts

    #To compare free memory.The memory that shows in console is bigger than shows on GUI.
    ${Memory_Show_In_Console} =   Get Free Memory In Console
    ${Memory_Show_On_GUI} =   Get Free Memory On GUI
    run keyword if    ${Memory_Show_In_Console}-${Memory_Show_On_GUI} > 1000    Fail    "The free memory difference is too big."

    #To compare total memory.The memory that shows in console is bigger than shows on GUI.
    ${Memory_Show_In_Console} =   Get Total Memory In Console
    ${Memory_Show_On_GUI} =   Get Total Memory On GUI
    run keyword if    ${Memory_Show_In_Console}-${Memory_Show_On_GUI} > 1000    Fail    "The total memory difference is too big."

    #To compare buffer.
    ${Buffer_Show_In_Console} =   Get Buffer In Console
    ${Buffer_Show_On_GUI} =   Get Buffer On GUI
    run keyword if    ${Buffer_Show_In_Console}-${Buffer_Show_On_GUI} > 10    Fail    "The total memory difference is too big."

Get Free Memory In Console
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${r} =  cli    dut1    free
    ${r} =  Get Line    ${r}    2
    @{R} =   Split String    ${r}
    log    @{R}[3]
    ${r} =  Set Variable    @{R}[3]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

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

Get Total Memory In Console
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${r} =  cli    dut1    free
    ${r} =  Get Line    ${r}    3
    @{R} =   Split String    ${r}
    log    @{R}[3]
    ${r} =  Set Variable    @{R}[3]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

Get Total Memory On GUI
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${result} =   Get Element text    web    ${Memory_Total}
    log    ${result}
    @{R} =   Split String    ${result}    kB
    ${r} =  Set Variable    @{R}[0]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

Get Buffer In Console
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${r} =  cli    dut1    free
    ${r} =  Get Line    ${r}    2
    @{R} =   Split String    ${r}
    log    @{R}[3]
    ${r} =  Set Variable    @{R}[5]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

Get Buffer On GUI
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    [Return]    ${r}
    ${result} =   Get Element text    web    ${Buffer}
    log    ${result}
    @{R} =   Split String    ${result}    kB
    ${r} =  Set Variable    @{R}[0]
    log    ${r}
    ${r} =  Convert To Integer    ${r}

*** comment ***
2017-12-12     Jujung_Chang
Init the script
