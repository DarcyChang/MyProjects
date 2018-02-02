*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${modified_Ending_IP_Address}    192.168.1.100
${modified_Device_IP_Address}    192.168.1.200

*** Test Cases ***
tc_RG_IP_Addressing_DHCP_Settings_Device_IP_Address
    [Documentation]    Verify setting up Device IP Address using a different IP Address for the ONT.
    ...    1.Modified the Device different IP address by web page, and that are able to login Web GUI.
    [Tags]   @TCID=STP_DD-TC-9576   @globalid=1442514    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore original DHCP setting
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to DHCP Settings by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    IP Addressing
    Wait Until Keyword Succeeds    5x    3s    click links    web    DHCP Settings

    #Record Device IP Address and Ending IP Address by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_interface_ip_address"]
    ${record_Device_IP_Address_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="ip_interface_ip_address"]
    Set Global Variable     ${orininal_Device_IP_Address_result}     ${record_Device_IP_Address_result}
    Wait Until Element Is Visible    web    xpath=//input[@id="end_ip_address"]
    ${record_Ending_IP_Address_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="end_ip_address"]
    Set Global Variable     ${orininal_Ending_IP_Address_result}     ${record_Ending_IP_Address_result}

    #Modified the Ending IP Address by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="end_ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="end_ip_address"]    ${modified_Ending_IP_Address}

    #Modified the Device IP Address by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_interface_ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_interface_ip_address"]    ${modified_Device_IP_Address}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Device IP Address has been changed from its original value.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Used modified Device IP Address login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${modified_Device_IP_Address}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Check DHCP Settings Device IP Address by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    IP Addressing
    Wait Until Keyword Succeeds    5x    3s    click links    web    DHCP Settings
    ${get_Device_IP_Address_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="ip_interface_ip_address"]
    should be equal    ${get_Device_IP_Address_result}    ${modified_Device_IP_Address}

*** Keywords ***
Restore original DHCP setting
    [Arguments]
    [Documentation]    Restore original DHCP setting
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    #Restore original DHCP setting by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_interface_ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_interface_ip_address"]    ${orininal_Device_IP_Address_result}
    Wait Until Element Is Visible    web    xpath=//input[@id="end_ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="end_ip_address"]    ${orininal_Ending_IP_Address_result}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The Device IP Address has been changed from its original value.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

*** comment ***