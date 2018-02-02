*** Settings ***
Resource    base.robot

*** Variables ***
${Button_SYNC} =    xpath=//*[@id="cbi-system-cfg02e48a-_systime"]/div/input
${Text_time} =    xpath=//*[@id="_systime-clock-status"]
${Select_timezone} =    xpath=//*[@id="cbid.system.cfg02e48a.zonename"]
${System_save} =    xpath=//*[@id="maincontent"]/div/form/div[3]/input[1]
${Language_tab} =    xpath=//*[@id="tab.system.cfg02e48a.language"]/a
${Select_language} =    xpath=//*[@id="cbid.system.cfg02e48a._lang"]
${Checkbox_NTPClinet} =    xpath=//*[@id="cbid.system.ntp.enable"]
${Checkbox_NTPServer} =    xpath=//*[@id="cbid.system.ntp.enable_server"]
${Input_candidates1} =    xpath=//*[@id="cbid.system.ntp.server.4"]
${Input_candidates2} =    xpath=//*[@id="cbid.system.ntp.server.5"]
${Input_candidates3} =    xpath=//*[@id="cbid.system.ntp.server.1"]
${Input_candidates4} =    xpath=//*[@id="cbid.system.ntp.server.2"]
${NTP_Candidate_1} =   xpath=//*[@id="cbid.system.ntp.server.1"]
${NTP_Candidate_2} =   xpath=//*[@id="cbid.system.ntp.server.2"]
${NTP_Candidate_3} =   xpath=//*[@id="cbid.system.ntp.server.3"]
${NTP_Candidate_4} =   xpath=//*[@id="cbid.system.ntp.server.4"]
${Button_candidates} =    xpath=//*[@id="cbi-system-ntp-server"]/div/div/img[4]
${Default_ntp_server}    3.openwrt.pool.ntp.org
${New_ntp_server}    time.stdtime.gov.tw
${Alert_element}    xpath=/html/body/div/div[3]/div[2]/div/form
${Red_candidates1}    css=input[id="cbid.system.ntp.server.4"][class="cbi-input-text cbi-input-invalid"]
${Red_candidates2}    css=input[id="cbid.system.ntp.server.1"][class="cbi-input-text cbi-input-invalid"]
${Red_candidates3}    css=input[id="cbid.system.ntp.server.2"][class="cbi-input-text cbi-input-invalid"]
${Input_hostname} =    xpath=//*[@id="cbid.system.cfg02e48a.hostname"]
${Logging_tab} =    xpath=//*[@id="tab.system.cfg02e48a.logging"]/a
${Input_BufferSize} =    xpath=//*[@id="cbid.system.cfg02e48a.log_size"]
${Input_LogServer} =    xpath=//*[@id="cbid.system.cfg02e48a.log_ip"]
${Input_LogServer_port} =    xpath=//*[@id="cbid.system.cfg02e48a.log_port"]
${Select_LogOutput_level} =    css=select[id="cbid.system.cfg02e48a.conloglevel"]
${Select_CronLog_level} =    css=select[id="cbid.system.cfg02e48a.cronloglevel"]

*** Keywords ***
Get Real Time
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    ${result}    Get Element text    web    ${Text_time}
    log    ${result}
    [Return]    ${result}

Select Timezone By Value
    [Arguments]    ${value}
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_label    web    ${Select_timezone}    ${value}
    sleep    1s
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Select Language By Value
    [Arguments]    ${value}
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    select_from_list_by_value    web    ${Select_language}    ${value}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Enable NTP Client
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    Select Checkbox    web    ${Checkbox_NTPClinet}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Disable NTP Client
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    Unselect checkbox    web    ${Checkbox_NTPClinet}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Enable NTP Server
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    Select Checkbox    web    ${Checkbox_NTPServer}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Disable NTP Server
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    Wait Until Keyword Succeeds    3x    2s    Unselect checkbox    web    ${Checkbox_NTPServer}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Add NTP Server Candidates
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe click    web    ${Button_candidates}
    ${r}  run keyword and return status    Wait Until Element Is Visible    web    ${Input_candidates2}    timeout=5s
    run keyword if    '${r}' == 'False'    Wait Until Keyword Succeeds    5x    1s    Retry Add NTP Server Candidates Button
    input text    web    ${Input_candidates2}    ${New_ntp_server}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Retry Add NTP Server Candidates Button
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    cpe click    web    ${Button_candidates}
    Wait Until Element Is Visible    web    ${Input_candidates2}    timeout=5s

Delete NTP Server Candidates
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    cpe click    web    ${Button_candidates}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Update NTP Server Candidates
    [Documentation]
    [Tags]   @AUTHOR=Hans_Sun
    input text    web    ${Input_candidates1}    ${New_ntp_server}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely

Modify NTP Candidate Name
    [Arguments]    ${NTP_Number}    ${Candidate_Name}
    [Documentation]
    [Tags]   @AUTHOR=Jujung_Chang
    run keyword if    '${NTP_Number}' == '0'    input text    web    ${NTP_Candidate_1}    ${Candidate_Name}
    run keyword if    '${NTP_Number}' == '1'    input text    web    ${NTP_Candidate_2}    ${Candidate_Name}
    run keyword if    '${NTP_Number}' == '2'    input text    web    ${NTP_Candidate_3}    ${Candidate_Name}
    run keyword if    '${NTP_Number}' == '3'    input text    web    ${NTP_Candidate_4}    ${Candidate_Name}
    cpe click    web    ${System_save}
    Wait Until Config Has Applied Completely
