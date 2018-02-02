*** Settings ***
Resource          base.robot

*** Keywords ***
gui do ping test
    [Arguments]    ${browser}    ${dest_addr}    ${pkg_size}
    [Documentation]    go to PING test page and do ping test
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=Ping Test
    input_text    ${browser}    xpath=//*[@id="ip_addr"]    ${dest_addr}
    input_text    ${browser}    xpath=//*[@id="packet_size"]    ${pkg_size}
    click_element    ${browser}    xpath=//*[@id="test_btn"]
    #wait the test result
    sleep    5
    Wait Until Element Is Enabled    ${browser}    xpath=//*[@id="test_btn"]    timeout=30

gui verify ping test
    [Arguments]    ${browser}    ${dest_addr}    ${pkg_size}
    [Documentation]    Check the ping test result
    : FOR    ${i}    IN RANGE    ${4}
    \    ${row}=    evaluate    ${i}+2
    \    #${real_pktsize}=    evaluate    ${pkg_size}+8
    \    ${value_bytes}    run webgui keyword with timeout    2    Get Table Cell    ${browser}    xpath=//*[@id="result_tbl"]
    \    ...    ${row}    2
    \    Log    the No:${i} return Bytes is ${value_bytes}
    \    #${value_bytes_int}=    Convert To Integer    ${value_bytes}
    \    Should Be Equal As Integers    ${value_bytes}    ${pkg_size}

gui get ping time average
    [Arguments]    ${browser}
    [Documentation]    Check the ping test result
    ${time_amount}=    Set Variable    0
    : FOR    ${i}    IN RANGE    ${4}
    \    ${row}=    evaluate    ${i}+2
    \    ${value_time}    run webgui keyword with timeout    2    Get Table Cell    ${browser}    xpath=//*[@id="result_tbl"]
    \    ...    ${row}    3
    \    Log    the No:${i} return time is ${value_time}
    \    ${value_time_int}=    Convert To Number    ${value_time}
    \    Should Not Be Equal    ${value_time_int}    0
    \    ${time_amount}=    evaluate    ${time_amount}+${value_time_int}
    ${time_average}=    evaluate    ${time_amount}/4
    [Return]    ${time_average}

gui traceroute do test
    [Arguments]    ${browser}    ${dest_addr}    ${mode}
    [Documentation]    go to traceroute test page and do test
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=Traceroute
    ${nee_cancel}=    Run Keyword And Return Status    Page Should Contain Element    ${browser}    xpath=//button[text()="Start Trace"]
    Run Keyword Unless    ${nee_cancel}    click_element    ${browser}    xpath=//button[text()="Cancel"]
    Wait Until Page Contains Element    ${browser}    xpath=//button[text()="Start Trace"]
    input_text    ${browser}    xpath=//*[@id='ip_addr']    ${dest_addr}
    #input_text    ${browser}    xpath=//*[@id="packet_size"]    ${pkg_size}
    click_element    ${browser}    xpath=//button[text()="Start Trace"]

gui traceroute verify test result
    [Arguments]    ${browser}    ${row}    ${column}
    [Documentation]    go to traceroute test page and do test
    ${value_time}    run webgui keyword with timeout    2    Get Table Cell    ${browser}    xpath=//*[@id='result_tbl']    ${row}
    ...    ${column}
    ${re_result_pass}    Run Keyword And Return Status    Should Match Regexp    ${value_time}    [\\s\\S]*\d*.\d*[\\s\\S]*ms[\\s\\S]*
    ${re_result_timeout}    Run Keyword And Return Status    Should Match Regexp    ${value_time}    [\\s\\S]*[*][\\s\\S]*
    ${return_result}=    Run Keyword If    ${re_result_pass}    Set Variable    PASS
    ...    ELSE IF    ${re_result_timeout}    Set Variable    TIMEOUT
    ...    ELSE    Set Variable    FAIL
    [Return]    ${return_result}

set reboot behavior
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}    ${behavior}
    [Documentation]    [Author:aijiang] set reboot behavior, clear or save after reboot
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | hostname | hostname of ipaddress |
    ...    | behavior | behavior after reboot, clear or save |
    ...
    ...    Example:
    ...    | set reboot behavior | firefox | http://192.168.1.1 | support | support | clear
    Should Match Regexp    ${behavior}    save|clear
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=System Log
    RUN KEYWORD IF    '${behavior}'=='save'    select radio button    ${browser}    logclear    save
    ...    ELSE    select radio button    ${browser}    logclear    clear

check system log is empty
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:aijiang] check system log is empty
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | hostname | hostname of ipaddress |
    ...
    ...    Example:
    ...    | check system log is empty | firefox | http://192.168.1.1 | support | support
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=System Log
    element should contain    ${browser}    xpath=//table[@id='sys_log_table']    No Entries Defined

check system log is not empty
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:aijiang] check system log is not empty
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...    | hostname | hostname of ipaddress |
    ...
    ...    Example:
    ...    | check system log is empty | firefox | http://192.168.1.1 | support | support
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=System Log
    element should not contain    ${browser}    xpath=//table[@id='sys_log_table']    No Entries Defined

restore cfg
    [Arguments]    ${browser}    ${ontip}
    [Documentation]    [Author:aijiang] restore 844 from a saved cfg file via gui
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...
    ...    Example:
    ...    | restore cfg | firefox | /tmp/backupconfig.cfg |
    ${filepath}    evaluate     '${log_dir}' + '/backupsettings.conf'
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=Configuration Save
    select radio button    ${browser}    backup_restore    Restore
    execute javascript    ${browser}    document.getElementById("fileUploadFrameObjId").style.display='block'
    select_frame    ${browser}    id=fileUploadFrameObjId
    choose file    ${browser}    id=file_restore_field    ${filepath}
    unselect_frame    ${browser}
    cpe click    ${browser}    xpath=//button[contains(., "Restore")]
    wait until keyword succeeds    30x    10s    element_should_not_be_visible    ${browser}    id=darkenScreenObject
    wait until keyword succeeds    5 min    15 sec    ont is login able    ${browser}    ${ontip}

