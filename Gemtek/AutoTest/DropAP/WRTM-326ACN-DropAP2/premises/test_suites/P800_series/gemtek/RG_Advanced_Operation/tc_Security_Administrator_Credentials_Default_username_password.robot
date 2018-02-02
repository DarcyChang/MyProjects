*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${modified_username}    calix
${modified_password}    calix
${Restore_times}    150

*** Test Cases ***
tc_Security_Administrator_Credentials_Default_username_password
    [Documentation]    Verify the default provisioning is to require an well known username and password.
    ...    1.When web page choose Restore Defaults, the gateway device username and password must be Restore default values.
    [Tags]   @TCID=STP_DD-TC-10549   @globalid=1506150    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

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

    #Choose Restore Defaults by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Utilities
    Wait Until Keyword Succeeds    5x    3s    click links    web    Restore Defaults
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Restore')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Restore')]    ${Restore_times}    #After Restore finish, web page Restore button will display.

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Check default username and password by web Page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    ${default_username_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_username_field"]
    should not be equal    ${default_username_result}    ${modified_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${default_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    should not be equal    ${default_password_result}    ${modified_password}

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Used default username and password login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${default_username_result}    ${default_password_result}

*** Keywords ***

*** comment ***