*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=RG_Advanced_Operation    @AUTHOR=Gemtek_Leo_Li

*** Variables ***
${negative_DMZ_Hosting_IP Address}    192.168.1.255

*** Test Cases ***
tc_Security_DMZ_Hosting_Enable_Manually_enter_IP_negative
    [Documentation]    Verify an error message is show if manually enter the DMZ Hosting IP address is negative.
    ...    1.Enter the DMZ Hosting negative IP address by web page, and web page will be show error message.
    [Tags]   @TCID=STP_DD-TC-10504   @globalid=1506094    @DUT=844FB  @DUT=844F    @AUTHOR=Gemtek_Leo_Li
    [Timeout]
    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}

    #Go to DMZ Hosting Settings by web Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Advanced
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    click links    web    DMZ Hosting

    #Modified DMZ state settings by web page
    Wait Until Element Is Visible    web    id=dmz_on
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    dmz_on    1

    #Modified negative DMZ Hosting IP Address by web page, and check error message by web page
    Wait Until Element Is Visible    web    id=deviceTypeRadio2
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    deviceTypeRadio2    1
    Wait Until Element Is Visible    web    xpath=//input[@id="ip_address"]
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id="ip_address"]    ${negative_DMZ_Hosting_IP Address}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text    web    IP Address "${negative_DMZ_Hosting_IP Address}" is restricted. Please choose another one.

*** Keywords ***

*** comment ***