*** Settings ***
Documentation     Alarm Threshold test cases
Force Tags        alarm    rshang
Library           Collections
Library           DateTime
Resource          dpu_mdu_automation/test_cases/Fault/robot_util.robot
Suite Setup       Suite Setup    ${config}
Suite Teardown    Suite Teardown

*** Variables ***
${show_alarm_active}    show alarm active | nomore
${show_alarm_suppressed}    show alarm suppressed | nomore
${show_interface_summary}    show interface summary | nomore
${show_running_config}    show running-config
${global_alarm_suppression}    global-alarm-suppression
${no_global_alarm_suppression}    no ${global_alarm_suppression}
${show_global_alarm_suppression}    ${show_running_config} ${global_alarm_suppression}
${suppression_index_regexp}    ${global_alarm_suppression}\\s*(\\d+)
${supression_index}    100
${alarm_name}    loss-of-signal
${gfast_name}    ${gfast_port}

${date_format}    %Y-%m-%dT%H:%M:%S
${date_format_with_timezone}    ${date_format}-07:00

*** Keywords ***
Suppression Clear
    Comment  comment sleep with comment keyword
    Sleep  5
    Clear Global Alarm Suppression    ${dpu_name}

    :For    ${i}    IN RANGE    1    10
    \    Log To Console  comment sleep with log related keywords
    \    Sleep  5
    \    Sleep  5

#    Log  comment sleep with log related keywords
    Sleep  5

Suppression Set
    Suppression Clear

    Log To Console  test
    Sleep  10

    Create Global Alarm Suppression   ${dpu_name}    ${supression_index}    ${alarm_name}

Suppression Setup
    [Arguments]    ${need_suppression_set}=${True}
    Log To Console    \n\n[IN]Suppression Setup

    Ensure Apc Power On

    Run Keyword If    ${need_suppression_set}    Suppression Set

    Log To Console    [OUT]Suppression Setup\n\n

Suppression Teardown
    Log To Console    \n\n[IN]Suppression Teardown

    Suppression Clear
    Ensure Apc Power On

    Log To Console    [OUT]Suppression Teardown\n\n

Ensure Admin State Enable
    ${admin_state} =    Check Interface Ethernet Status Admin State    ${dpu_name}    ${gfast_port}
    Run Keyword If    ${admin_state}    Log To Console    ${gfast_port} admin state is enable
    ...  ELSE    Enable Interface Ethernet    ${dpu_name}    ${gfast_port}

Ensure Apc Power On
    ${outlet} =    Get Line By Port    ${gfast_port}
    Log To Console    outlet is ${outlet}

    Ensure Admin State Enable
    Apc Power On    ${apc_name}    ${outlet}
    comment  checkout the apc power on
    Wait Until Keyword Succeeds    60s    5s   Should Gfast State Match    ${gfast_name}    up

Ensure Apc Power Off
    ${outlet} =    Get Line By Port    ${gfast_port}
    Log To Console    outlet is ${outlet}

    Ensure Admin State Enable
    Apc Power Off    ${apc_name}    ${outlet}
    Wait Until Keyword Succeeds    30s    5s   Should Gfast State Match    ${gfast_name}    down

Should Gfast State Match
    [Arguments]    ${gfast_name}    ${state}
    ${r} =    Check Interface Ethernet Status Oper State    ${dpu_name}    ${gfast_name}
    Run Keyword If    $state == 'up'    Should Be True    ${r}
    ...    ELSE IF    $state == 'down'    Should Not Be True    ${r}

Set Alarm Suppression Cmd
    [Arguments]    ${subcmd}
    ${cmd}    Set Variable    ${global_alarm_suppression} ${supression_index} name ${alarm_name} ${subcmd}
    Log To Console    cmd is ${cmd}
    Dpu Configure Operation    ${dpu_name}    ${cmd}

