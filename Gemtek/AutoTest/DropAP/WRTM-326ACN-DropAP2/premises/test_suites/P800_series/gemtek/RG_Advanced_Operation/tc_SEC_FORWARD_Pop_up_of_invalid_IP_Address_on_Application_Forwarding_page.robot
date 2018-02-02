*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${negative_IP}    192.168.1.256

*** Test Cases ***
tc_SEC_FORWARD_Pop_up_of_invalid_IP_Address_on_Application_Forwarding_page
    [Documentation]    Verify an error message is show if create new application IP Address settings is negative.
    ...    1.Modified the negative IP Address settings by web page, and web page will be show error message.
    [Tags]   @TCID=STP_DD-TC-9508   @globalid=1440711    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to Application Forwarding by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    Application Forwarding

    #Create Application Name of Application Rule by web Page
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'New')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'New')]
    Wait Until Element Is Visible    web    id=associate_rule_with_ip_radio
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    associate_rule_with_ip_radio    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address_field"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address_field"]    ${negative_IP}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    The IP Address, "${negative_IP}", is not valid.Please enter an IP Address in the form of:"xxx.xxx.xxx.xxx"
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Ok')]
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Ok')]

*** Keywords ***

*** comment ***