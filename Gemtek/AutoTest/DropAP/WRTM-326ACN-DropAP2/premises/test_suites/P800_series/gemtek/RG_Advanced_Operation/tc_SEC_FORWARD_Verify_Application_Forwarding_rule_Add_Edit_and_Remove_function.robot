*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${Application_Name}    test rule
${Application_Protocol}    TCP
${Application_Port_Start}    8800
${Application_Port_End}    8809
${edit_Application_Port_Start}    8888
${edit_Application_Port_End}    8889


*** Test Cases ***
tc_SEC_FORWARD_Verify_Application_Forwarding_rule_Add_Edit_and_Remove_function
    [Documentation]    Verify “Application Forwarding” rule “Add”, “Edit” and “Remove” function.
    ...    1.When Create New Application Rule, web page can be clicked “New”, “Edit” and “Remove” button.
    [Tags]   @TCID=STP_DD-TC-9503   @globalid=1440706    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Create Application Name of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Element Is Visible    web    xpath=//input[@id="application_name_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="application_name_field"]    ${Application_Name}

    #Create Application Protocol by web Page
    Wait Until Element Is Visible    web    xpath=//select[@id='application_protocol_selector']
    select_from_list_by_label    web    xpath=//select[@id='application_protocol_selector']    ${Application_Protocol}

    #Create Application Port Start and Port End by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${Application_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${Application_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check Create New Application Rule settings by web Page
    Wait Until Element Is Visible    web    xpath=//span[@id="applications_table_application_name"]
    ${get_Application_Name_result} =    Wait Until Keyword Succeeds    5x    3s    get element text    web    xpath=//span[@id="applications_table_application_name"]
    log    ${get_Application_Name_result}
    Should Contain    ${get_Application_Name_result}    ${Application_Name}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    1    ${Application_Protocol}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    2    ${Application_Port_Start}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    3    ${Application_Port_End}

    #Edit Create New Application Rule Port Start and Port End settings by web Page
    #Wait Until Keyword Succeeds    5x    3s     Edit Application Rule    web    xpath=//table[@id='applications_table']    2    4    xpath=//button[contains(., 'Edit')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${edit_Application_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${edit_Application_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check Edit Create New Application Rule Port Start and Port End settings by web Page
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    2    ${edit_Application_Port_Start}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    3    ${edit_Application_Port_End}

    #Remove Create New Application Rule settings by web Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    page should contain text    web    Are you sure that you want to removeApplication Rule: "${Application_Name}"?
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Check Remove Create New Application Rule settings by web Page
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    1    No Entries Defined

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

*** comment ***