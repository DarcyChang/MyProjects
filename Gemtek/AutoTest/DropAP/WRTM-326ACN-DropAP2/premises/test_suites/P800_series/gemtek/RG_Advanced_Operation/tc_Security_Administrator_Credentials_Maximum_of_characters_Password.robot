*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${Maximum_password}    calixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalixcalix1234    #Password field accept up to 64 characters.

*** Test Cases ***
tc_Security_Administrator_Credentials_Maximum_of_characters_Password
    [Documentation]    Verify that is able to login with the maximum number 64 password characters.
    ...    1.Modified the maximum number 64 password characters by web page, and that are able to login Web GUI.
    [Tags]   @TCID=STP_DD-TC-10553   @globalid=1506154    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
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

    #Modified Maximum of characters password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${Maximum_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Check modified Maximum of characters password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    ${modified_password_result} =    Wait Until Keyword Succeeds    5x    3s    get_element_value    web    xpath=//input[@id="admin_password_password_field"]
    should be equal    ${modified_password_result}    ${Maximum_password}

    #Logout Web GUI
    Wait Until Keyword Succeeds    5x    3s    click links    web    Logout

    #Used modified username and password login Web GUI
    Wait Until Keyword Succeeds    5x    3s    login ont    web    ${g_844fb_gui_url}    ${record_username_result}    ${modified_password_result}

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