*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${Application_Name}    Calix
${Application_Port_Start}    1
${Application_Port_End}    1

*** Test Cases ***
tc_SEC_FORWARD_Verify_that_One_Application_Forwarding_Rule_Can_Assign_to_Only_One_Device
    [Documentation]    Verify that One Application Forwarding Rule Can Assign to Only One Device.
    ...    1.Create New Association and add IP Address by web page.
    ...    2.If want to add another IP Address to the last created rule, the Apply button will turn gray.
    [Tags]   @TCID=STP_DD-TC-9504   @globalid=1440707    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
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

    #Create IP Address of Associate Application by web Page
    Wait Until Element Is Visible    web    id=associate_rule_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_rule_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address_field"]
    ${record_Associate_Application_IP} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address_field"]    ${record_Associate_Application_IP}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Go to Create IP Address of Associate Application again by web Page, and the Apply button will turn gray
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address_field"]    ${record_Associate_Application_IP}
    ${get_Application_Apply_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//button[@id="apply_edit_association_button"]@disabled
    Should Contain    ${get_Application_Apply_result}    true

*** Keywords ***
Restore original setting of Application Forwarding
    [Arguments]
    [Documentation]    Restore original setting of Application Forwarding
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Restore Create New Association's status by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Remove')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Edit')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Remove')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** comment ***