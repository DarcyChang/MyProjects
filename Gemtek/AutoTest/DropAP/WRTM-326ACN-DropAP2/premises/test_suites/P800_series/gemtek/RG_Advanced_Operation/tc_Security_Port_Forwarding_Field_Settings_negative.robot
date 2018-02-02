*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${negative_Local_IP}    255.255.255.255
${negative_Local_Port_Start}    0
${negative_Local_Port_End}    0
${Local_Port_Start}    1
${Local_Port_End}    1
${negative_Remote_IP}    255.255.255.255
${negative_Remote_Port_Start}    0
${negative_Remote_Port_End}    0
${Original_Local_Port_Start}
${Original_Local_Port_End}
${Original_Remote_Port_Start}
${Original_Remote_Port_End}

*** Test Cases ***
tc_Security_Port_Forwarding_Field_Settings_negative
    [Documentation]    Verify an error message is show if create new association field settings is negative.
    ...    1.Modified and input negative field settings by web page, and web page will be show error message.
    [Tags]   @TCID=STP_DD-TC-10506   @globalid=1506102    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore original setting of Port Forwarding
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Port Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Port Forwarding

    #Create negative New Association Local IP and check error message by web page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    id=associate_local_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_local_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="local_ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_ip_address_field"]    ${negative_Local_IP}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Local IP Address, "${negative_Local_IP}", is not valid.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Clear Fields')]    #Clears negative Local IP settings.

    #Create negative New Association Local Port Start and Port End, and check error message by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_start_field"]    ${negative_Local_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_end_field"]    ${negative_Local_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Local Port Port Start value, "${negative_Local_Port_Start}", is not a valid port value in the range (1 - 65535).The Local Port Port End value, "${negative_Local_Port_End}", is not a valid port value in the range (1 - 65535).
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Clear Fields')]    #Clears negative Local Port Start and Port End settings.

    #Create acceptable New Association Local Port Start and Port End by web page, and ensure that it will not be checked to Local side settings
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_start_field"]    ${Local_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_end_field"]    ${Local_Port_End}

    #Create negative New Association Remote IP and check error message by web page
    Wait Until Element Is Visible    web    id=associate_remote_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_remote_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_ip_address_field"]    ${negative_Remote_IP}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Remote IP Address, "${negative_Remote_IP}", is not valid.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[@id="clear_edit_remote_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="clear_edit_remote_button"]    #Clears negative Remote IP settings.

    #Create negative New Association Remote Port Start and Port End, and check error message by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_port_start_field"]    ${negative_Remote_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_port_end_field"]    ${negative_Remote_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Remote Port Port Start value, "${negative_Remote_Port_Start}", is not a valid port value in the range (1 - 65535).The Remote Port Port End value, "${negative_Remote_Port_End}", is not a valid port value in the range (1 - 65535).
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** Keywords ***
Restore Original setting of Port Forwarding
    [Arguments]
    [Documentation]    Restore original setting of Application Forwarding
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Clear Fields')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Clear Fields')]    #Clears Local Port Start and Port End settings.
    ${get_Local_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="local_port_start_field"]
    Should Contain    ${get_Local_Port_Start_result}    ${Original_Local_Port_Start}
    ${get_Local_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="local_port_end_field"]
    Should Contain    ${get_Local_Port_Start_result}    ${Original_Local_Port_End}
    Wait Until Element Is Visible    web    xpath=//button[@id="clear_edit_remote_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="clear_edit_remote_button"]    #Clears negative Remote Port Start and Port End settings.
    ${get_Remote_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="remote_port_start_field"]
    Should Contain    ${get_Remote_Port_Start_result}    ${Original_Remote_Port_Start}
    ${get_Remote_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="remote_port_end_field"]
    Should Contain    ${get_Remote_Port_End_result}    ${Original_Remote_Port_End}

*** comment ***