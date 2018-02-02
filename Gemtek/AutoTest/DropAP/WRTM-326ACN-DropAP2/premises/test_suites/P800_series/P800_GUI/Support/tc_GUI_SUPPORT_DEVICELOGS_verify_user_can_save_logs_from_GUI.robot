*** Settings ***
Documentation     Test suite for 844EGUI Test
#Suite Setup       suite_setup
#Suite Teardown    suite_teardown
Test Setup        setup
Test Teardown     teardown
Resource          base.robot
Force Tags        @feature=support
*** Variables ***
${upgrade_timeout}    300
${original_status}    KEEP
${localhost}    linux_host
${log}    logproxy.tar.gz
${log_dir}    ${DEVICES.firefox.auto_download['dir']}
${cmd_rm_log}    rm -rf /tmp/logproxy.tar.gz
*** Test Cases ***
verify_user_can_save_logs_from_GUI
    [Documentation]    [Author:wywang]  844 could be reset to factory settings from GUI
    ...    Step 1: 	access to http://192.168.1.1/html/support/support_device_logs.html
    ...    Step 2:  find and click "savedevicelogs_btn"
    ...    Step 3:  verify log file is saved on local server.
    ...
    [Tags]    @TMS_ID=    @author=wywang    @Contour_ID=    CI=844V_0
    login ont    ${browser}    ${url}    ${username}    ${password}
    cpe click    ${browser}    link=Support
    cpe click    ${browser}    link=Device Logs
    cpe click    ${browser}    xpath=//button[@id="savedevicelogs_btn"]    wait_time=300
    ${cmd_ls_log}    catenate    ls    ${log_dir}
    ${res}=    cli    ${linux_host}    ${cmd_ls_log}
    should contain    ${res}    ${log}


*** Keywords ***
teardown
    ${full_path_log}    catenate    SEPARATER=    ${log_dir}    /    ${log}
    ${cmd_rm_log}    catenate    rm -rf     ${full_path_log}
    ${res}=    cli    ${linux_host}    ${cmd_rm_log}