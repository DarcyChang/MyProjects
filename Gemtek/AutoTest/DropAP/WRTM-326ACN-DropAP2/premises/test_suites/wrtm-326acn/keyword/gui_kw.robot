*** Settings ***

*** Variables ***

*** Keywords ***
t801f_gui_get_text_from_about_window
    [Arguments]    ${browser}    ${value_type}
    [Documentation]    [Author:syan]    Description:Get the text of hardware/software information (e.g. Model, Release) on 801f gui "About" popup window.
    ...            args:
    ...    browser: session name
    ...    value_type: Model:| Serial Number:| FSAN Number:| Release:| Mac Address:
    ...    Examples:| t801f_gui_get_text_from_about_window | 801f | Release: |

    &{position_dict}    Create dictionary    Model:=2    Serial Number:=4    FSAN Number:=6    Release:=8    Mac Address:=10
    ${position}    get from dictionary    ${position_dict}    ${value_type}
    ${locator}    set variable    xpath=//span[text()='${value_type}']/parent::div/span[${position}]
    log to console    ${locator}
    wait_until_page_contains_element    ${browser}    ${locator}    10
    capture_page_screenshot     ${browser}
    ${value}    get element text    ${browser}    ${locator}
    log to console    ${value}
    [Return]    ${value}

login ont
    [Documentation]  [Author:wywang] login ont in ${url} page with ${username} and ${password}
    [Arguments]     ${browser}    ${url}    ${username}    ${password}
    delete all cookies    ${browser}
    go_to_page    ${browser}    ${url}
    input_text    ${browser}    name=Username    ${username}
    input_text    ${browser}    name=Password    ${password}
    cpe click    ${browser}    xpath=//button[contains(., 'Login')]
    page should contain element    ${browser}    link=Logout

login ont should fail
    [Documentation]  [Author:david qian] login ont in ${url} page with ${username} and ${password} should be failed
    [Arguments]    ${browser}    ${url}    ${username}    ${password}
    delete all cookies    ${browser}
    go_to_page    ${browser}    ${url}
    input_text    ${browser}    name=Username    ${username}
    input_text    ${browser}    name=Password    ${password}
    cpe click    ${browser}    xpath=//button[contains(., 'Login')]
    page should not contain element    ${browser}    link=Logout

cpe click
    [Documentation]  [Author:david qian] Click visible element and wait the action finished, ${wait_time} is timeout value for finding element
    [Arguments]    ${browser}    ${locator}    ${search_time}=1.7    ${wait_time}=60
    click visible element    ${browser}    ${locator}

wait action finish
    [Documentation]  [Author:david qian] Wait action finish by checking element which id is darkenScreenObject is not displayed
    [Arguments]    ${browser}    ${elem_locator}     ${search_time}     ${wait_time}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_wait_time}
    ${origin_wait_time}    set_implicit_wait_time    ${browser}    ${search_time}
    # check whether the object exist
    ${block_exist}    run keyword and return status    page_should_contain_element    ${browser}    ${elem_locator}
    return from keyword if  ${block_exist}==False
    # wait until element not visible
    set_implicit_wait_time    ${browser}    ${origin_wait_time}

    run keyword if    ${block_exist}      wait_until_element_is_not_visible    ${browser}    ${elem_locator}    ${wait_time}

ont is login able
    [Documentation]  [Author:david qian]
    [Arguments]   ${browser}    ${check_url}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_wait_time}
    go to page    ${browser}    ${check_url}
    ${origin_wait_time}    set_implicit_wait_time    ${browser}    5
    # page should be login page which contains 'User Name:' or logined page which contains 'Logout'
    ${status}    run keyword and return status    page should contain text    ${browser}    User Name:
    return from keyword if    ${status}==True
    ${status}    run keyword and return status    page should contain text    ${browser}    Logout
    return from keyword if    ${status}==True
    should be true    ${status}

run webgui keyword with timeout
    [Documentation]  [Author:david qian] Set implicit wait time to ${timeout} before run keyword and reset implicit wait time to its origin value after run the keyword
    [Arguments]  ${timeout}    ${keyword}    ${browser}    @{args}
    [Teardown]  set_implicit_wait_time    ${browser}    ${origin_timeout}
    ${origin_timeout}    set_implicit_wait_time    ${browser}    ${timeout}
    ${ret}    run keyword    ${keyword}    ${browser}    @{args}
    [Return]  ${ret}

click links
    [Documentation]    [Author:david qian] Click every link of @{links}
    [Arguments]  ${browser}    @{links}
    :FOR    ${link}    IN    @{links}
    \    cpe click    ${browser}    link=${link}

verify table cell by column name
    [Documentation]  [Author:david qian]
    [Arguments]      ${browser}    ${table_locator}    ${row_index}    ${column_name}    ${expected_value}    ${cell_search_timeout}=1
    @{loc}     run webgui keyword with timeout    ${cell_search_timeout}    get_table_cell_contains_content    ${browser}    ${table_locator}        ${column_name}
    ${page_value}    run webgui keyword with timeout    ${cell_search_timeout}    get table cell    ${browser}    xpath=//table[@id='tab_wan']    ${row_index}    @{loc}[1]
    should be equal as strings     ${page_value}    ${expected_value}

which radio button is selected
    [Documentation]    Judge which radio button was selected, and return the button value
    ...    args:gui_session--session name(e.g. gui), group_name--the only one group name of all radio buttons,
    ...    radio_value_list--the list of values of all radio buttons' value attributes.
    [Arguments]    ${gui_session}    ${group_name}    @{radio_value_list}
    [Tags]    @author=syan
    :For    ${index}    in    @{radio_value_list}
    \    ${status}=    run keyword and return status    radio_button_should_be_set_to    ${gui_session}    ${group_name}    ${index}
    \    return from keyword if    ${status}==True    ${index}

get_status_of_gfast
    [Documentation]    Get specified status of gfast in GUI
    ...    args:gui_session--session name(e.g. gui), line_id--line id of 801F(e.g. 1 or 2),support both 801F and 801FB
    ...    status_name--the status name, only value "Link State", "RX Phy Rate", "TX Phy Rate", "RX ETR" and "TX ETR"
    ...    author=syan
    [Arguments]    ${gui_session}    ${line_id}    ${status_name}
    &{gfast_status_dic}=    create dictionary    Link State=2    RX Phy Rate=3    TX Phy Rate=4    RX ETR=5    TX ETR=6
    ${table_title_index}=    get from dictionary    ${gfast_status_dic}    ${status_name}
    ${row_index_of_table}=    evaluate  ${line_id}+1
    ${status}=    get element text    ${gui_session}    xpath=//h1[text()='G.fast']/parent::div//table[1]//tr[${row_index_of_table}]/td[${table_title_index}]
    [Return]    ${status}
