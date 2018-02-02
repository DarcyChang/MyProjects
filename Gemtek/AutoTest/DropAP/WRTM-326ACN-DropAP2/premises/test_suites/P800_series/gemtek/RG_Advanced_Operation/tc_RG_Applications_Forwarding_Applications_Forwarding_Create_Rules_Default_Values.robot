*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${Create_Application_Rule_Name}    test rule
${Create_Application_Rule_Protocol}    UDP
${Create_Application_Rule_Port_Start}    8800
${Create_Application_Rule_Port_End}    8809
${Restore_times}    150
${Original_Association_Application}
${Original_Associate_Application_With_Device}    display: none;
${Original_Application_Rule_Name}
${Original_Application_Rule_Protocol}    TCP
${Original_Application_Rule_Port_Start}
${Original_Application_Rule_Port_End}

*** Test Cases ***
tc_RG_Applications_Forwarding_Applications_Forwarding_Create_Rules_Default_Values
    [Documentation]    Verify the default values when creating a new rule.
    ...    1.When web page choose Restore Defaults, the gateway device Application Forwarding settings must be Restore default values.
    [Tags]   @TCID=STP_DD-TC-10510   @globalid=1506106    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
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
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="application_name_field"]    ${Create_Application_Rule_Name}

    #Create Application Protocol of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//select[@id='application_protocol_selector']
    select_from_list_by_label    web    xpath=//select[@id='application_protocol_selector']    ${Create_Application_Rule_Protocol}

    #Create Application Port Start and Port End of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${Create_Application_Rule_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${Create_Application_Rule_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check Create New Application Rule settings by web Page
    Wait Until Element Is Visible    web    xpath=//span[@id="applications_table_application_name"]
    ${get_Application_Rule_Name_result} =    Wait Until Keyword Succeeds    5x    3s    get element text    web    xpath=//span[@id="applications_table_application_name"]
    Should Contain    ${get_Application_Rule_Name_result}    ${Create_Application_Rule_Name}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    1    ${Create_Application_Rule_Protocol}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    2    ${Create_Application_Rule_Port_Start}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    3    ${Create_Application_Rule_Port_End}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Go Back')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Go Back')]

    #Check Association Application field value by web Page
    ${get_Association_Application_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//select[@id="application_select"]
    should be equal    ${get_Association_Application_result}    ${Create_Application_Rule_Name}

    #Record Device address of the Associate Application
    Wait Until Element Is Visible    web    id=lan_device_selector
    ${record_Device_address} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    id=lan_device_selector

    #Create New Association and select Associate Application With IP Address
    Wait Until Element Is Visible    web    id=associate_rule_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_rule_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address_field"]    ${record_Device_address}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check Associate Application settings by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='associations_table']    2    2    ${record_Device_address}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='associations_table']    2    3    ${Create_Application_Rule_Name}

    #Choose Restore Defaults by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Restore Defaults
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Restore')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Restore')]    ${Restore_times}    #After Restore finish, web page Restore button will display.

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Check default Association Application field value by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    ${get_Association_Application_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//select[@id="application_select"]
    should be equal    ${get_Association_Application_result}    ${Original_Association_Application}

    #Check default value of Associate Application With Device
    ${get_Associate_Application_With_Device_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="ip_address_field"]@style
    Should Contain    ${get_Associate_Application_With_Device_result}    ${Original_Associate_Application_With_Device}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='associations_table']    2    1    No Entries Defined

    #Check default Application Name of Application Rule
    Wait Until Element Is Visible    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Element Is Visible    web     xpath=//input[@id="application_name_field"]
    ${get_Application_Rule_Name_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="application_name_field"]
    should be equal    ${get_Application_Rule_Name_result}    ${Original_Application_Rule_Name}

    #Check default Application Protocol of Application Rule
    Wait Until Element Is Visible    web     xpath=//select[@id="application_protocol_selector"]
    ${get_Application_Rule_Protocol_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//select[@id="application_protocol_selector"]
    should be equal    ${get_Application_Rule_Protocol_result}    ${Original_Application_Rule_Protocol}

    #Check default Application Port Start of Application Rule
    ${get_Application_Rule_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="port_start_field"]
    Should Contain    ${get_Application_Rule_Port_Start_result}    ${Original_Application_Rule_Port_Start}

    #Check default Application Port End of Application Rule
    ${get_Application_Rule_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="port_end_field"]
    Should Contain    ${get_Application_Rule_Port_End_result}    ${Original_Application_Rule_Port_End}

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