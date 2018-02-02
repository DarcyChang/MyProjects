*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Jujung_Chang    norun

*** Variables ***

*** Test Cases ***
tc_get_ip
    [Documentation]   tc_get_ip
    ...    1. Create two libraries to get cell value, the library can be called by Wait Until Keyword Succeeds to avoid dynamic java script web data reflash
    ...    2. Table Data Should Not Be Empty will also return cell value when the keyword succeeds
    [Tags]
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Status Page and check Wide Area Network (WAN) table
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    Wait Until Element Is Visible    web    id=conn_tab

    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    1s     Table Data Should Contain    web    xpath=//table[@id='conn_tab']    3    2    Connected

    #Check if there's ip value in the cell and also return the ip value if cell value is not empty
    ${my_ip} =    Wait Until Keyword Succeeds    10x    2s     Table Data Should Not Be Empty    web    xpath=//table[@id='gateway_tab']    10    2
    log    ${my_ip}


*** Keywords ***
Table Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]
    ${cell1}    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Table Data Should Not Be Empty
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is empty, then return cell value.
    ${cell1}    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
    [Return]    ${cell1}
