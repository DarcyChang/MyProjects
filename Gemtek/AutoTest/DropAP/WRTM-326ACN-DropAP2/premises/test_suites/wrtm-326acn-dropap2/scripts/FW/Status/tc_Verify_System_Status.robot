*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Status    @AUTHOR=Jujung_Chang

*** Variables ***

*** Test Cases ***
tc_Verify_System_Status
    [Documentation]  tc_Verify_System_Status
    ...    1.  Go to webpage Status>Overview
    ...    2.  In the "System" table, Verify below parameters display correctly Hostname, Model, Firmware Version, kernel Version, Local time, Uptime and Load Average
    [Tags]   @TCID=WRTM-326ACN-283    @DUT=WRTM-326ACN     @AUTHOR=Jujung_Chang
    [Timeout]

    Go to webpage Status>Overview
    In the "System" table, Verify below parameters display correctly Hostname, Model, Firmware Version, kernel Version, Local time, Uptime and Load Average

*** Keywords ***
Go to webpage Status>Overview
    [Documentation]  Go to webpage Status>Overview
    [Tags]   @AUTHOR=Jujung_Chang
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview

In the "System" table, Verify below parameters display correctly Hostname, Model, Firmware Version, kernel Version, Local time, Uptime and Load Average
    [Documentation]  Verify System table
    [Tags]   @AUTHOR=Jujung_Chang

    ${hostname}  Get Status->Overview->System->Hostname
    Should Be Equal    ${hostname}    DropAP

    ${model} =  Get Status->Overview->System->Model
    Should Be Equal    ${model}    Gemtek DropAP

    ${FirmwareVersion} =  Get Status->Overview->System->FirmwareVersion
    Go to web page Device Management>Firmware
    ${Device_Management_FirmwareVersion} =  Verify Firmware Version Format in page is x.x.xx
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview
    Should Contain    ${FirmwareVersion}    ${Device_Management_FirmwareVersion}

    ${KernelVersion} =  Get Status->Overview->System->KernelVersion
    Should Not Be Empty    ${KernelVersion}

    ${LocalTime} =  Get Status->Overview->System->LocalTime
    ${Device_Management_System_Time} =  Get Real Time on Device Management>System page
    Wait Until Keyword Succeeds    3x    2s    click links    web    Status  Overview
    Should Contain    ${LocalTime}    ${Device_Management_System_Time}

    ${Uptime} =  Get Status->Overview->System->Uptime
    Should Not Be Empty    ${Uptime}

    ${LoadAverage} =  Get Status->Overview->System->LoadAverage
    Should Not Be Empty    ${LoadAverage}


Go to web page Device Management>Firmware
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  Firmware

Verify Firmware Version Format in page is x.x.xx
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    ${result} =   Get Element Text    web    ${FW_version}
    [Return]    ${result}

Get Real Time on Device Management>System page
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${after_time} =   Get Real Time
    log    ${after_time}
    @{after_times} =  Split String  ${after_time}
    log  ${after_times}
    ${RealTime} =   Set Variable    @{after_times}[3]
    @{RealTime} =   Split String  ${RealTime}    :
    [Return]    @{RealTime}[0]

Get Real Time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    ${result}    Get Element text    web    ${Text_time}
    log    ${result}
    [Return]    ${result}

*** comment ***
2017-11-13     Jujung_Chang
Init the script
