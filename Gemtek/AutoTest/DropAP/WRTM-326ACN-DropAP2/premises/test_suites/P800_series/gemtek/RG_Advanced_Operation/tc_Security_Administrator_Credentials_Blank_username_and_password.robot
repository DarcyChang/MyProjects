*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li    stable

*** Variables ***
${modified_username}
${modified_password}

*** Test Cases ***
tc_Security_Administrator_Credentials_Blank_username_and_password
    [Documentation]    Verify an error message is shown if a blank username and password is applied.
    ...    1.Modified and input blank username and password by web page, and web page will be show error message.
    [Tags]   @TCID=STP_DD-TC-10551   @globalid=1506152    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Administrator Credentials by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Administrator Credentials

    #Input blank the username and password by web page
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_username_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_username_field"]    ${modified_username}
    Wait Until Element Is Visible    web    xpath=//input[@id="admin_password_password_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="admin_password_password_field"]    ${modified_password}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]

    #Web page will be show error message, and click OK to closed windows
    page should contain text    web    Please enter a Username.Please enter a Password.
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    cpe click    web    xpath=//button[contains(., 'Ok')]

*** Keywords ***

*** comment ***