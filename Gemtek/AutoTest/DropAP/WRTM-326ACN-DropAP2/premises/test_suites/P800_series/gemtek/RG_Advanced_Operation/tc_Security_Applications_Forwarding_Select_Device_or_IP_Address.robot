*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${Application_Name}    Calix
${Application_Port_Start}    1
${Application_Port_End}    1
${Original_Associate_Application_With_Device}    display: none;
${Original_Associate_Application_With_IP_Address}    display: inline;

*** Test Cases ***
tc_Security_Applications_Forwarding_Select_Device_or_IP_Address
    [Documentation]    Verify Application Forwarding Create New Association, Associate Application can be selected device or IP address.
    ...    1.When Create New Association, Associate Application can be selected device or IP address.
    [Tags]   @TCID=STP_DD-TC-10509   @globalid=1506105    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore original setting of Application Forwarding
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Go to create New Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="create_application_rule_button"]

    #Create Application Name of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="application_name_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="application_name_field"]    ${Application_Name}

    #Create Application Port Start of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${Application_Port_Start}

    #Create Application Port End of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${Application_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Go Back')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Go Back')]

    #Record Device address of the Associate Application
    Wait Until Element Is Visible    web    id=lan_device_selector
    ${record_Device_address} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    id=lan_device_selector

    #Create New Association and select Associate Application With Device
    Wait Until Element Is Visible    web    id=associate_rule_with_device_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_rule_with_device_radio    1
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check that Associate Application is selected Device
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    ${get_Associate_Application_With_Device_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="ip_address_field"]@style
    Should Contain    ${get_Associate_Application_With_Device_result}    ${Original_Associate_Application_With_Device}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='associations_table']    2    2    ${record_Device_address}

    #Remove Create New Association With Device
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    page should contain text    web    Are you sure that you want to remove the association between ${record_Device_address} at IP Address ${record_Device_address} and ${Application_Name}.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Create New Association and select Associate Application With IP Address
    Wait Until Element Is Visible    web    id=associate_rule_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_rule_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address_field"]    ${record_Device_address}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check that Associate Application is selected IP Address
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    ${get_Associate_Application_With_IP_Address_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="ip_address_field"]@style
    Should Contain    ${get_Associate_Application_With_IP_Address_result}    ${Original_Associate_Application_With_IP_Address}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='associations_table']    2    2    ${record_Device_address}

    #Remove Create New Association With IP Address
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    page should contain text    web    Are you sure that you want to remove the association between ${record_Device_address} at IP Address ${record_Device_address} and ${Application_Name}.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Restore original setting of Application Forwarding
    [Arguments]
    [Documentation]    Restore original setting of Application Forwarding
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    #Remove rule of Application
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Edit')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Remove')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    page should contain text    web    Are you sure that you want to remove
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** comment ***