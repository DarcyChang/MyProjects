*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${Original_Local_Device}    display: none;
${Original_Local_Protocol}    TCP
${Original_Local_Port_Start}
${Original_Local_Port_End}
${Original_Remote_All_IP_Addresses}    display: none;
${Original_Remote_Port_Start}
${Original_Remote_Port_End}
${modified_Local_Protocol}    UDP
${modified_Local_Port_Start}    1
${modified_Local_Port_End}    1
${modified_Remote_IP}    192.168.1.200
${modified_Remote_Port_Start}    1
${modified_Remote_Port_End}    1
${Restore_times}    150

*** Test Cases ***
tc_Security_Port_Forwarding_Default_Settings
    [Documentation]    Verify Restore Defaults the device gateway, default settings should be restoring to factory defaults.
    ...    1.When web page choose Restore Defaults, the gateway device Port Forwarding settings must be Restore default values.
    [Tags]   @TCID=STP_DD-TC-10505   @globalid=1506101    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Port Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Port Forwarding

    #Create New Association Local IP and Protocol and Port by web page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    id=associate_local_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_local_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//select[@id='protocol_selector']
    select_from_list_by_label    web    xpath=//select[@id='protocol_selector']    ${modified_Local_Protocol}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_start_field"]    ${modified_Local_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="local_port_end_field"]    ${modified_Local_Port_End}

    #Create New Association Remote IP and Port by web page
    Wait Until Element Is Visible    web    id=associate_remote_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_remote_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_ip_address_field"]    ${modified_Remote_IP}
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_port_start_field"]    ${modified_Remote_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="remote_port_end_field"]    ${modified_Remote_Port_End}
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Apply')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Remove')]    #After Apply finish, web page will display Remove button.

    #Choose Restore Defaults by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Restore Defaults
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Restore')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Restore')]    ${Restore_times}    #After Restore finish, web page will display Restore button.

    #Check default Port Forwarding without any rules by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Port Forwarding

    #Check default values of Port Forwarding Local settings by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    ${get_Local_Device_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="local_ip_address_field"]@style
    Should Contain    ${get_Local_Device_result}    ${Original_Local_Device}
    Wait Until Element Is Visible    web    xpath=//select[@id="protocol_selector"]
    ${get_Local_Protocol_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//select[@id="protocol_selector"]
    should be equal    ${get_Local_Protocol_result}    ${Original_Local_Protocol}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_start_field"]
    ${get_Local_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="local_port_start_field"]
    should be equal    ${get_Local_Port_Start_result}    ${Original_Local_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="local_port_end_field"]
    ${get_Local_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="local_port_end_field"]
    should be equal    ${get_Local_Port_End_result}    ${Original_Local_Port_End}

    #Check default values of Port Forwarding Remote settings by web Page
    ${get_Remote_All_IP_Addresses_result} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    xpath=//input[@id="remote_ip_address_field"]@style
    Should Contain    ${get_Remote_All_IP_Addresses_result}    ${Original_Remote_All_IP_Addresses}
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_start_field"]
    ${get_Remote_Port_Start_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="remote_port_start_field"]
    should be equal    ${get_Remote_Port_Start_result}    ${Original_Remote_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="remote_port_end_field"]
    ${get_Remote_Port_End_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="remote_port_end_field"]
    should be equal    ${get_Remote_Port_End_result}    ${Original_Remote_Port_End}

*** Keywords ***

*** comment ***