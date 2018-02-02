*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${Maximum_username}    calixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalix1234
${Maximum_password}    calixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalix1234
${negative_username}    calixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalix12345
${negative_password}    calixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalix12345

*** Test Cases ***
tc_Security_Administrator_Credentials_Maximum_of_characters_negative
    [Documentation]    Verify that is not possible to exceed the maximum number 64 caracters.
    ...    1.Modified the maximum number 64 username and password characters by web page, and check is not possible to exceed the maximum number 64 caracters.
    [Tags]   @TCID=STP_DD-TC-10554   @globalid=1506155    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore Username and Password
    #Login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Record username and password by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    ${record_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_username_field"]
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${record_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    Set Global Variable     ${orininal_username_result}     ${record_username_result}
    Set Global Variable     ${orininal_password_result}     ${record_password_result}

    #Modified Maximum of characters username and password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_username_field"]    ${negative_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${negative_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check modified Maximum of characters username and password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    ${modified_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_username_field"]
    #Because of character limit, so even user input over 64 characters, Web GUI will just accept 64 character any way, so we just directly check maximum username value.
    should be equal    ${modified_username_result}    ${Maximum_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${modified_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    #Because of character limit, so even user input over 64 characters, Web GUI will just accept 64 character any way, so we just directly check maximum password value.
    should be equal    ${modified_password_result}    ${Maximum_password}

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Used modified username and password login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${modified_username_result}    ${modified_password_result}

*** Keywords ***
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