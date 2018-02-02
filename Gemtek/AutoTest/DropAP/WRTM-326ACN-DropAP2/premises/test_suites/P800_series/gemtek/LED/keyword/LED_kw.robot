*** Settings ***

*** Variables ***

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Cell Value Should Be Empty
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is empty.
    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Length Should Be    ${cell1}    0

Get Non Empty Cell Value
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    [Documentation]    the keyword use get_table_cell keyword to retrieve cell value and check if it is non empty, then return cell value.
    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Not Be Empty    ${cell1}
    [Return]    ${cell1}

reboot system
    [Arguments]    ${browser}    ${ontip}    ${username}    ${password}
    [Documentation]    [Author:aijiang] Reboot system via ONT GUI
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | browser name setting in your yaml |
    ...    | ontip | ONT GUI IP |
    ...    | username | username to login the ONT GUI |
    ...    | password | password to login the ONT GUI |
    ...
    ...    Example:
    ...    | reboot system | firefox | http://192.168.1.1 | support | support
    login ont    ${browser}    ${ontip}    ${username}    ${password}
    cpe click    ${browser}    link=Utilities
    cpe click    ${browser}    link=Reboot
    Wait Until Keyword Succeeds    5x    2s     cpe click    ${browser}    xpath=//button[contains(.,"Reboot")]
    Wait Until Keyword Succeeds    5x    2s     cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    sleep    30
    wait until keyword succeeds    5 min    15 sec    ont is login able    ${browser}    ${ontip}
