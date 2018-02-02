*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${acceptable_special_character_username}    !*()-_.
${acceptable_special_character_password}    !*()-_.
${negative_special_character_username1}    !*()-_@
${negative_special_character_password1}    !*()-_@
${negative_special_character_username2}    !*()-_#
${negative_special_character_password2}    !*()-_#
${negative_special_character_username3}    !*()-_$
${negative_special_character_password3}    !*()-_$
${negative_special_character_username4}    !*()-_%
${negative_special_character_password4}    !*()-_%
${negative_special_character_username5}    !*()-_&
${negative_special_character_password5}    !*()-_&
${negative_special_character_username6}    !*()-_/
${negative_special_character_password6}    !*()-_/
${negative_special_character_username7}    !*()-_?
${negative_special_character_password7}    !*()-_?

*** Test Cases ***
tc_Security_Administrator_Credentials_Special_Characters
    [Documentation]    Verify the special characters are able to be used in username and password.
    ...    1.Modified the special characters username and password by web page, and that are able to login Web GUI.
    [Tags]   @TCID=STP_DD-TC-10557   @globalid=1506158    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore Username and Password
    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Record username and password by web Page
    Wait Until Keyword Succeeds    5x    3s    Record username    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    Record password    xpath=//input[@id="admin_password_password_field"]
    Set Global Variable     ${orininal_username_result}     ${record_username_result}
    Set Global Variable     ${orininal_password_result}     ${record_password_result}

    #Modified the acceptable special character username and password by web page
    Wait Until Keyword Succeeds    5x    3s    Modified special character    xpath=//input[@id="admin_username_field"]    ${acceptable_special_character_username}
    Wait Until Keyword Succeeds    5x    3s    Modified special character    xpath=//input[@id="admin_password_password_field"]    ${acceptable_special_character_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check modified the acceptable special character username and password
    Wait Until Keyword Succeeds    5x    3s    Check modified username    xpath=//input[@id="admin_username_field"]    ${acceptable_special_character_username}
    Wait Until Keyword Succeeds    5x    3s    Check modified password    xpath=//input[@id="admin_password_password_field"]    ${acceptable_special_character_password}

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Used modified the acceptable special character username and password login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${Check_modified_username_result}    ${Check_modified_password_result}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Modified the first negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username1}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password1}

    #Modified the second negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username2}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password2}

    #Modified the third negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username3}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password3}

    #Modified the fourth negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username4}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password4}

    #Modified the fifth negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username5}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password5}

    #Modified the sixth negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username6}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password6}

    #Modified the seventh negative special character username and password by web page, and check web page will be show error message
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_username_field"]    ${negative_special_character_username7}
    Wait Until Keyword Succeeds    5x    3s    Modified and check negative special character    xpath=//input[@id="admin_password_password_field"]    ${negative_special_character_password7}

*** Keywords ***
Record username
    [Arguments]    ${Xpath}
    [Documentation]    Record username values
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    ${get_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    ${Xpath}
    Set Global Variable    ${record_username_result}    ${get_username_result}

Record password
    [Arguments]    ${Xpath}
    [Documentation]    Record password values
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    ${get_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    ${Xpath}
    Set Global Variable    ${record_password_result}    ${get_password_result}

Modified special character
    [Arguments]    ${Xpath}    ${text}
    [Documentation]    Modified acceptable special character
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    Wait Until Keyword Succeeds    5x    3s    input_text    web    ${Xpath}    ${text}

Check modified username
    [Arguments]    ${Xpath}    ${text}
    [Documentation]    Check modified acceptable special character username
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    ${Check_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    ${Xpath}
    should be equal    ${Check_username_result}    ${text}
    Set Global Variable    ${Check_modified_username_result}    ${Check_username_result}

Check modified password
    [Arguments]    ${Xpath}    ${text}
    [Documentation]    Check modified acceptable special character password
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    ${Check_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    ${Xpath}
    should be equal    ${Check_password_result}    ${text}
    Set Global Variable    ${Check_modified_password_result}    ${Check_password_result}

Modified and check negative special character
    [Arguments]    ${Xpath}    ${text}
    [Documentation]    Modified negative special character and check error message
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    Wait Until Element Is Visible    web    ${Xpath}
    Wait Until Keyword Succeeds    5x    3s    input_text    web    ${Xpath}    ${text}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Web page will be show error message, and click OK to closed windows
    page should contain text    web    The Username contains invalid characters.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]

Restore Username and Password
    [Arguments]
    [Documentation]    Restore Username and Password
    [Tags]    @AUTHOR=Gemtek_Leo_Li

    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Restore initial record username and password by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_username_field"]    ${orininal_username_result}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${orininal_password_result}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

*** comment ***