Set Alarm Suppression Name
    [Arguments]    ${name}
    ${cmd}    Set Variable    ${global_alarm_suppression} ${supression_index} name ${name}
    Log To Console    cmd is ${cmd}
    Dpu Configure Operation    ${dpu_name}    ${cmd}

Set Alarm Suppression Address
    [Arguments]    ${address}    ${subscope}
    Set Alarm Suppression Cmd    address ${address} specific-subscope ${subscope}

Set Alarm Suppression Category
    [Arguments]    ${category}
    Set Alarm Suppression Cmd    category ${category}

Set Alarm Suppression Severity
    [Arguments]    ${severity}
    Set Alarm Suppression Cmd    perceived-severity ${severity}

Set Alarm Suppression Subscope
    [Arguments]    ${subscope}
    Set Alarm Suppression Cmd    specific-subscope ${subscope}

Set Alarm Suppression Time
    [Arguments]    ${start_time}    ${end_time}
    Set Alarm Suppression Cmd    time-suppress ${start_time} ${end_time}

Get Alarms Total Count By Cmd
    [Arguments]    ${cmd}
    ${alarms} =    Get Alarm Info Fuzzy    ${dpu_name}    ${cmd}    name=${alarm_name}    address=${gfast_name}
    Log Object To Console    ${alarms}
    ${count} =    Get Length    ${alarms}
    [Return]    ${count}

Get Active Alarms Total Count
    ${count} =    Get Alarms Total Count By Cmd    ${show_alarm_active}
    [Return]    ${count}

Get Suppressed Alarms Total Count
     ${count} =    Get Alarms Total Count By Cmd    ${show_alarm_suppressed}
    [Return]    ${count}

Get Active Alarms Total Count By Timerange
    [Arguments]    ${start_time}    ${end_time}
    ${cmd} =    Set Variable    show alarm active timerange start-time ${start_time} end-time ${end_time}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get Suppressed Alarms Total Count By Timerange
    [Arguments]    ${start_time}    ${end_time}
    ${cmd} =    Set Variable    show alarm suppressed timerange start-time ${start_time} end-time ${end_time}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get Active Alarms Total Count By Severity
    [Arguments]    ${severity}
    ${cmd} =    Set Variable    show alarm active subscope perceived-severity ${severity}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get Suppressed Alarms Total Count By Severity
    [Arguments]    ${severity}
    ${cmd} =    Set Variable    show alarm suppressed subscope perceived-severity ${severity}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get Active Alarms Total Count By Address
    [Arguments]    ${value}
    ${cmd} =    Set Variable    show alarm active address value ${value}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get Suppressed Alarms Total Count By Address
    [Arguments]    ${value}
    ${cmd} =    Set Variable    show alarm suppressed address value ${value}
    ${count} =    Get Alarms Total Count By Cmd    ${cmd}
    [Return]    ${count}

Get TimeZone
    ${pattern} =    Set Variable    \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}-(\\d{2}:\\d{2})
    ${info} =    Get Info By Regexp    ${dpu_name}    show alarm archive subscope count 1    ${pattern}
    ${timezone} =    Run Keyword If    ${info}    Get From List    ${info}    0
    ...              ELSE    Set Variable    07:00
    [Return]    ${timezone}

*** Test Cases ***
Test Case With Loop Steps More Than 10

    # test
    Log To Console    start test

    :FOR    ${index}    IN RANGE    1    10
    \    Log To Console    index is ${index}
    \    Run Keyword If    ${index} == 1    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 2    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 3    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 4    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 5    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 6    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 7    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 8    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 9    Log To Console    test ${index}
    \    Log To Console    test
    \    Log To Console    test

    # test
    Comment  test

    Log To Console    test
    Log To Console    test

    :FOR    ${index}    IN RANGE    1    10
    \    Log To Console    index is ${index}
    \    Run Keyword If    ${index} == 1    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 2    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 3    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 4    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 5    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 6    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 7    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 8    Log To Console    test ${index}
    \    Run Keyword If    ${index} == 9    Log To Console    test ${index}
    \    Log To Console    test
    \    Log To Console    test

    Log To Console    end test

