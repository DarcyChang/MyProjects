*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${Restore_times}    150
${Original_Associate_Application_With_Device}    display: none;
${Original_Application_Name}
${Original_Application_Protocol}    TCP
${Original_Application_Port_Start}    1 - 65535
${Original_Application_Port_End}    1 - 65535

*** Test Cases ***
tc_SEC_FORWARD_Default_settings_of_Application_Forwarding_page
    [Documentation]    Verify Restore Defaults the device gateway, default settings should be restoring to factory defaults.
    ...    1.When web page choose Restore Defaults, the gateway device Application Forwarding settings must be Restore default values.
    [Tags]   @TCID=STP_DD-TC-9502   @globalid=1440705    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

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

    #Check default Application message of Application Forwarding, when click the View button
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'View')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'View')]
    page should contain text    web    No Application Rule is selected
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Check default value of Associate Application With Device
    ${get_Associate_Application_With_Device_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="ip_address_field"]@style
    Should Contain    ${get_Associate_Application_With_Device_result}    ${Original_Associate_Application_With_Device}

    #Check default Application Name of Application Rule, when click the New button
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web     xpath=//input[@id="application_name_field"]
    ${get_Application_Name_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="application_name_field"]
    should be equal    ${get_Application_Name_result}    ${Original_Application_Name}

    #Check default Application Protocol of Application Rule
    Wait Until Element Is Visible    web     xpath=//select[@id="application_protocol_selector"]
    ${get_Application_Protocol_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//select[@id="application_protocol_selector"]
    should be equal    ${get_Application_Protocol_result}    ${Original_Application_Protocol}

    #Check default Application Port Start of Application Rule
    ${get_Application_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="port_start_field"]@placeholder
    Should Contain    ${get_Application_Port_Start_result}    ${Original_Application_Port_Start}

    #Check default Application Port End of Application Rule
    ${get_Application_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="port_end_field"]@placeholder
    Should Contain    ${get_Application_Port_End_result}    ${Original_Application_Port_End}

*** Keywords ***

*** comment ***