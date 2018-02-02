*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***

*** Test Cases ***
tc_Security_Administrator_Credentials_Show_Password
    [Documentation]    Verify it is possible to see the password as it was entered.
    ...    1.When web page Administrator Password Enable Show, then it is possible to see the password.
    [Tags]   @TCID=STP_DD-TC-10556   @globalid=1506157    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Check by default it should not show plain password, so admin_password_password_field type is password, and the sytel should be display: inline-block; to show ● mask
    ${not_show_style} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    id=admin_password_password_field@style
    Should Contain    ${not_show_style}    display: inline-block;

    #Enable Administrator Password Show by web Page
    Wait Until Element Is Visible    web    id=show_admin_password_checkbox
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    id=show_admin_password_checkbox    1

    #After clicking on show password, the sytel of admin_password_password_field type should be display: none; to dismiss ● mask
    ${show_style} =    Wait Until Keyword Succeeds    5x    3s    get element attribute    web    id=admin_password_password_field@style
    Should Contain    ${show_style}    display: none;

*** Keywords ***

*** comment ***