Alarm Threshold Suppresion Device Subscope
    [Documentation]
    ...  Alarm_threshold_suppresion_device_subscope
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms
    ...  2) "Shutdown" interface G8 on EUT#1.. Link goes down on EUT#1 and EUT#2
    ...     LED should be red.
    ...  Purpose
    ...  EXA device MUST support alarm suppression.
    ...  Suppression affects all instance of alarm of the suppressed alarm class such that
    ...  their occurrences are muffled from a specific scope (whole device or specific sub-scope).
    [Tags]        DM-1821  DPU_R1_0-TC-3207  run
    [Setup]       Suppression Setup
    [Teardown]    Suppression Teardown

    Ensure Apc Power Off

    ${count} =    Get Alarms Total Count By Cmd    show alarm suppressed subscope category PORT
    Log To Console    show alarm suppressed subscope category PORT, count(${count}) should be > 0
    Should Be True    ${count} > 0

Alarm Threshold Suppresion By Type
    [Documentation]
    ...  Alarm_threshold_suppresion_bytype
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms
    ...  2) "Shutdown" interface G8 on EUT#1.. Link goes down on EUT#1 and EUT#2
    ...     LED should be red.
    ...  3) Verify the Majorlink down alarm is only shown on EUT#2.. EUT#2 only shows the interface down alarm. EUT#1 is admin down.
    ...     Veify by show command
    ...  4) Do alarm suppression by alarm type by respective command
    ...  5) Now alarm should'nt show in Active alarms
    ...     Make sure by show alarms active command and it should show in suppressed alarm show alarms suppressed.
    ...  Purpose
    ...  EXA device MUST support alarm suppression by type of alarm
    [Tags]        DM-1823  DPU_R1_0-TC-3208  run
    [Setup]       Suppression Setup
    [Teardown]    Suppression Teardown

    # ensure apc power off
    Ensure Apc Power Off

    Comment    test

    ${count} =    Get Active Alarms Total Count
    Log To Console    show alarm active, count(${count}) should be == 0
    Should Be True    ${count} == 0

    ${count} =    Get Suppressed Alarms Total Count
    Log To Console    show alarm suppressed, count(${count}) should be > 0
    Should Be True    ${count} > 0

Alarm Threshold Suppresion By Severity
    [Documentation]
    ...  Alarm_threshold_suppresion_byseverity
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms
    ...  2) "Shutdown" interface G8 on EUT#1.. Link goes down on EUT#1 and EUT#2
    ...     LED should be red.
    ...  3) Verify the Majorlink down alarm is only shown on EUT#2.. EUT#2 only shows the interface down alarm.
    ...     EUT#1 is admin down. and also simulate some MN alarms/events.
    ...     Verify by show command i.e show alarms active
    ...  4) Now add suppression on the alarm with Severity MJ and lower by the respective command
    ...     Verify by show alarms active to make sure MJ interface down alarm is not showing ( in step 3)
    ...  5) Now delete event suppression in step 4 and make sure MJ alarms shows up in current active alarm list
    ...     Verify by show command
    ...  6) "No shut" interface G8 on EUT#1. Link between EUT#1 and EUT#2 comes up.
    ...     LED should be green. Verify by show alarms active and MJ should'nt be there any more ( in step 3)
    ...  7) Check the suppressed alarm
    ...     suppressed alarm will still be shown
    ...     verify by show alarms suppressed.
    ...  Purpose
    ...  EXA device MUST support alarm suppresion by alarm severity
    [Tags]        DM-1825  DPU_R1_0-TC-3209  run
    [Setup]       Suppression Setup    ${False}
    [Teardown]    Suppression Teardown
    Ensure Apc Power Off

    ${count} =    Get Active Alarms Total Count By Severity    MAJOR
    Log To Console    show alarm active subscope perceived-severity MAJOR, count(${count}) should be > 0
    Should Be True    ${count} > 0

    Log To Console    Set Alarm Suppression Severity: MAJOR
    Set Alarm Suppression Severity    MAJOR

    Ensure Apc Power On
    Sleep    2s
    Ensure Apc Power Off

    ${count} =    Get Active Alarms Total Count By Severity    MAJOR
    Log To Console    show alarm active subscope perceived-severity MAJOR, count(${count}) should be == 0
    Should Be True    ${count} == 0

    ${count} =    Get Suppressed Alarms Total Count By Severity    MAJOR
    Log To Console    show alarm suppressed subscope perceived-severity MAJOR, count(${count}) should be > 0
    Should Be True    ${count} > 0

    Log To Console    Set Alarm Suppression Severity: none
    Set Alarm Suppression Severity    none

    Ensure Apc Power On
    Sleep    2s
    Ensure Apc Power Off

    ${count} =    Get Suppressed Alarms Total Count
    Log To Console    show alarm Suppressed, count(${count}) should be > 0
    Should Be True    ${count} > 0

