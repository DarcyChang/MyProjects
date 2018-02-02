*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${acceptable_special_character_Application_Rule_Name}    -_    #!*()-_.
${Create_Application_Rule_Port_Start}    8800
${Create_Application_Rule_Port_End}    8809
${negative_special_character_Application_Rule_Name1}    -_!
${negative_special_character_Application_Rule_Name2}    -_*
${negative_special_character_Application_Rule_Name3}    -_(
${negative_special_character_Application_Rule_Name4}    -_)
${negative_special_character_Application_Rule_Name5}    -_.


*** Test Cases ***
tc_Security_Applications_Forwarding_Available_Characters
    [Documentation]    Verify if special characters can be entered for Application Forwarding.
    ...    1.Entered the special characters for Application Forwarding by web page, and that are able to Create New Application Rule.
    [Tags]   @TCID=STP_DD-TC-10511   @globalid=1506107    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Modified the acceptable special character Application Name by Application Rule web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[@id="create_application_rule_button"]
    Wait Until Element Is Visible    web    xpath=//input[@id="application_name_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="application_name_field"]    ${acceptable_special_character_Application_Rule_Name}

    #Create Application Port Start and Port End by Application Rule web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="port_start_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_start_field"]    ${Create_Application_Rule_Port_Start}
    Wait Until Element Is Visible    web    xpath=//input[@id="port_end_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="port_end_field"]    ${Create_Application_Rule_Port_End}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check Create New Application Rule settings by web Page
    Wait Until Element Is Visible    web    xpath=//span[@id="applications_table_application_name"]
    ${get_Application_Rule_Name_result} =    Wait Until Keyword Succeeds    5x    3s    get element text    web    xpath=//span[@id="applications_table_application_name"]
    Should Contain    ${get_Application_Rule_Name_result}    ${acceptable_special_character_Application_Rule_Name}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    2    ${Create_Application_Rule_Port_Start}
    Wait Until Keyword Succeeds    5x    3s     Cell Data Should Contain    web    xpath=//table[@id='applications_table']    2    3    ${Create_Application_Rule_Port_End}

    #Remove Create New Application Rule settings by web Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Remove')]
    page should contain text    web    Are you sure that you want to removeApplication Rule: "${acceptable_special_character_Application_Rule_Name}"?
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

    #Modified the first negative special character Application Rule Name by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character Application Rule Name    xpath=//input[@id="application_name_field"]    ${negative_special_character_Application_Rule_Name1}

    #Modified the second negative special character Application Rule Name by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character Application Rule Name    xpath=//input[@id="application_name_field"]    ${negative_special_character_Application_Rule_Name2}

    #Modified the third negative special character Application Rule Name by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character Application Rule Name    xpath=//input[@id="application_name_field"]    ${negative_special_character_Application_Rule_Name3}

    #Modified the fourth negative special character Application Rule Name by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character Application Rule Name    xpath=//input[@id="application_name_field"]    ${negative_special_character_Application_Rule_Name4}

    #Modified the fifth negative special character Application Rule Name by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character Application Rule Name    xpath=//input[@id="application_name_field"]    ${negative_special_character_Application_Rule_Name5}

*** Keywords ***
Cell Data Should Contain
    [Arguments]    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}    ${included_string}
    [Documentation]    Get cell data from table, and it should contain ${included_string}
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    ${cell1} =    run webgui keyword with timeout    1    get_table_cell    ${my_gui_session}    ${my_table}    ${my_row}    ${my_column}
    log    ${cell1}
    Should Contain    ${cell1}    ${included_string}

Modified and check negative special character Application Rule Name
    [Arguments]    ${Xpath}    ${text}
    [Documentation]    Modified negative special character Application Rule Name and check error message
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    Wait Until Keyword Succeeds    5x    3s    input_text    web    ${Xpath}    ${text}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Web page will be show error message, and click OK to closed windows
    page should contain text    web    The Application Name cannot include invalid character
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]

*** comment ***