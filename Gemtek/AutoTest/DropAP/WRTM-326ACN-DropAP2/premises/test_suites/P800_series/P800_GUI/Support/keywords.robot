*** Settings ***
Documentation    Keywords for Support

*** Keywords ***
#verify table cell by column name
#    [Arguments]      ${browser}    ${table_locator}    ${row_index}    ${column_name}    ${expected_value}    ${cell_search_timeout}=1
#    @{loc}     run webgui keyword with timeout    ${cell_search_timeout}    get_table_cell_contains_content    ${browser}    ${table_locator}        ${column_name}
#    ${page_value}    run webgui keyword with timeout    ${cell_search_timeout}    get table cell    ${browser}    xpath=//table[@id='tab_wan']    ${row_index}    @{loc}[1]
#    should be equal      ${page_value}    ${expected_value}