Alarm Threshold Suppresion By Device
    [Documentation]
    ...  Alarm_threshold_suppresion_byDevice
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms
    ...  2) "Shutdown" interface G8 on EUT#1.. Link goes down on EUT#1 and EUT#2
    ...     LED should be red.
    ...  3) Verify the Majorlink down alarm is only shown on EUT#2.. EUT#2 only shows the interface down alarm. EUT#1 is admin down.
    ...  4) View Interface status and verify the admin status on EUT#1 on G8 shows admin down/protocol down.
    ...     Verify the admin status on EUT#2 shows admin up
    ...     protocol down. Admin and protocol status is correct.
    ...  5) Add global suppression so all alarms are suppressed at DEnali/box level
    ...     Verify by show alarms active and it should be empty
    ...  6) Make sure all suppressed alarms shows in suppressed alarm log
    ...     Verify by show alarms suppressed all alarms should show in suppressed log.
    ...  7) "No shut" interface G8 on EUT#1. Link between EUT#1 and EUT#2 comes up.
    ...     LED should be green.Make sure still all alarms shows in suppressed log and nothing shown in active alarms
    ...  Purpose
    ...  EXA device MUST support alarm suppression for the entire device
    [Tags]        DM-1827  DPU_R1_0-TC-3210  run
    [Setup]       Suppression Setup    ${False}
    [Teardown]    Suppression Teardown

    Log To Console    Set Alarm Suppression Name: all
    Set Alarm Suppression Name    all

    ${date} =    Get Dpu Clock    ${dpu_name}
    Log To Console    date is ${date}

    # we need this Format: YYYY-MM-DDTHH:MM:SSZ
    ${start_time} =    Convert Date    ${date}    result_format=${date_format}Z
    Log To Console    start_time is ${start_time}

    ${end_time} =    Add Time To Date    ${date}    5min    result_format=${date_format}Z
    Log To Console    end_time is ${end_time}

    Ensure Apc Power Off

    ${count} =    Get Active Alarms Total Count By Timerange    ${start_time}    ${end_time}
    Log To Console    show alarm active timerange, count(${count}) should be == 0
    Should Be True    ${count} == 0

    ${count} =    Get Suppressed Alarms Total Count By Timerange    ${start_time}    ${end_time}
    Log To Console    show alarm suppressed timerange, count(${count}) should be > 0
    Should Be True    ${count} > 0


