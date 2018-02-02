*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=Web_GUI    @AUTHOR=Hans_Sun
Suite Setup    Run keywords    Changed DUT's time by SSH
*** Variables ***


*** Test Cases ***
tc_Local_Time_SYNC_WIth_Browser
    [Documentation]  tc_Local_Time_SYNC_WIth_Browser
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    ...    2. Click SYNC WITH BROWSER Button
    ...    3. Verify Local Time Value has updated to current time
    [Tags]   @TCID=WRTM-326ACN-328    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    Click SYNC WITH BROWSER Button after Changed DUT's time by SSH
    Verify Local Time Value has updated to current time

*** Keywords ***
Changed DUT's time by SSH
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cli    vm1    sed -i /192.168/d /home/vagrant/.ssh/known_hosts
    ${dut_time}    cli    dut1    date 11:11:11
    ${dut_time}    Get Line    ${dut_time}    1
    log    ${dut_time}
    @{dut_times}  Split String  ${dut_time}
    log  ${dut_times}
    Set Suite Variable    @{dut_times}    @{dut_times}

Go to web page Device Management>System and Beneath System Properties, select "General Settings" Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System

Get Real Time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element text    web    ${Text_time}
    log    ${result}
    [Return]    ${result}

Click SYNC WITH BROWSER Button after Changed DUT's time by SSH
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe click    web    ${Button_SYNC}
    #wait sync up time for GUI
    sleep    5

Verify Local Time Value has updated to current time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    5x    1s    Check Real Time Had Changed

Check Real Time Had Changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${after_time}    Get Real Time
    log    ${after_time}
    @{after_times}  Split String  ${after_time}
    log  ${after_times}
    Should Not Be Equal    @{dut_times}[3]    @{after_times}[3]

*** comment ***
2017-11-06     Hans_Sun
Use date command to check function of SYNC WITH BROWSER Button is succeed

2017-10-30     Hans_Sun
Init the script
