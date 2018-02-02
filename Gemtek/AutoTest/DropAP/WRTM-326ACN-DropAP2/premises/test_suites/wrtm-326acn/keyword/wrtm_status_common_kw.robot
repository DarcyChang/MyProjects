*** Settings ***

*** Variables ***

*** Keywords ***
Ping Host IP by GUI 
    [Arguments]    ${browser}    ${host_ip}
    [Documentation]    Reboot and Check Login
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

        
    # go to sysinfo page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    sleep    3s
    
    # click on system setting
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page0"]/a/p
    cpe click    ${browser}    xpath=//*[@id="li_page0"]/a/p
    sleep    3s
    
    # click on ping button
    cpe click    ${browser}    xpath=//*[@id="internet_ping"]/div[2]/button
    sleep    2s
    
    # Input host ip to input box
    Input Text    ${browser}    xpath=//*[@id="ping_target"]    ${host_ip}
    
    sleep    2s
    cpe click    ${browser}    xpath=//*[@id="ping_tool"]/div/div/div[3]/button[2]
    
    sleep    10s
    
    #Wait Until Keyword Succeeds    5x    3s    Element Should Contain    ${browser}    id=ping_process@style    display: none;
    
    ${ping_result}=    Get Element Value    ${browser}    xpath=//*[@id="ping_result_area"]
    
    [Return]    ${ping_result}

Get Firmware Version
    [Arguments]    ${browser}
    [Documentation]    To see if firmware file is shown in the path
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    
    ${version_first}=    Get Element Text    ${browser}    xpath=//*[@id="fw_first"]
    ${version_last}=    Get Element Text    ${browser}    xpath=//*[@id="fw_last"]

    ${fw_version}=    Catenate    SEPARATOR=    ${version_first}    ${version_last}
    # Generate dut_fw_version log so that email can show firmware version when sending by Jenkins
    Run    echo ${fw_version} > ~/dut_fw_version.log
    
    [Return]    ${fw_version}
    
Check Firmware is Available and Get Full Path File Name
    [Arguments]    ${fw_folder}
    [Documentation]    To see if firmware file is shown in the path
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    log    ${fw_folder}
    ${fw_file}=    List Files In Directory    ${fw_folder}
    ${fw_file}=    Get From List     ${fw_file}    0
    log    ${fw_file}
    ${fw_file_full_path}=    Catenate    SEPARATOR=/    ${fw_folder}    ${fw_file}
    File Should Exist    ${fw_file_full_path}
    
    [Return]    ${fw_file_full_path}

Upgrade Firmware via GUI
    [Arguments]    ${browser}    ${fw_name}
    [Documentation]    Upgrade firmware
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    # go to sysinfo page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    sleep    3s
    
    # click on system setting
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page0"]/a/p
    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    3s
    
    choose file    ${browser}    xpath=//*[@id="firmware_upload"]   ${fw_name}
    # click on firmware upgrade button
    cpe click    ${browser}    xpath=//*[@id="fireware_upgrade_start"]    1.5    240
    
    sleep    120s
    Wait Until Element Is Not Visible    web    xpath=//*[@id="processing_modal"]    240    #After upload and reboot finish, web page upgrade button will disappear.
    
    

Reboot Device and Check Login
    [Arguments]    ${browser}    ${device_http_ip}    ${username}    ${password}
    [Documentation]    Reboot and Check Login
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

        
    login ont    ${browser}    ${device_http_ip}    ${username}    ${password}
    
    # go to sysinfo page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    sleep    3s
    
    # click on system setting
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page0"]/a/p
    cpe click    ${browser}    xpath=//*[@id="li_page0"]/a/p
    sleep    3s
    
    # click on reset device button
    cpe click    ${browser}    xpath=//*[@id="area_0"]/ul/li[1]/div[2]/div/button[1]
    sleep    2s
    
    # confirm reset default operation
    cpe click    ${browser}    xpath=//*[@id="restart"]    1.5    60
    
    sleep    40s
    
    wait until keyword succeeds    5 min    15 sec    device is login able    ${browser}    ${device_http_ip}
    login ont    ${browser}    ${device_http_ip}    ${username}    ${password}


Restore Default and Check Login
    [Arguments]    ${browser}    ${device_http_ip}    ${username}    ${password}
    [Documentation]    Restore Default and Check Login
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    login ont    ${browser}    ${device_http_ip}    ${username}    ${password}
    
    # go to sysinfo page
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    sleep    3s
    
    # click on system setting
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page1"]/a/p
    cpe click    ${browser}    xpath=//*[@id="li_page1"]/a/p
    sleep    3s
    
    # click on reset default button
    cpe click    ${browser}    xpath=//*[@id="area_1"]/ul/li[4]/div[2]/button/span
    sleep    3s
    
    # confirm reset default operation
    cpe click    ${browser}    xpath=//*[@id="resetDefaultButton"]    1.5    60
    
    sleep    60s
    #Remove sshhost file. Need to remove 192.168.55.1 entry in the sshhost file after reset default

    Run    sed -i '/192.168.55.1/d' /home/vagrant/.ssh/known_hosts
    
    wait until keyword succeeds    5 min    15 sec    device is login able    ${browser}    ${device_http_ip}
    login ont    ${browser}    ${device_http_ip}    ${username}    ${password}
    
device is login able
    [Arguments]   ${browser}    ${check_url}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_wait_time}
    #close browser     ${browser}
    #open browser      ${browser}
    go to page        ${browser}    ${check_url}
    ${origin_wait_time}    set_implicit_wait_time    ${browser}    5
    # page should be login page which contains 'User Name:' or logined page which contains 'Logout'
    ${status}    run keyword and return status    Page Should Contain Element    ${browser}    xpath=//*[@id="loginuser"]
    return from keyword if    ${status}==True
    ${status}    run keyword and return status    Page Should Contain Element    ${browser}    xpath=//*[@id="loginpass"]
    return from keyword if    ${status}==True
    should be true    ${status}

    
    


Internet Status Should be Down
    [Arguments]    ${browser}    
    [Documentation]    Check Internet Status by style value of internet element
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    ${internet_status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=internet_down@style  
    Should Not Contain    ${internet_status}    display: none;
    ${internet_status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=internet_on@style  
    Should Contain    ${internet_status}    display: none;
    
Internet Status Should be Up
    [Arguments]    ${browser}    
    [Documentation]    Check Internet Status by style value of internet element
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen
    
    Go To Page     ${browser}    ${g_dut_gui_url}/main_pannel_sysinfo.html
    ${internet_status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=internet_down@style  
    Should Contain    ${internet_status}    display: none;
    ${internet_status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=internet_on@style  
    Should Not Contain    ${internet_status}    display: none;

    
    
*** comment ***