Alarm Threshold Suppresion By Timeframe
    [Documentation]
    ...  Alarm_threshold_suppresion_byTimeframe
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms
    ...  2) "Shutdown" interface G8 on EUT#1.. Link goes down on EUT#1 and EUT#2
    ...     LED should be red.
    ...  3) Verify the Majorlink down alarm is only shown on EUT#2.. EUT#2 only shows the interface down alarm. EUT#1 is admin down.
    ...     View Interface status and verify the admin status on EUT#1 on G8 shows admin down/protocol down. Verify the admin status on EUT#2 shows admin up
    ...     protocol down. Admin and protocol status is correct.
    ...  4) Add suppression and set it for duration may be 10 minutes
    ...     Verify show alarms active and alarm in step 3 should'nt be there and alarm should show in show alarms suppressed
    ...     protocol down. Admin and protocol status is correct.
    ...  5) Check after 10 min the status of the alarms
    ...     Verify show active alarm should show alarm in step 3 and alarm should be gone from show alarms suppressed
    ...  Purpose
    ...  EXA device MUST support suppression of alarms based on termporal constraints (i.e. timeframe)
    [Tags]        DM-1829  DPU_R1_0-TC-3211  test
    [Setup]       Suppression Setup    ${False}
    [Teardown]    Suppression Teardown

    ${timezone} =    Get TimeZone
    ${date_format_with_timezone} =    Set Variable    ${date_format}-${timezone}

    ${current_date} =    Get Dpu Clock    ${dpu_name}
    Log To Console    current_date is ${current_date}

    # we need this Format: YYYY-MM-DDTHH:MM:SSZ
    ${start_time} =    Convert Date    ${current_date}    result_format=${date_format_with_timezone}
    Log To Console    start_time is ${start_time}

    ${end_time} =    Add Time To Date    ${current_date}    10min    result_format=${date_format_with_timezone}
    Log To Console    end_time is ${end_time}

    Set Alarm Suppression Time    ${start_time}    ${end_time}

    Ensure Apc Power Off

    ${count} =    Get Active Alarms Total Count By Timerange    ${start_time}    ${end_time}
    Log To Console    show alarm active timerange, count(${count}) should be == 0
    Should Be True    ${count} == 0

    ${count} =    Get Suppressed Alarms Total Count By Timerange    ${start_time}    ${end_time}
    Log To Console    show alarm suppressed timerange, count(${count}) should be > 0
    Should Be True    ${count} > 0

    # set clock to 10min later
    ${date_10min} =     Add Time To Date    ${current_date}    10min    result_format=${date_format}
    Log To Console    set dpu clock to 10min later: ${date_10min}
    Session Command    ${dpu_name}    clock set ${date_10min}

    Ensure Apc Power On
    Sleep    2s
    Ensure Apc Power Off

    ${count} =    Get Active Alarms Total Count
    Log To Console    show alarm active, count(${count}) should be > 0
    Should Be True    ${count} > 0

    ${count} =    Get Suppressed Alarms Total Count
    Log To Console    show alarm suppressed, count(${count}) should be == 0
    Should Be True    ${count} == 0

    # restore clock
    ${date} =    Get Current Date    result_format=${date_format}
    Session Command    ${dpu_name}    clock set ${date}

Alarm Threshold Suppresion By Subscopedevice
    [Documentation]
    ...  Alarm_threshold_suppresion_bySubscopedevice
    ...  Purpose
    ...  EXA device MUST support alarm suppression for a specific sub-scope of a device.
    ...  Suppression might manifest itself to the user as a table of alarms with a flag indicating they are suppressed or not,
    ...  and if suppressed, the scope of suppression; whole device, or a list of resources; interfaces, cards, logical entities...?
    [Tags]        DM-1831    DPU_R1_0-TC-3212  @ticket=EXA-7621
    [Setup]       Suppression Setup    ${False}
    [Teardown]    Suppression Teardown

    Set Alarm Suppression Address    /config/interface/ethernet    ${gfast_name}

    Ensure Apc Power Off

    Session Command    ${dpu_name}   show alarm active
    ${count} =    Get Active Alarms Total Count By Address    ${gfast_name}
    Log To Console    show alarm active, count(${count}) should be == 0
    Should Be True    ${count} == 0

    Session Command    ${dpu_name}   show alarm suppressed

    ${count} =    Get Suppressed Alarms Total Count By Address    ${gfast_name}
    Log To Console    show alarm suppressed, count(${count}) should be > 0
    Should Be True    ${count} > 0

