*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${Application_Name}    test rule
${negative_Application_Port_Start}    90000
${negative_Application_Port_End}    90000

*** Test Cases ***
tc_SEC_FORWARD_Pop_up_of_invalid_port_range_on_Application_Forwarding_page
    [Documentation]    Verify an error message is show if create new application port range settings is negative.
    ...    1.Modified the negative port range settings by web page, and web page will be show error message.
    [Tags]   @TCID=STP_DD-TC-9505   @globalid=1440708    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
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

    #Create negative Application Port Start and Port End by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${negative_Application_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${negative_Application_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #check error message by web page
    page should contain text    web    Port Start value is out of range: ${negative_Application_Port_Start}Please enter a number between 1 and 65535.Port End value is out of range: ${negative_Application_Port_End}Please enter a number between 1 and 65535.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** Keywords ***

*** comment ***