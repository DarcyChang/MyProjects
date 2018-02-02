*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun

*** Variables ***
${Restore_times}    150
${Default_ssid}    CXNK00040D1E
${Default_net_state}    Enabled
${Default_net_broadcast}    Enabled
${Default_wifi_radio}    On
${Default_wifi_mode}    ac
${Default_frequency}    5GHz
${Default_channel_mode}    Auto Select
${Default_wifi_security}    Enabled
${Default_security_type}    psk+psk2
${Default_MAC_authentication}    Disabled
${Default_WPS}    Enabled
${Default_WPS_type}    Push Button
${Default_WMM}    Enabled
${Default_WMM_power}    Disabled
${Default_packets_received}    0

*** Test Cases ***
tc_GUI-5GWiFi-GUI-Checking Default Settings of Wireless Status 5G
    [Documentation]    tc_GUI-5GWiFi-GUI-Checking Default Settings of Wireless Status 5G
    ...    1.Go to web gui click Restore Defaults button
    ...    2.Wait Restore Defaults is completed
    ...    3.Go to Wireless status page, and check default settings if is correct
    [Tags]    @TCID=STP_DD-TC-10919    @globalid=1526108    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Choose Restore Defaults by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Restore Defaults
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Restore')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Restore')]    ${Restore_times}    #After Restore finish, web page Restore button will display.

    #Go to Status/Wireless page to check Wireless defult settings
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Keyword Succeeds    5x    3s    go_to_page    web    ${g_844fb_gui_url}/html/status/status_wirelessstatus.html
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_value    web    id=id_ssid    4
    ${result} =   Wait Until Keyword Succeeds    5x    3s    get_selected_list_labels    web    xpath=//select[@id='id_ssid']
    Should Contain    ${result}    ${Default_ssid}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    2    2    ${Default_net_state}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    3    2    ${Default_net_broadcast}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    4    2    ${Default_wifi_radio}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    5    2    ${Default_wifi_mode}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    6    2    ${Default_frequency}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Non Empty    web    xpath=//table[@id='gv_statusTabObjID']    7    2
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    8    2    ${Default_channel_mode}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    9    2    ${Default_wifi_security}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    10    2    ${Default_security_type}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    11    2    ${Default_MAC_authentication}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    12    2    ${Default_WPS}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    13    2    ${Default_WPS_type}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    14    2    ${Default_WMM}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    15    2    ${Default_WMM_power}
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Non Empty    web    xpath=//table[@id='gv_statusTabObjID']    16    2
    Wait Until Keyword Succeeds    5x    2s     Cell Data Should Contain    web    xpath=//table[@id='gv_statusTabObjID']    17    2    ${Default_packets_received}

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Cell Data Should Non Empty
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is non empty, then return cell value.
    [Tags]    @AUTHOR=Gemtek_Hans_Sun

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
*** comment ***