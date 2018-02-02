*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${modified_username}    calix
${modified_password}    calix

*** Test Cases ***
tc_Security_Administrator_Credentials_Edit_username_password
    [Documentation]    Verify the user is able to modify username and password.
    ...    1.Modified the username and password by web page, and that are able to login Web GUI.
    [Tags]   @TCID=STP_DD-TC-10550   @globalid=1506151    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    [Teardown]    Restore Username and Password
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

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

    #Modified the username and password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_username_field"]    ${modified_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${modified_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check modified username and password by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    ${modified_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_username_field"]
    should be equal    ${modified_username_result}    ${modified_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${modified_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    should be equal    ${modified_password_result}    ${modified_password}

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
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

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