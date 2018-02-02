*** Settings ***
Resource    base.robot

Force Tags    @FEATURE=System    @AUTHOR=Hans_Sun
*** Variables ***

*** Test Cases ***
tc_Config_Cron_Log_Level
    [Documentation]  tc_Config_Cron_Log_Level
    ...    1. Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    ...    2. Select a new Cron Log Level and Save
    ...    3. Refresh Page and Verify Cron Log Level Has been changed
    [Tags]   @TCID=WRTM-326ACN-319    @DUT=WRTM-326ACN     @AUTHOR=Hans_Sun
    [Timeout]

    Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    Select a new Cron Log Level and Save
    Refresh Page and Verify Cron Log Level Has been changed

*** Keywords ***
Go to web page Device Management>System and Beneath System Properties, select "Logging " Tab
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Login Web GUI
    Wait Until Keyword Succeeds    3x    2s    click links    web    Device Management  System
    cpe click    web    ${Logging_tab}

Select a new Cron Log Level and Save
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Cron Log Level Settings    web    Debug
    Check Cron Log Level Settings    web    Warning

Refresh Page and Verify Cron Log Level Has been changed
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Check Cron Log Level Settings    web    Normal

Check Cron Log Level Settings
    [Arguments]    ${b}    ${input}
    Select From List By Label    web    ${Select_CronLog_level}    ${input}
    cpe click    ${b}    ${System_save}
    #wait save compeletdly
    sleep    2
    Wait Until Keyword Succeeds    3x    2s    click links    ${b}    System
    cpe click    ${b}    ${Logging_tab}
    ${result} =    get_selected_list_label    ${b}    ${Select_CronLog_level}
    Should Be Equal    ${result}    ${input}

*** comment ***
2017-12-12     Hans_Sun
Init the script
