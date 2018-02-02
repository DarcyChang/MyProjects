*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${modified_username}    calix
${modified_password}    calix

*** Test Cases ***
tc_Security_Administrator_Credentials_Without_Apply
    [Documentation]    Verify a modification is not applied if 'Apply' is not clicked.
    ...    1.Modified username and password by web page, and then not clicked  'Apply'.
    ...    2.Modified username and password will not be applied.
    [Tags]   @TCID=STP_DD-TC-10558   @globalid=1506159    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
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

    #Modified the username and password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_username_field"]    ${modified_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${modified_password}

    #Check modified username and password by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    ${modified_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_username_field"]
    should not be equal    ${modified_username_result}    ${record_username_result}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${modified_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    should not be equal    ${modified_password_result}    ${record_password_result}

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Used default username and password login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${record_username_result}    ${record_password_result}

*** Keywords ***

*** comment ***