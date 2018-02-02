*** Settings ***
Documentation     Test suite for 800E GUI
#Suite Setup
#Suite Teardown
#Test Setup
#Test Teardown
Resource          base.robot
Resource          keywords.robot
Force Tags        @feature=utilities

*** Variables ***
#${device}     linux_host
${log_dir}     ${DEVICES.firefox.auto_download['dir']}

*** Test Cases ***
GUI_UTILITIES_Checking_Default_Settings_of_System_log_page
    [Documentation]  Checking Log Save Function.
    ...    Step 1: Open GUI system log page, click “Save Log” and verify the result.
    ...
    ...    Expect Result:
    ...    Save the system log as a CSV file, file name is “syslog.conf” by default; Contents of the file match the log table.

    [Tags]    @TMS_ID=    @author=bfan    @Contour_ID=    CI=844V_0

    login ont     ${browser}    ${url}    ${username}    ${password}
    cpe click     ${browser}    link=Utilities
    cpe click     ${browser}    link=System Log
    log to console     ${log_dir}

#    ${RC}    run webgui keyword with timeout    1    get table rows and columns count    ${browser}    xpath=//table[@id='sys_log_table']
#    Log to console    ${RC}
#    ${row}=    evaluate   ${RC}[0]
#    log to console   ${row}

    ${cell1}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='sys_log_table']    2    1
    log to console    ${cell1}

    RUN KEYWORD IF    '${cell1}'=='No Entries Defined'       Get file informaion     ${browser}    ${linux_host}
    ...    ELSE    Get cell information    ${browser}     ${linux_host}

    [Teardown]    teardown   ${linux_host}

*** Keywords ***
teardown
    [Arguments]    ${linux_host}
    [Documentation]    [Author:bfan] Delete the syslog file in VM
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | linux_host | linux shell |

    ...    Example:
    ...    | teardown | SHELL1
    ${path}     evaluate     '${log_dir}' + '/syslog.conf'
    log to console   ${path}
    #cli    ${linux_host}     cd ${log_dir}
    cli    ${linux_host}     rm -rf ${path}


Get file informaion
    [Arguments]    ${browser}    ${linux_host}
    [Documentation]    [Author:bfan]   Get the syslog information in VM
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | linux_host | linux shell |
    ...
    ...    Example:
    ...    | Get file informaion | firefox | SHELL1
    ${path}     evaluate     '${log_dir}' + '/syslog.conf'
    log to console   ${path}
    cpe click     ${browser}    xpath=//button[contains(., "Save Log")]
    ${res1}     cli    ${linux_host}    head -n 1 ${path}
    log to console    ${res1}
    should match regexp     ${res1}    \\s0\\s
#    Log to console      ${res1]
#    ${res}    Convert to string    ${res1}
#    should be empty   ${res}

Get cell information
    [Arguments]    ${browser}     ${linux_host}
    [Documentation]    [Author:bfan]  Get first row information in table
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | row | the row count of syslog table |
    ...    | linux_host | linuxshell |

    ...    Example:
    ...    | Get cell information | firefox | 5 | SHELL1
    ${path}     evaluate     '${log_dir}' + '/syslog.conf'
    log to console   ${path}
    ${cell1}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='sys_log_table']    2    1
    log to console    ${cell1}
    ${cell2}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='sys_log_table']    2    2
    log to console    ${cell2}
    ${cell3}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='sys_log_table']    2    3
    log to console    ${cell3}
    ${cell4}    run webgui keyword with timeout    1    get table cell    ${browser}    xpath=//table[@id='sys_log_table']    2    4
    log to console    ${cell4}
    ${first_row1}=     catenate   ${cell1}  ${cell2}  ${cell3}  ${cell4}
    log to console    ${first_row1}
    ${first_row}    Convert to string    ${first_row1}

    cpe click     ${browser}    xpath=//button[contains(., "Save Log")]
    ${res1}     cli    ${linux_host}     head -n 1 ${path}
    ${res}    Convert to string    ${res1}

    should contain     ${res}    ${first_row}



