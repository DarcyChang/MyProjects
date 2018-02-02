*** Settings ***

*** Variables ***

*** Keywords ***
Check PPTP_L2TP Connected
    [Arguments]    ${browser}
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen

    # Go to device setting page
    Go To Page     ${browser}    ${l2tp_server_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page2"]/a/span/i[2]
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/span/i[2]
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="l2tp"]/h4/div[1]    1.5    30
    sleep    3s

    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=disconnect@style
    log    ${status}
    Should Not Contain    ${status}    none

    ${status} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    ${browser}    id=connect@style
    log    ${status}
    Should Contain    ${status}    none

Config PPTP_L2TP
    [Arguments]    ${browser}    ${protocol_type}    ${pptp_server}    ${username}    ${password}    ${connection_type}=full    ${start_when_boot}=False    ${force_encryption}=False
    [Documentation]
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen


    # Go to device setting page
    Go To Page     ${browser}    ${l2tp_server_gui_url}/main_pannel_wifi.html
    sleep    3s

    # Click on Internet setting tab
    Wait Until Element Is Visible    ${browser}    xpath=//*[@id="li_page2"]/a/span/i[2]
    Wait Until Keyword Succeeds    5x    2s    cpe click    ${browser}    xpath=//*[@id="li_page2"]/a/span/i[2]
    sleep    3s
    # Expand Port Forwarding section
    Wait Until Keyword Succeeds    15x    2s    cpe click    ${browser}    xpath=//*[@id="l2tp"]/h4/div[1]    1.5    30
    sleep    3s
    Select From List By Value    ${browser}    xpath=//*[@id="proto"]    ${protocol_type}


    Input Text    ${browser}    xpath=//*[@id="server_ipaddr"]    ${pptp_server}
    Input Text    ${browser}    xpath=//*[@id="username"]    ${username}
    Input Text    ${browser}    xpath=//*[@id="pw_ui"]    ${password}

    Run Keyword If    '${connection_type}' == 'full'    Select From List By Index    ${browser}    xpath=//*[@id="defaultroute"]    0
    ...    ELSE    Select From List By Index    ${browser}    xpath=//*[@id="defaultroute"]    1

    # connection_type=1: full, connection_type=0: smart
    Run Keyword If    ${start_when_boot}    select_checkbox    ${browser}    xpath=//*[@id="auto_checkbox"]
    ...    ELSE    unselect_checkbox    ${browser}    xpath=//*[@id="auto_checkbox"]

    Run Keyword If    ${force_encryption}    select_checkbox    ${browser}    xpath=//*[@id="mppe_checkbox"]
    ...    ELSE    unselect_checkbox    ${browser}    xpath=//*[@id="mppe_checkbox"]


    cpe click    ${browser}    xpath=//*[@id="l2tpSaveButton"]

Ping Host IP by GUI
    [Arguments]    ${browser}    ${host_ip}
    [Documentation]    Reboot and Check Login
    [Tags]    @AUTHOR=Gemtek_Thomas_Chen


    # go to sysinfo page
    Go To Page     ${browser}    ${l2tp_server_gui_url}/main_pannel_sysinfo.html
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

*** comment ***
2017-11-08     Gemtek_Jujung_Chang
Copy from wrtm-326acn project.