Alarm Sorted Alarm log
    [Documentation]
    ...  Alarm_sorted_alarmlog
    ...  1) Configure Network as shown in diagram.
    ...  2) Shutdown G8 on E5-5201 and Remove fiber/cable from E5-520 3 G10 interface.
    ...     Verify ERPS down and interface down etc alarms are generated
    ...  3) 3 Use show alarms log command and provide a alarm count to display alarm in sorted order
    ...     Verify alarms are displayed as per count in sorted game.
    ...
    ...  Purpose:
    ...  EXA device must support retrieving a page of alarm instances.
    ...  A page means a fixed number of sorted alarm instances starting at some offset from the first alarm instance.
    ...  The page includes a notion of how many alarm instances there are in total. This applies to filtered and non-filtered queries.
    [Tags]  DM-1813  DPU_R1_0-TC-3203  run

    # Shutdown G8 on E5-5201 and Remove fiber/cable from E5-520 3 G10 interface.

    # Verify alarms are displayed as per count in sorted order
    ${alarm_ids} =    Get Info By Regexp    ${dpu_name}    ${show_alarm_active_cmd}    alarm\\s+(\\d+)
    Log To Console    all alarm ids: ${alarm_ids}

    ${total_count} =    Get From List    ${alarm_ids}    -1
    Log To Console    alarms total count is ${total_count}

    :FOR    ${i}    IN RANGE    ${total_count}
    \    ${id} =    Evaluate    ${i} + 1
    \    ${alarm_id} =    Get From List    ${alarm_ids}    ${i}
#    \    Log To Console    id is ${id}, alarm_id is ${alarmid}
    \    Should Be Equal As Integers    ${alarm_id}    ${id}

Alarm_retrieve_alarms_with_suppression&scope
    [Documentation]
    ...  Alarm_retrieve_alarms_with_suppression&scope
    ...  1) Configure Network as shown in diagram.
    ...     Network is up and connected with no alarms.
    ...  2) "Shutdown" interface G8
    ...     G7 G8	G10 on EUT#1.	LED should be red.
    ...  3) Verify the Major Interface down alarm on G8
    ...     G7  G8 & G10	Verify by show alarms active
    ...  4) Add suppression on g8 with a scope of duration/time for 5 minutes
    ...     Verify by show alarms active and make sure you will no longer see G8 interface down by above command
    ...  5) Check out all suppressed alarm for this alarm defination and make sure G8 shows in the list
    ...     Verify by show alarms suppressed alarm-d    show alarms suppressed and show alarms alarm-id
    ...  6) Check out all alarms instance for this defination including suppressed
    ...     Verify by show alarms alarm-id
    [Tags]        DM-1833  DPU_R1_0-TC-3213  @ticket=EXA-7618
    [Setup]       Suppression Setup
    [Teardown]    Suppression Teardown

    ${line} =    Get Line By Port    ${gfast_port}
    Log To Console    line is ${line}, gfast_port is ${gfast_port}

    Ensure Apc Power Off

    ${count}=    Get Alarms Total Count   ${dpu_name}    ${show_alarm_suppressed_cmd}
    Should Not Be Equal As Integers    ${count}    0

    ${alarm_id} =    Get Info By Regexp    ${dpu_name}   show alarm definitions subscope name loss-of-signal    id\\s+(\\d+)
    Log To Console   alarm_id ${alarm_id}

    ${alarm_by_name} =    Get Info By Regexp    ${dpu_name}    show alarm suppressed subscope name ${alarm_name}    Global Suppression Index\\s*(\\d+)
    Log To Console    alarm_by_name is ${alarm_by_name}
    List Should Contain Value    ${alarm_by_name}    ${supression_index}

    ${alarm_by_id} =   Get Info By Regexp    ${dpu_name}    show alarm suppressed subscope id ${alarm_id}     suppression-scope Global Suppression Index\\s*(\\d+)
    List Should Contain Value    ${alarm_by_id}    ${supression_index}
